import unittest
import struct
from option_header import OptionHeader, OptionHeader32, OptionHeader64


class TestOptionHeader(unittest.TestCase):
    def test_get_dll_characteristics_list_single_flag(self):
        header = OptionHeader(0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0,
                              0, 0, 0, 0x0040, 0,
                              0, 0, 0, 0,
                              0)

        characteristics = header.get_dll_characteristics_list()

        self.assertEqual(len(characteristics), 1)
        self.assertIn("DYNAMIC_BASE", characteristics)

    def test_get_dll_characteristics_list_multiple_flags(self):
        header = OptionHeader(0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0,
                              0, 0, 0, 0x0140, 0,
                              0, 0, 0, 0,
                              0)

        characteristics = header.get_dll_characteristics_list()

        self.assertGreater(len(characteristics), 1)
        self.assertIn("DYNAMIC_BASE", characteristics)
        self.assertIn("NX_COMPAT", characteristics)

    def test_get_dll_characteristics_list_no_flags(self):
        header = OptionHeader(0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0)

        characteristics = header.get_dll_characteristics_list()

        self.assertEqual(len(characteristics), 0)
        self.assertEqual(characteristics, [])


class TestOptionHeader32(unittest.TestCase):
    def test_from_bytes(self):
        test_data = struct.pack(
            '<BBIIIIIIIIIHHHHHHIIIIHHIIIIII',
            2,  # major_linker_version
            30,  # minor_linker_version
            4096,  # size_of_code
            8192,  # size_of_initialized_data
            1024,  # size_of_uninitialized_data
            0x1000,  # address_of_entry_point
            0x1000,  # base_of_code
            0x3000,  # base_of_data
            0x400000,  # image_base
            4096,  # section_alignment
            512,  # file_alignment
            6, 0,  # major/minor os version
            1, 0,  # major/minor image version
            6, 0,  # major/minor subsystem version
            0,  # win32_version
            0x10000,  # size_of_image
            1024,  # size_of_headers
            0x12345678,  # check_sum
            2,  # subsystem
            0x8140,  # dll_characteristics
            0x100000,  # size_of_stack_reserve
            0x1000,  # size_of_stack_commit
            0x100000,  # size_of_heap_reserve
            0x1000,  # size_of_heap_commit
            0,  # loader_flags
            16  # number_of_rva_and_sizes
        )

        header = OptionHeader32.from_bytes(test_data)

        self.assertEqual(header.base_of_data, 0x3000)
        self.assertEqual(header.magic, 0x010B)
        self.assertEqual(header.major_linker_version, 2)
        self.assertEqual(header.size_of_code, 4096)
        self.assertEqual(header.image_base, 0x400000)


class TestOptionHeader64(unittest.TestCase):
    def test_from_bytes(self):
        test_data = struct.pack(
            '<BBIIIIIQIIHHHHHHIIIIHHQQQQII',
            2,  # major_linker_version
            30,  # minor_linker_version
            4096,  # size_of_code
            8192,  # size_of_initialized_data
            1024,  # size_of_uninitialized_data
            0x1000,  # address_of_entry_point
            0x1000,  # base_of_code
            0x140000000,  # image_base (64-bit)
            4096,  # section_alignment
            512,  # file_alignment
            6, 0,  # major/minor os version
            1, 0,  # major/minor image version
            6, 0,  # major/minor subsystem version
            0,  # win32_version
            0x10000,  # size_of_image
            1024,  # size_of_headers
            0x12345678,  # check_sum
            2,  # subsystem
            0x8140,  # dll_characteristics
            0x100000,  # size_of_stack_reserve
            0x1000,  # size_of_stack_commit
            0x100000,  # size_of_heap_reserve
            0x1000,  # size_of_heap_commit
            0,  # loader_flags
            16  # number_of_rva_and_sizes
        )

        header = OptionHeader64.from_bytes(test_data)

        self.assertEqual(header.magic, 0x020B)
        self.assertEqual(header.major_linker_version, 2)
        self.assertEqual(header.size_of_code, 4096)
        self.assertEqual(header.image_base, 0x140000000)
