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

    def parse_struct():
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
        struct_dict[name] = parse_struct()
        logger.debug("parsed struct %s, line_num = %d",
                     name, line_num)

        line_num += 1

    return struct_dict


def visualise_struct(struct: Struct):
    """Visualise struct member alignment

        --- = filled bytes
        xxx = unused bytes
    """
    alignment = ctypes.alignment(struct.structure)

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
    # TODO tidy up struct parsing from file into more functions
    # -> maybe a class for a given file?
    # would allow struct dependencies to be handled automatically instead of in
    # main()

    structs = [Struct(key, val)
               for key, val in extract_structs("test_struct.c").items()]
    struct_classes = []

    for struct in structs:
        if struct.structure is not None:
            struct_classes.append(struct.structure)
        else:
            for member in struct.members:
                if member.dtype is None:
                    # find required struct
                    required_struct = [x for x in structs if x.name ==
                                       member.dep_struct][0]

                    logger.debug("%s.%s: found %s", struct.name, member.name,
                                 required_struct)

                    member.dtype = extract_type_with_struct(member.type_str,
                                                            required_struct)

                    logger.debug("%s.%s has type %s", struct.name, member.name,
                                 member.dtype)

            struct.structure = struct.to_structure()
            struct_classes.append(struct.structure)

    # print structs, members, and their sizes
    for struct in structs:
        print(f"{struct.name}: "
              f"{[ctypes.sizeof(member.dtype) for member in struct.members]}"
              f" -> {ctypes.sizeof(struct.structure)}, "
              f"alignment {ctypes.alignment(struct.structure)}")
        for member in struct.members:
            print(f"    {member} -> {member.dtype} "
                  f"({ctypes.sizeof(member.dtype)})")

        visualise_struct(struct)
        print()
