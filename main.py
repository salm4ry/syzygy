"""Main syzygy code:

Parse a C file's structs and output size and alignment information
"""

import ctypes
import logging
from parse_struct import Struct, extract_type_with_struct
# from compile import compile_prog

# set up logging
logging.basicConfig()
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # set log level for main


def extract_structs(filename: str):
    """Extract struct text from a C file

    Return:
        struct_dict (dict): struct name:members dictionary
    """
    struct_dict = {}
    data = None

    with open(filename, 'r', encoding="ascii") as src:
        data = src.readlines()

    line = ""
    line_num = 0

    def extract_members():
        """Extract struct members from a given position in a C file

        Nonlocal parameters:
            line: current file line
            line_num: current file line number
        """
        nonlocal line, line_num  # defined in the outer function
        struct_lines = []

        while "}" not in line and line_num < len(data):
            line = data[line_num]
            struct_lines.append(line.strip())
            line_num += 1

        # remove last element }
        return struct_lines[:-1]

    while line_num < len(data):
        line = data[line_num].strip()
        name = ""

        if line.startswith("struct"):
            name = line.split(" ")[1]
        elif line.startswith("typedef struct"):
            name = line.split(" ")[2]
        else:
            line_num += 1
            continue

        struct_dict[name] = []

        line_num += 1
        struct_dict[name] = extract_members()
        logger.debug("parsed struct %s, line_num = %d",
                     name, line_num)

        line_num += 1

    return struct_dict


def parse_structs_from_file(filename):
    """Extract and parse structs from a C file"""
    structs = [Struct(key, val) for key, val in
               extract_structs(filename).items()]

    for struct in structs:
        # handle structs with members that depend on other structs
        # i.e. one or more of its members have type == None
        if struct.dtype is None:
            for member in struct.members:
                if member.dtype is None:
                    # find struct dependency (first match)
                    dep_struct = next(x for x in structs if x.name ==
                                      member.dep_struct)

                    logger.debug("%s.%s: found %s", struct.name, member.name,
                                 dep_struct)

                    # set member data type
                    member.dtype = extract_type_with_struct(member.type_str,
                                                            dep_struct)

                    logger.debug("%s.%s has type %s", struct.name, member.name,
                                 member.dtype)

            # finally, get ctypes.Structure type for struct now that all
            # members are defined
            struct.dtype = struct.to_structure()

    return structs


def print_struct_with_sizes(struct: Struct):
    print(f"{struct.name}: "
          f"{[ctypes.sizeof(member.dtype) for member in struct.members]}"
          f" -> {ctypes.sizeof(struct.dtype)}, "
          f"alignment {ctypes.alignment(struct.dtype)}")
    for member in struct.members:
        print(f"    {member}, size {ctypes.sizeof(member.dtype)}")


def visualise_struct(struct: Struct):
    """Visualise struct member alignment

    --- = filled bytes
    xxx = unused bytes
    """
    alignment = ctypes.alignment(struct.dtype)

    print("|", end="")
    for member in struct.members:
        member_size = ctypes.sizeof(member.dtype)
        if member_size == alignment:
            print(member_size * "-", end="|")
        else:
            print("".join([member_size * "-",
                           (alignment - member_size) * "x"]),
                  end="|")
    print()


if __name__ == "__main__":
    structs = parse_structs_from_file("test_struct.c")

    # print structs, members, and their sizes
    for struct in structs:
        print_struct_with_sizes(struct)
        visualise_struct(struct)
        print()
