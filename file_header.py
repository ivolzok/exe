import struct
from datetime import datetime


class FileHeader:
    machine_types_dict = {
        0x014C: "IMAGE_FILE_MACHINE_I386 (Intel 386)",
        0x8664: "IMAGE_FILE_MACHINE_AMD64 (x64)",
        0x01C0: "IMAGE_FILE_MACHINE_ARM (ARM LE)",
        0xAA64: "IMAGE_FILE_MACHINE_ARM64 (ARM64 LE)",
        0x014D: "IMAGE_FILE_MACHINE_I486 (Intel 486)",
        0x014E: "IMAGE_FILE_MACHINE_PENTIUM (Intel Pentium)",
        0x0200: "IMAGE_FILE_MACHINE_IA64 (Intel Itanium)",
        0x0EBC: "IMAGE_FILE_MACHINE_EBC (EFI Byte Code)",
    }

    characteristics_dict = {
        0x0001: "IMAGE_FILE_RELOCS_STRIPPED",
        0x0002: "IMAGE_FILE_EXECUTABLE_IMAGE",
        0x0004: "IMAGE_FILE_LINE_NUMS_STRIPPED",
        0x0008: "IMAGE_FILE_LOCAL_SYMS_STRIPPED",
        0x0010: "IMAGE_FILE_AGGRESSIVE_WS_TRIM",
        0x0020: "IMAGE_FILE_LARGE_ADDRESS_AWARE",
        0x0080: "IMAGE_FILE_BYTES_REVERSED_LO",
        0x0100: "IMAGE_FILE_32BIT_MACHINE",
        0x0200: "IMAGE_FILE_DEBUG_STRIPPED",
        0x0400: "IMAGE_FILE_REMOVABLE_RUN_FROM_SWAP",
        0x0800: "IMAGE_FILE_NET_RUN_FROM_SWAP",
        0x1000: "IMAGE_FILE_SYSTEM",
        0x2000: "IMAGE_FILE_DLL",
        0x4000: "IMAGE_FILE_UP_SYSTEM_ONLY",
    }

    def __init__(
            self,
            machine,
            number_of_sections,
            time_date_stamp,
            pointer_to_symbol_table,
            number_of_symbols,
            size_of_optional_header,
            characteristics,
    ):
        self.machine = machine
        self.number_of_sections = number_of_sections
        self.time_date_stamp = time_date_stamp
        self.pointer_to_symbol_table = pointer_to_symbol_table
        self.number_of_symbols = number_of_symbols
        self.size_of_optional_header = size_of_optional_header
        self.characteristics = characteristics
        self.characteristics_list = self.get_characteristics_list()

    @classmethod
    def from_bytes(cls, data):
        fields = struct.unpack('<HHIIIHH', data)
        return cls(*fields)

    def get_characteristics_list(self):
        characteristics = []
        for key, value in self.characteristics_dict.items():
            if self.characteristics & key == key:
                characteristics.append(value)
        return characteristics

    def __str__(self):
        characteristics_str = ', '.join(self.characteristics_list)
        machine_str = self.characteristics_dict.get(self.machine)
        time = datetime.fromtimestamp(self.time_date_stamp).strftime('%Y-%m-%d %H:%M:%S')

        return f"""File Header:
    Machine: {machine_str} (0x{self.machine:04X})
    Number of Sections: {self.number_of_sections}
    Time Date Stamp: {self.time_date_stamp} ({time})
    Pointer to Symbol Table: 0x{self.pointer_to_symbol_table:08X}
    Number of Symbols: {self.number_of_symbols}
    Size of Optional Header: {self.size_of_optional_header} bytes
    Characteristics: {characteristics_str} (0x{self.characteristics:04X})"""
