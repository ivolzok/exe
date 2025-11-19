import unittest
import struct
from data_directory import DataDirectory


class TestDataDirectory(unittest.TestCase):
    def test_add_row(self):
        directory = DataDirectory()

        directory.add_row(0x1000, 0x200)
        directory.add_row(0x2000, 0x300)

        self.assertEqual(len(directory.table), 2)
        self.assertEqual(directory.table[0], (0x1000, 0x200))
        self.assertEqual(directory.table[1], (0x2000, 0x300))

    def test_getitem(self):
        directory = DataDirectory()
        directory.add_row(0x1000, 0x200)
        directory.add_row(0x2000, 0x300)

        self.assertEqual(directory[0], (0x1000, 0x200))
        self.assertEqual(directory[1], (0x2000, 0x300))

    def test_from_bytes_empty_data(self):
        directory = DataDirectory.from_bytes(b'')
        self.assertEqual(len(directory.table), 0)

    def test_from_bytes_single_entry(self):
        data = struct.pack('<II', 0x1000, 0x200)

        directory = DataDirectory.from_bytes(data)

        self.assertEqual(len(directory.table), 1)
        self.assertEqual(directory.table[0], (0x1000, 0x200))

    def test_from_bytes_multiple_entries(self):
        data = struct.pack('<IIII', 0x1000, 0x200, 0x2000, 0x300)

        directory = DataDirectory.from_bytes(data)

        self.assertEqual(len(directory.table), 2)
        self.assertEqual(directory.table[0], (0x1000, 0x200))
        self.assertEqual(directory.table[1], (0x2000, 0x300))
