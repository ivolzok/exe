import struct
class FileHeader:
    def __init__(self, machine, numberOfSections, timeDateStamp,
                 pointerToSymbolTable, numberOfSymbols, sizeOfOptionalHeader, characteristics):
        self.machine = machine
        self.numberOfSections = numberOfSections
        self.timeDataStamp = timeDateStamp
        self.pointerToSymbolTable = pointerToSymbolTable
        self.numberOfSymbols = numberOfSymbols
        self.sizeOfOptionalHeader = sizeOfOptionalHeader
        self.characteristics = characteristics

    @classmethod
    def from_bytes(cls, header):
        fields = struct.unpack('<HHIIIHH', header[:20])
        return cls(*fields)

