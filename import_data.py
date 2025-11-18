import struct


class ImportData:
    def __init__(self, original_first_thunk, time_date_stamp, forwarder_chain, name, first_thunk):
        self.original_first_thunk = original_first_thunk
        self.time_date_stamp = time_date_stamp
        self.forwarder_chain = forwarder_chain
        self.name = name
        self.first_thunk = first_thunk
        self.string_name = None

    @classmethod
    def from_bytes(cls, data):
        fields = struct.unpack('<IIIII', data)
        return ImportData(*fields)

    def add_string_name(self, pointer, file):
        start_pointer = file.tell()
        file.seek(pointer)
        name = b''
        while True:
            byte = file.read(1)
            if byte == b'\x00' or not byte:
                break
            name += byte
        file.seek(start_pointer)
        self.string_name = name.decode()

    def __str__(self):
        return f"""Import DLL:
    DLL Name:          {self.string_name}
    Original First Thunk:  0x{self.original_first_thunk:08X}
    Time Date Stamp:       0x{self.time_date_stamp:08X}
    Forwarder Chain:       0x{self.forwarder_chain:08X}
    First Thunk:           0x{self.first_thunk:08X}"""
