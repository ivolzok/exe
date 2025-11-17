import struct

class FileHeader:
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

