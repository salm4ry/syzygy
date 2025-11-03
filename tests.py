import unittest
import json

import syzygy

"""
Python unittest documentation: https://docs.python.org/3/library/unittest.html
unittest Real Python guide: https://realpython.com/python-unittest/
"""


class TestBasicStructs(unittest.TestCase):
    """Test struct size, alignment, and layout"""

    def _test_case(self, input_file, output_file, num_structs):
        # TODO separate parts into generic function?
        # get output using input from input_file
        structs = syzygy.parse_structs_from_file(input_file)

        # compare to expected output in output_file
        with open(output_file) as f:
            expected = json.load(f)

        for i in range(num_structs):
            expected_struct = expected["structs"][i]
            struct_json = structs[i].to_json()

            self.assertEqual(struct_json["size"],
                             expected_struct["size"])
            self.assertEqual(struct_json["alignment"],
                             expected_struct["alignment"])
            self.assertEqual(syzygy.visualise_struct(structs[i]).strip(),
                             expected_struct["layout"])

    def test_int_struct(self):
        self._test_case("tests/input/int_struct.c",
                        "tests/output/int_struct.json", 1)

    def test_pointer_struct(self):
        self._test_case("tests/input/pointer_struct.c",
                        "tests/output/pointer_struct.json", 2)

    def test_array_struct(self):
        self._test_case("tests/input/array_struct.c",
                        "tests/output/array_struct.json", 1)


class TestParsing(unittest.TestCase):
    """Test struct and member name and data type parsing"""

    def _test_case(self, input_file, output_file, num_structs):
        # TODO separate parts into generic function?
        # get output using input from input_file
        structs = syzygy.parse_structs_from_file(input_file)

        # compare to expected output in output_file
        with open(output_file) as f:
            expected = json.load(f)

        for i in range(num_structs):
            expected_struct = expected["structs"][i]
            struct_json = structs[i].to_json()

            # struct name
            self.assertEqual(struct_json["name"], expected_struct["name"])

            for member in expected_struct["members"]:
                self.assertEqual(struct_json["members"][i], member)

    # TODO parsing test cases


if __name__ == "__main__":
    unittest.main()
