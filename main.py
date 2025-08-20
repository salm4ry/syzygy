from parse_struct import Struct


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

    for x in structs:
        print(x)

    '''
    # print members, including sizes
    for key in structs.keys():
        print(f"{key}: ")
        for i in structs[key]:
            print(f"  {i} (= {ctypes.sizeof(extract_type(i))})")
            StructMember(i)
        print()
    '''
