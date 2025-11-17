import struct


class DataDirectory:
    def __init__(self):
        self.table = []

    def add_row(self, virtual_address, size):
        self.table.append((virtual_address, size))

    def __getitem__(self, index):
        return self.table[index]

    @classmethod
    def from_bytes(cls, data):
        if len(data) % 8 != 0:
            raise ValueError("данные должны делиться на 8")
        directory = DataDirectory()
        for i in range(0, len(data), 8):
            virtual_address, size = struct.unpack('<II', data[i:i+8])
            directory.add_row(virtual_address, size)
        return directory