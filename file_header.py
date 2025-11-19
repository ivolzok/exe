import struct
from datetime import datetime


class FileHeader:
    machine_types_dict = {
        0x0: "Applicable to any machine type",
        0x184: "Alpha AXP, 32-bit address space",
        0x284: "Alpha 64, 64-bit address space",
        0x1D3: "Matsushita AM33",
        0x8664: "x64",
        0x1C0: "ARM little endian",
        0xAA64: "ARM64 little endian",
        0xA641: "ARM64EC — ABI for interoperability between ARM64 and emulated x64",
        0xA64E: "ARM64X — mixed ARM64 and ARM64EC code",
        0x1C4: "ARM Thumb-2 little endian",
        0xEBC: "EFI byte code",
        0x14C: "Intel 386 or later (x86)",
        0x200: "Intel Itanium (IA-64)",
        0x6232: "LoongArch 32-bit processor family",
        0x6264: "LoongArch 64-bit processor family",
        0x9041: "Mitsubishi M32R little endian",
        0x266: "MIPS16",
        0x366: "MIPS with FPU",
        0x466: "MIPS16 with FPU",
        0x1F0: "PowerPC little endian",
        0x1F1: "PowerPC with floating point support",
        0x160: "MIPS I compatible 32-bit big endian",
        0x162: "MIPS I compatible 32-bit little endian",
        0x166: "MIPS III compatible 64-bit little endian",
        0x168: "MIPS IV compatible 64-bit little endian",
        0x5032: "RISC-V 32-bit address space",
        0x5064: "RISC-V 64-bit address space",
        0x5128: "RISC-V 128-bit address space",
        0x1A2: "Hitachi SH3",
        0x1A3: "Hitachi SH3 DSP",
        0x1A6: "Hitachi SH4",
        0x1A8: "Hitachi SH5",
        0x1C2: "Thumb",
        0x169: "MIPS little-endian WCE v2",
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
        characteristics_str = ', '.join(self.get_characteristics_list())
        machine_str = self.machine_types_dict.get(self.machine)
        time = datetime.fromtimestamp(self.time_date_stamp).strftime('%Y-%m-%d %H:%M:%S')

        return f"""File Header:
    Machine: {machine_str} (0x{self.machine:04X})
    Number of Sections: {self.number_of_sections}
    Time Date Stamp: {self.time_date_stamp} ({time})
    Pointer to Symbol Table: 0x{self.pointer_to_symbol_table:08X}
    Number of Symbols: {self.number_of_symbols}
    Size of Optional Header: {self.size_of_optional_header} bytes
    Characteristics: {characteristics_str} (0x{self.characteristics:04X})"""
