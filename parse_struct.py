import ctypes
from pydoc import locate

ASTERISK = "*"


def extract_type(member: str):
    # locate data type from name
    base_type = locate(f"ctypes.c_{member.split()[0]}")

    # TODO handle:
    # structs within structs
    # double pointers

    if ASTERISK in member:
        # return a pointer to the specified type
        return ctypes.POINTER(base_type)
    return base_type


class StructMember:
    def __init__(self, member_str):
        self.name = member_str.split(" ")[-1].strip(";")
        self.type_str = member_str.split(" ")[:-1]

        # pointer found (* attached to variable name)
        if ASTERISK in self.name:
            self.type_str.append(ASTERISK)
        if any([ASTERISK in x for x in self.type_str]):
            # strip asterisk from data types
            self.type_str = [x.replace(ASTERISK, "") for x in self.type_str]
            # add data type to signify pointer
            self.type_str.append(ASTERISK)

        # filter to remove empty space
        self.type_str = list(filter(None, self.type_str))
        # remove asterisks stuck to member name
        self.name = self.name.replace("*", "")

        self.dtype = extract_type(" ".join(self.type_str))
        '''
        print(f"name: {self.name}, type_str: {self.type_str}, dtype: "
              f"{self.dtype}")
        '''

    def __str__(self):
        return f"{self.name} ({" ".join(self.type_str)})"


class Struct:
    def __init__(self, name, members):
        self.name = name
        self.members = [StructMember(x) for x in members]

    def __str__(self):
        res = [f"struct {self.name}: "]
        for member in self.members:
            res.append(str(member))

        res = res[0] + ", ".join(res[1:])
        return res
