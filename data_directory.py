import struct


class DataDirectory:
    directory_names = [
        "Export", "Import", "Resource", "Exception",
        "Certificate", "Relocation", "Debug", "Architecture",
        "Global Ptr", "TLS", "Load Config", "Bound Import",
        "IAT", "Delay Import", "CLR", "Reserved"
    ]
    def __init__(self):
        self.table = []

    def add_row(self, virtual_address, size):
        self.table.append((virtual_address, size))

    def __getitem__(self, index):
        return self.table[index]

    @classmethod
    def from_bytes(cls, data):
        directory = DataDirectory()
        for i in range(0, len(data), 8):
            virtual_address, size = struct.unpack('<II', data[i:i+8])
            directory.add_row(virtual_address, size)
        return directory

    def __str__(self):
        result = "Data Directories:\n"
        for i, (va, size) in enumerate(self.table):
            if i < len(self.directory_names):
                name = self.directory_names[i]
            else:
                name = f"Directory {i}"
            result += f"  {name}: Virtual Address = 0x{va:08X}, Size = 0x{size:08X}\n"
        return result