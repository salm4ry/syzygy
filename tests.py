import unittest
import json
from pydoc import locate

import syzygy

"""
Python unittest documentation: https://docs.python.org/3/library/unittest.html
unittest Real Python guide: https://realpython.com/python-unittest/
"""


def get_outputs(input_file, output_file):
    # get expected output
    with open(output_file) as f:
        expected = json.load(f)

    # run syzygy on input to get real output
    real = syzygy.parse_structs_from_file(input_file)

    return (expected, real)


class TestBasicStructs(unittest.TestCase):
    """Test struct size, alignment, and layout"""

    def _test_case(self, input_file, output_file, num_structs):
        expected, real = get_outputs(input_file, output_file)

        for i in range(num_structs):
            expected_struct = expected["structs"][i]
            struct_json = real[i].to_json()

            self.assertEqual(struct_json["size"], expected_struct["size"])
            self.assertEqual(struct_json["alignment"],
                             expected_struct["alignment"])
            self.assertEqual(
                syzygy.visualise_struct(real[i]).strip(),
                expected_struct["layout"]
            )

    def test_int_struct(self):
        self._test_case(
                "tests/input/int_struct.c", "tests/output/int_struct.json", 1
        )

    def test_pointer_struct(self):
        self._test_case(
            "tests/input/pointer_struct.c",
            "tests/output/pointer_struct.json",
            2
        )

    def test_array_struct(self):
        self._test_case(
            "tests/input/array_struct.c", "tests/output/array_struct.json", 1
        )


class TestParsing(unittest.TestCase):
    """Test struct and member name and data type parsing"""

    def _test_case(self, input_file, output_file, num_structs):
        expected, real = get_outputs(input_file, output_file)

        for i in range(num_structs):
            expected_struct = expected["structs"][i]
            struct_json = real[i].to_json()
            real_members = real[i].members

            # struct name
            self.assertEqual(struct_json["name"], expected_struct["name"])

            # iterating by index allowed because member order should be
            # deterministic (i.e. the order they are defined in the struct)
            for j in range(len(expected_struct["members"])):
                # compare names
                self.assertEqual(
                    real_members[j].name, expected_struct["members"][j]["name"]
                )
                # compare ctypes data types to check parsing
                self.assertEqual(
                    real_members[j].dtype,
                    locate("ctypes." + expected_struct["members"][j]["dtype"]),
                )

        return expected, real

    def test_basic_types(self):
        """Test names and ctypes data types"""
        self._test_case("tests/input/basic_types.c",
                        "tests/output/basic_types.json", 6)

    def test_arrays(self):
        expected, real = self._test_case("tests/input/array_struct.c",
                                         "tests/output/array_types.json", 1)

        # test array lengths
        expected_members = expected["structs"][0]["members"]
        real_members = real[0].members
        for i in range(len(expected_members)):
            self.assertEqual(real_members[i].length,
                             expected_members[i]["length"])


if __name__ == "__main__":
    unittest.main()
