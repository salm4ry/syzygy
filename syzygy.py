"""Main syzygy code:

Parse a C file's structs and output size and alignment information
"""

import ctypes
import logging
import sys
import argparse

from parse_struct import Struct, extract_type_with_struct
from compile import compile_prog
from args import init_arg_parser

# set up logging
logging.basicConfig()
logger = logging.getLogger(__name__)


def extract_structs(data: str):
    """Extract struct text from a C string (array of file lines)

    Return:
        struct_dict (dict): struct name:members dictionary
    """
    struct_dict = {}

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


def fix_struct_deps(struct_list):
    for struct in struct_list:
        # handle structs with members that depend on other structs
        # i.e. one or more of its members have type == None
        if struct.dtype is None:
            for member in struct.members:
                if member.dtype is None:
                    logger.debug("looking for %s", member.dep_struct)
                    # find struct dependency (first match)
                    try:
                        dep_struct = next(x for x in struct_list if x.name ==
                                          member.dep_struct)
                    except StopIteration:
                        break

                    logger.debug("%s.%s: found %s", struct.name, member.name,
                                 dep_struct)

                    # set member data type and size
                    member.dtype = extract_type_with_struct(member.type_str,
                                                            dep_struct,
                                                            member.length)
                    member.size = ctypes.sizeof(member.dtype) * member.length

                    logger.debug("%s.%s has type %s", struct.name, member.name,
                                 member.dtype)

            # finally, get ctypes.Structure type, size, and alignment now
            # that all members are defined
            if all(member.dtype is not None for member in struct.members):
                struct.dtype = struct.to_structure()
            else:
                logger.error("could not set type for %s", struct.name)
                struct.dtype = None

    return struct_list


def parse_structs(data: str):
    struct_list = [Struct(key, val) for key, val in
                   extract_structs(data).items()]

    struct_list = fix_struct_deps(struct_list)

    return struct_list


def parse_structs_from_file(filename):
    """Extract and parse structs from a C file"""

    with open(filename, 'r', encoding="ascii") as f:
        data = f.readlines()

    return parse_structs(data)


def print_struct_with_sizes(struct: Struct):
    """Print struct size and sizes of its members"""
    print(f"{struct.name}: "
          f"{[member.size for member in struct.members]}"
          f" -> {ctypes.sizeof(struct.dtype)}, "
          f"alignment {ctypes.alignment(struct.dtype)}")
    for member in struct.members:
        print(f"    {member}, size {member.size}")


def visualise_struct(struct: Struct):
    """Visualise struct member alignment

    --- = filled bytes
    xxx = unused bytes

    Return struct visualisation string
    """
    res = ""
    struct_alignment = ctypes.alignment(struct.dtype)
    struct_size = ctypes.sizeof(struct.dtype)
    byte_pos = 0

    for member in struct.members:
        member_alignment = ctypes.alignment(member.dtype)
        member_size = ctypes.sizeof(member.dtype) * member.length
        padding = 0

        if byte_pos % member_alignment != 0:
            # calculate padding size
            padding = member_alignment - (byte_pos % member_alignment)
        res += "".join([padding * "x", "|", member_size * "-"])

        byte_pos += padding + member_size

    if byte_pos % struct_alignment != 0:
        padding = struct_alignment - (byte_pos % struct_alignment)
        res += padding * "x"
        byte_pos += padding
    res += "|\n"

    logger.debug("rendered %d bytes, expected %d", byte_pos, struct_size)
    assert byte_pos == struct_size
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    init_arg_parser(parser)
    args = parser.parse_args()

    # debug logging
    if args.debug:
        logger.setLevel(logging.DEBUG)  # set log level for main

    # compilation check
    if args.check:
        compiled_src = compile_prog(args.file)
        if compiled_src is None:
            # compilation failed, print an error and exit
            print("invalid code, cannot parse structs")
            sys.exit(1)

    structs = parse_structs_from_file(args.file)

    # print structs, members, and their sizes
    for entry in structs:
        print_struct_with_sizes(entry)
        print(visualise_struct(entry))
