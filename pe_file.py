import struct
from file_header import FileHeader
from option_header import OptionHeader, OptionHeader32, OptionHeader64
from data_directory import DataDirectory
from section import Section


class PEFile:
    def __init__(self, signature, file_header: FileHeader,
                 option_header: OptionHeader, data_directory: DataDirectory, sections: dict[str,Section]):
        self.signature = signature
        self.file_header = file_header
        self.option_header = option_header
        self.data_directory = data_directory
        self.sections = sections

    @classmethod
    def from_file(cls, file):
        # переходим к основной части файла
        file.seek(0x3C)
        e_lfanew = struct.unpack('<I', file.read(4))[0]
        file.seek(e_lfanew)

        signature = file.read(4)
        file_header = FileHeader.from_bytes(file.read(20))

        optional_header = None
        magic = struct.unpack('<H', file.read(2))[0]
        if magic == 267:
            optional_header = OptionHeader32.from_bytes(file.read(94))
        elif magic == 523:
            optional_header = OptionHeader64.from_bytes(file.read(110))

        data_directories_number = optional_header.number_of_rva_and_sizes
        data_directory = DataDirectory.from_bytes(file.read(8 * data_directories_number))

        sections = {}
        sections_num = file_header.number_of_sections
        for i in range(sections_num):
            section = Section.from_bytes(file.read(40))
            sections[section.name.decode().rstrip('\x00')] = section

        return PEFile(signature, file_header, optional_header, data_directory, sections)
