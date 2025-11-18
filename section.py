import struct


class Section:
    characteristics_dict = {
        0x00000020: "CODE",
        0x00000040: "INITIALIZED_DATA",
        0x00000080: "UNINITIALIZED_DATA",
        0x00000001: "TYPE_NO_PAD",
        0x00000008: "LNK_INFO",
        0x00000200: "LNK_REMOVE",
        0x00000800: "LNK_COMDAT",
        0x00001000: "GPREL",
        0x00008000: "MEM_PURGEABLE",
        0x00010000: "MEM_16BIT",
        0x00020000: "MEM_LOCKED",
        0x00040000: "MEM_PRELOAD",
        0x00100000: "ALIGN_1BYTES",
        0x00200000: "ALIGN_2BYTES",
        0x00300000: "ALIGN_4BYTES",
        0x00400000: "ALIGN_8BYTES",
        0x00500000: "ALIGN_16BYTES",
        0x00600000: "ALIGN_32BYTES",
        0x00700000: "ALIGN_64BYTES",
        0x00800000: "ALIGN_128BYTES",
        0x00900000: "ALIGN_256BYTES",
        0x00A00000: "ALIGN_512BYTES",
        0x00B00000: "ALIGN_1024BYTES",
        0x00C00000: "ALIGN_2048BYTES",
        0x00D00000: "ALIGN_4096BYTES",
        0x00E00000: "ALIGN_8192BYTES",
        0x01000000: "LNK_NRELOC_OVFL",
        0x02000000: "MEM_DISCARDABLE",
        0x04000000: "MEM_NOT_CACHED",
        0x08000000: "MEM_NOT_PAGED",
        0x10000000: "MEM_SHARED",
        0x20000000: "MEM_EXECUTE",
        0x40000000: "MEM_READ",
        0x80000000: "MEM_WRITE"
    }

    def __init__(self, name, virtual_size, virtual_address, size_of_raw_data,
                 pointer_to_raw_data, pointer_to_relocations, pointer_to_line_numbers,
                 number_of_relocations, number_of_line_numbers, characteristics):
        self.name = name
        self.virtual_size = virtual_size
        self.virtual_address = virtual_address
        self.size_of_raw_data = size_of_raw_data
        self.pointer_to_raw_data = pointer_to_raw_data
        self.pointer_to_relocations = pointer_to_relocations
        self.pointer_to_line_numbers = pointer_to_line_numbers
        self.number_of_relocations = number_of_relocations
        self.number_of_line_numbers = number_of_line_numbers
        self.characteristics = characteristics

    @classmethod
    def from_bytes(cls, data):
        fields = struct.unpack('<8sIIIIIIHHI', data)
        return Section(*fields)

    def get_characteristics_list(self):
        characteristics = []
        for key, value in self.characteristics_dict.items():
            if self.characteristics & key == key:
                characteristics.append(value)
        return characteristics

    def __str__(self):
        characteristics_str = ', '.join(self.get_characteristics_list())
        return f"""Section: {self.name.decode().rstrip('\x00')}
          Virtual Size:          0x{self.virtual_size:08X} ({self.virtual_size})
          Virtual Address:       0x{self.virtual_address:08X}
          Raw Data Size:         0x{self.size_of_raw_data:08X} ({self.size_of_raw_data})
          Raw Data Pointer:      0x{self.pointer_to_raw_data:08X}
          Relocations Pointer:   0x{self.pointer_to_relocations:08X}
          Line Numbers Pointer:  0x{self.pointer_to_line_numbers:08X}
          Number of Relocations: {self.number_of_relocations}
          Number of Line Numbers: {self.number_of_line_numbers}
          Characteristics:       {characteristics_str} (0x{self.characteristics:08X})"""
