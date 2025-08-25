"""Struct parsing classes and helper functions"""

import ctypes
import logging
from pydoc import locate

ASTERISK = "*"


def extract_type(type_str: str):
    """Extract ctypes data type from a string

    Return:
        parsed type on success
        None on error (e.g. struct required)
    """
    # locate data type from name
    res = locate(f"ctypes.c_{type_str.split()[0]}")

    # treat all pointers as void pointers (same size)
    if ASTERISK in type_str:
        res = ctypes.c_voidp

    return res


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

        self.dtype = extract_type(" ".join(self.type_str))
        logging.debug("name = %s, type_str = %s, dtype = %s",
                      self.name, self.type_str, self.dtype)

        # type requires a struct
        if self.dtype is None:
            self.dep_struct = ("".join(self.type_str)).replace(
                    "struct", "")
            logging.debug("member %s needs %s", self.name, self.dep_struct)

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
        self.structure = None

        # convert to structure if all member data types are defined
        if all(x.dtype is not None for x in self.members):
            self.structure = self.to_structure()

    def __str__(self):
        res = [f"struct {self.name}: "]
        for member in self.members:
            res.append(str(member))

        res = res[0] + ", ".join(res[1:])
        return res

    def to_structure(self):
        """Convert struct to ctypes.Structure"""
        return type(self.name, (ctypes.Structure,),
                    {"_fields_": [member.to_tuple() for member in
                                  self.members]})


def extract_type_with_struct(type_str: str, dep_struct: Struct):
    """Extract ctypes data type from a string and the struct it depends on

    Parameters:
        type_str (str): C data type string
        required_struct (Struct): struct the type depends on
    """
    res = None

    for word in type_str:
        if word == dep_struct.name:
            res = dep_struct.structure

    return res
