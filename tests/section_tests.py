import unittest
import struct
from section import Section


class TestSection(unittest.TestCase):
    def test_from_bytes(self):
        test_data = struct.pack(
            '<8sIIIIIIHHI',
            b'.data\x00\x00\x00',  # name
            0x800,  # virtual_size
            0x2000,  # virtual_address
            0x1000,  # size_of_raw_data
            0x800,  # pointer_to_raw_data
            0x0,  # pointer_to_relocations
            0x0,  # pointer_to_line_numbers
            0,  # number_of_relocations
            0,  # number_of_line_numbers
            0xC0000040  # characteristics
        )

        section = Section.from_bytes(test_data)

        self.assertEqual(section.name, b'.data\x00\x00\x00')
        self.assertEqual(section.virtual_size, 0x800)
        self.assertEqual(section.virtual_address, 0x2000)
        self.assertEqual(section.size_of_raw_data, 0x1000)
        self.assertEqual(section.pointer_to_raw_data, 0x800)
        self.assertEqual(section.characteristics, 0xC0000040)

    def test_get_characteristics_list_single_flag(self):
        section = Section(b'.text\x00\x00\x00', 0, 0, 0, 0,
                          0, 0, 0, 0,
                          0x00000020)  # CODE

        characteristics = section.get_characteristics_list()

        self.assertEqual(len(characteristics), 1)
        self.assertIn("CODE", characteristics)

    def test_get_characteristics_list_multiple_flags(self):
        section = Section(b'.text\x00\x00\x00', 0, 0, 0, 0,
                          0, 0, 0,
                          0, 0x60000020)

        characteristics = section.get_characteristics_list()

        self.assertGreater(len(characteristics), 1)
        self.assertIn("CODE", characteristics)
        self.assertIn("MEM_EXECUTE", characteristics)
        self.assertIn("MEM_READ", characteristics)

    def test_get_characteristics_list_alignment_flags(self):
        section = Section(b'.text\x00\x00\x00', 0, 0, 0, 0,
                          0, 0, 0, 0,
                          0x00500020)

        characteristics = section.get_characteristics_list()

        self.assertIn("CODE", characteristics)
        self.assertIn("ALIGN_16BYTES", characteristics)

    def test_get_characteristics_list_no_flags(self):
        section = Section(b'.text\x00\x00\x00', 0, 0, 0, 0,
                          0, 0, 0, 0,
                          0x00000000)

        characteristics = section.get_characteristics_list()

        self.assertEqual(len(characteristics), 0)
        self.assertEqual(characteristics, [])

    def test_get_characteristics_list_combined_flags(self):
        section = Section(b'.data\x00\x00\x00', 0, 0, 0, 0,
                          0, 0, 0, 0,
                          0xC0000040)

        characteristics = section.get_characteristics_list()

        self.assertIn("INITIALIZED_DATA", characteristics)
        self.assertIn("MEM_READ", characteristics)
        self.assertIn("MEM_WRITE", characteristics)
