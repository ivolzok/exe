import unittest
import struct
from file_header import FileHeader


class TestFileHeader(unittest.TestCase):
    def test_from_bytes(self):
        test_data = struct.pack(
            '<HHIIIHH',
            0x8664,
            3,
            1633046400,
            0x2000,
            100,
            240,
            0x2102
        )

        header = FileHeader.from_bytes(test_data)

        self.assertEqual(header.machine, 0x8664)
        self.assertEqual(header.number_of_sections, 3)
        self.assertEqual(header.time_date_stamp, 1633046400)
        self.assertEqual(header.pointer_to_symbol_table, 0x2000)
        self.assertEqual(header.number_of_symbols, 100)
        self.assertEqual(header.size_of_optional_header, 240)
        self.assertEqual(header.characteristics, 0x2102)

    def test_get_characteristics_list_single_flag(self):
        header = FileHeader(0x014C, 1, 0,
                            0, 0, 0, 0x0002)

        characteristics = header.get_characteristics_list()

        self.assertEqual(len(characteristics), 1)
        self.assertIn("IMAGE_FILE_EXECUTABLE_IMAGE", characteristics)

    def test_get_characteristics_list_multiple_flags(self):
        header = FileHeader(0x014C, 1, 0,
                            0, 0, 0, 0x2102)

        characteristics = header.get_characteristics_list()

        self.assertGreater(len(characteristics), 1)
        self.assertIn("IMAGE_FILE_EXECUTABLE_IMAGE", characteristics)
        self.assertIn("IMAGE_FILE_DLL", characteristics)
        self.assertIn("IMAGE_FILE_32BIT_MACHINE", characteristics)

    def test_get_characteristics_list_no_flags(self):
        header = FileHeader(0x014C, 1, 0,
                            0, 0, 0, 0x0000)

        characteristics = header.get_characteristics_list()

        self.assertEqual(len(characteristics), 0)
        self.assertEqual(characteristics, [])

    def test_get_characteristics_list_unknown_flags(self):
        header = FileHeader(0x014C, 1, 0, 0,
                            0, 0, 0x8000)

        characteristics = header.get_characteristics_list()

        self.assertEqual(len(characteristics), 0)
