import ctypes
import logging
from parse_struct import Struct, extract_type_with_struct
# from compile import compile_prog


# TODO docstrings

def extract_structs(filename: str):
    structs = {}

    src = open(filename, 'r')
    data = src.readlines()
    src.close()

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

        structs[name] = []

        line_num += 1
        structs[name] = parse_struct()
        # print(f"parsed struct {name}, line_num = {line_num}")

        line_num += 1

    return structs


if __name__ == "__main__":
    # set up logging
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)  # set log level for main

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
        print()
