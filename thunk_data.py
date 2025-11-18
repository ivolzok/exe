import abc
import struct


class ThunkData:
    def __init__(self, data_address):
        self.data_address = data_address

    @classmethod
    @abc.abstractmethod
    def from_int(cls, data):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass


class ThunkDataOrdinal(ThunkData):
    def __init__(self, ordinal):
        super().__init__(ordinal)

    @classmethod
    def from_int(cls, data):
        return ThunkDataOrdinal(data & 0xFFFF)

    def __str__(self):
        return f"Ordinal {self.data_address} (0x{self.data_address:X})"


class ThunkDataName(ThunkData):
    def __init__(self, name_rva):
        super().__init__(name_rva)
        self.name = None
        self.hint = None

    @classmethod
    def from_int(cls, data):
        return ThunkDataName(data)

    def add_name_and_hint(self, offset, file):
        start_pointer = file.tell()
        file.seek(offset + self.data_address)
        self.hint = struct.unpack('<H', file.read(2))[0]
        name = b''
        while True:
            byte = file.read(1)
            if byte == b'\x00' or not byte:
                break
            name += byte
        file.seek(start_pointer)
        self.name = name.decode()

    def __str__(self):
        return f"{self.name} (Hint: {self.hint})"
