"""Struct parsing classes and helper functions"""

import ctypes
import logging
from pydoc import locate

ASTERISK = "*"
ARRAY_START = "["
ARRAY_END = "]"

# set up logging
logging.basicConfig()
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # set log level for this module


def extract_type(type_str: str):
    """Extract ctypes data type from a string

    Return:
        parsed type and number of elements (in order to handle arrays)
            on success
        (None, x) on error (e.g. struct required)
    """
    num_elems = 1
    # locate data type from name
    res = locate(f"ctypes.c_{type_str.split()[0]}")

    # treat all pointers as void pointers (same size)
    if ASTERISK in type_str:
        res = ctypes.c_voidp
    elif all(x in type_str for x in [ARRAY_START, ARRAY_END]):
        # type is an array: find the length (characters between the two
        # brackets)
        start_pos = type_str.find(ARRAY_START)
        end_pos = type_str.find(ARRAY_END)

        # len(ARRAY_START):end_pos
        num_elems = type_str[start_pos + len(ARRAY_START):end_pos].strip()

    return (res, int(num_elems))


class StructMember:
    """C struct member information

    Attributes:
        name (str): struct member name
        type_str (str): C data type string
        dtype (type): ctypes data type derived from type+str
        dep_struct (str): name of struct dtype depends on (if dtype is None)
    """

    def __init__(self, member_str):
        # check for and strip asterisks before continuing
        asterisk_count = member_str.count(ASTERISK)
        member_str = member_str.replace(ASTERISK, "")

        # set name (now stripped of asterisks and semicolon at end of line)
        self.name = member_str.split(" ")[-1].strip(";")

        self.type_str = member_str.split(" ")[:-1]
        # append stripped asterisks and remove empty elements
        self.type_str = list(filter(None, (self.type_str + [ASTERISK *
                                    asterisk_count])))

        self.dtype, self.length = extract_type(
                " ".join(self.type_str + [self.name]))
        logger.debug("name = %s, type_str = %s, dtype = %s",
                     self.name, self.type_str, self.dtype)

        # type requires a struct
        if self.dtype is None:
            self.dep_struct = ("".join(self.type_str)).replace(
                    "struct", "")
            # strip square brackets from array
            self.dep_struct = self.dep_struct.split(ARRAY_START, 1)[0]
            logger.debug("member %s needs %s", self.name, self.dep_struct)

    def __str__(self):
        return f"{self.name} ({" ".join(self.type_str)})"

    def to_tuple(self):
        """Convert name and data type to tuple expected by ctypes.Structure"""
        return (self.name, self.dtype)


class Struct:
    """C struct information

    Attributes:
        name (str): struct name
        members (StructMember[]): list of struct members
    """

    def __init__(self, name, members):
        self.name = name
        self.members = [StructMember(x) for x in members]
        self.dtype = None

        # convert to structure if all member data types are defined
        if all(x.dtype is not None for x in self.members):
            self.dtype = self.to_structure()

    def __str__(self):
        res = [f"struct {self.name}: "]
        for member in self.members:
            res.append(str(member))

        res = res[0] + ", ".join(res[1:])
        return res

    def to_structure(self):
        """Convert struct to ctypes.Structure"""
        logger.debug([member.__str__() for member in self.members])
        return type(self.name, (ctypes.Structure,),
                    {"_fields_": [member.to_tuple() for member in
                                  self.members]})

    def to_json(self):
        """Convert struct to JSON object"""
        data = {}

        data["name"] = self.name
        data["size"] = ctypes.sizeof(self.dtype)
        data["alignment"] = ctypes.alignment(self.dtype)
        data["members"] = [{"name": member.name,
                            "size":
                                ctypes.sizeof(member.dtype) * member.length,
                            "alignment": ctypes.alignment(member.dtype)
                            } for member in self.members]

        return data


def extract_type_with_struct(type_str: str, dep_struct: Struct, length: int):
    """Extract ctypes data type from a string and the struct it depends on

    Parameters:
        type_str (str): C data type string
        required_struct (Struct): struct the type depends on
        length (int): number of elements the member consists of
            (handle arrays of structs)
    """
    res = None

    for word in type_str:
        if word == dep_struct.name:
            res = dep_struct.dtype

    return res
