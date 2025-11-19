import struct
from file_header import FileHeader
from option_header import OptionHeader, OptionHeader32, OptionHeader64
from data_directory import DataDirectory
from section import Section
from import_table import ImportTable


class PEFile:
    def __init__(self, signature, file_header: FileHeader,
                 option_header: OptionHeader, data_directory: DataDirectory,
                 sections: dict[str, Section], imports: list[ImportTable]):
        self.signature = signature
        self.file_header = file_header
        self.option_header = option_header
        self.data_directory = data_directory
        self.sections = sections
        self.imports = imports

    @classmethod
    def from_file(cls, file):
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

        imports = []
        if len(data_directory.table) >= 2:
            import_rva = data_directory[1][0]
            for section in sections.values():
                if section.virtual_address <= import_rva < section.virtual_address + section.size_of_raw_data:
                    offset = section.pointer_to_raw_data - section.virtual_address
                    file.seek(offset + import_rva)
                    while True:
                        import_data = file.read(20)
                        if import_data == b'\x00' * 20:
                            break
                        import_data = ImportTable.from_bytes(import_data)
                        import_data.add_string_name(offset + import_data.name, file)
                        import_data.add_thunks(offset, file, optional_header.magic)
                        imports.append(import_data)
                    break

        return PEFile(signature, file_header, optional_header, data_directory, sections, imports)

    def __str__(self):
        parts = [str(self.file_header), str(self.option_header), str(self.data_directory)]
        for section in self.sections.values():
            parts.append(str(section))
        for dll in self.imports:
            parts.append(str(dll))
        return '\n\n'.join(parts)
