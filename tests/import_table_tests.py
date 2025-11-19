import unittest
import struct
from import_table import ImportTable


class TestImportTableFromBytes(unittest.TestCase):

    def test_from_bytes_normal_case(self):
        test_data = struct.pack(
            '<IIIII',
            0x1000,  # original_first_thunk
            0x12345678,  # time_date_stamp
            0x2000,  # forwarder_chain
            0x3000,  # name
            0x4000  # first_thunk
        )

        table = ImportTable.from_bytes(test_data)

        self.assertEqual(table.original_first_thunk, 0x1000)
        self.assertEqual(table.time_date_stamp, 0x12345678)
        self.assertEqual(table.forwarder_chain, 0x2000)
        self.assertEqual(table.name, 0x3000)
        self.assertEqual(table.first_thunk, 0x4000)
        self.assertIsNone(table.string_name)
        self.assertEqual(table.thunks, [])
