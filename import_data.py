import struct
from thunk_data import ThunkDataName, ThunkDataOrdinal


class ImportData:
    def __init__(self, original_first_thunk, time_date_stamp, forwarder_chain, name, first_thunk):
        self.original_first_thunk = original_first_thunk
        self.time_date_stamp = time_date_stamp
        self.forwarder_chain = forwarder_chain
        self.name = name
        self.first_thunk = first_thunk
        self.string_name = None
        self.thunks = []

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

    def add_thunks(self, offset, file, magic):
        first_thunk = self.first_thunk if self.first_thunk != 0 else self.original_first_thunk
        start_pointer = file.tell()
        file.seek(offset + first_thunk)
        data_length = 4 if magic == 0x010B else 8
        while True:
            data = file.read(data_length)
            if data == b'\x00' * data_length:
                break
            if magic == 0x010B:
                data = struct.unpack('<I', data)[0]
                if data & 0x80000000:
                    data = ThunkDataOrdinal.from_int(data)
                else:
                    data = ThunkDataName.from_int(data)
                    data.add_name_and_hint(offset, file)
            else:
                data = struct.unpack('<Q', data)[0]
                if data & 0x8000000000000000:
                    data = ThunkDataOrdinal.from_int(data)
                else:
                    data = ThunkDataName.from_int(data)
                    data.add_name_and_hint(offset, file)
            self.thunks.append(data)

        file.seek(start_pointer)

    def __str__(self):
        return f"""Import DLL:
DLL Name:          {self.string_name}
Original First Thunk:  0x{self.original_first_thunk:08X}
Time Date Stamp:       0x{self.time_date_stamp:08X}
Forwarder Chain:       0x{self.forwarder_chain:08X}
First Thunk:           0x{self.first_thunk:08X}
Functions:             
{'\n'.join(map(str, self.thunks))}"""
