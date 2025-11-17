import struct

class Section:
    def __init__(self, name, virtual_size, virtual_address, size_of_row_data,
                 pointer_to_raw_data, pointer_to_relocations, pointer_to_line_numbers,
                 number_of_relocations, number_of_line_numbers, characteristics):
        self.name = name
        self.virtual_size = virtual_size
        self.virtual_address = virtual_address
        self.size_of_row_data = size_of_row_data
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

