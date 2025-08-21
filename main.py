import ctypes
from parse_struct import Struct
from compile import compile_prog


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
    structs = [Struct(key, val)
               for key, val in extract_structs("test_struct.c").items()]

    for struct in structs:
        # define ctypes.Structure containing the struct's members
        class TempStruct(ctypes.Structure):
            _fields_ = [member.to_tuple() for member in struct.members]

        # print the sizes of each of the members followed by the size of the
        # struct
        print(f"{[ctypes.sizeof(member.dtype) for member in struct.members]}"
              f" -> {ctypes.sizeof(TempStruct())}")


    '''
    print()
    compile_prog("test_struct.c")

    # print members, including sizes
    for key in structs.keys():
        print(f"{key}: ")
        for i in structs[key]:
            print(f"  {i} (= {ctypes.sizeof(extract_type(i))})")
            StructMember(i)
        print()
    '''
