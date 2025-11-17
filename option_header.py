import struct
class OptionHeader:
    magic_types = {
        0x010B: "PE32",
        0x020B: "PE32+ (64-bit)",
    }

    subsystems = {
        0: "Unknown",
        1: "Native",
        2: "Windows GUI",
        3: "Windows CUI",
        5: "OS/2 CUI",
        7: "POSIX CUI",
        9: "Windows CE GUI",
        10: "EFI Application",
        11: "EFI Boot Service",
        12: "EFI Runtime Service",
        13: "EFI ROM",
        14: "XBOX",
        16: "Windows Boot Application"
    }

    dll_characteristics_dict = {
        0x0020: "HIGH_ENTROPY_VA",
        0x0040: "DYNAMIC_BASE",
        0x0080: "FORCE_INTEGRITY",
        0x0100: "NX_COMPAT",
        0x0200: "NO_ISOLATION",
        0x0400: "NO_SEH",
        0x0800: "NO_BIND",
        0x1000: "APPCONTAINER",
        0x2000: "WDM_DRIVER",
        0x4000: "GUARD_CF",
        0x8000: "TERMINAL_SERVER_AWARE"
    }

    def __init__(
            self,
            magic,
            major_linker_version,
            minor_linker_version,
            size_of_code,
            size_of_initialized_data,
            size_of_uninitialized_data,
            address_of_entry_point,
            base_of_code,
            image_base,
            section_alignment,
            file_alignment,
            major_os_version,
            minor_os_version,
            major_image_version,
            minor_image_version,
            major_subsystem_version,
            minor_subsystem_version,
            win32_version,
            size_of_image,
            size_of_headers,
            check_sum,
            subsystem,
            dll_characteristics,
            size_of_stack_reserve,
            size_of_stack_commit,
            size_of_heap_reserve,
            size_of_heap_commit,
            loader_flags,
            number_of_rva_and_sizes,
    ):
        self.magic = magic
        self.major_linker_version = major_linker_version
        self.minor_linker_version = minor_linker_version
        self.size_of_code = size_of_code
        self.size_of_initialized_data = size_of_initialized_data
        self.size_of_uninitialized_data = size_of_uninitialized_data
        self.address_of_entry_point = address_of_entry_point
        self.base_of_code = base_of_code
        self.image_base = image_base
        self.section_alignment = section_alignment
        self.file_alignment = file_alignment
        self.major_os_version = major_os_version
        self.minor_os_version = minor_os_version
        self.major_image_version = major_image_version
        self.minor_image_version = minor_image_version
        self.major_subsystem_version = major_subsystem_version
        self.minor_subsystem_version = minor_subsystem_version
        self.win32_version_value = win32_version
        self.size_of_image = size_of_image
        self.size_of_headers = size_of_headers
        self.check_sum = check_sum
        self.subsystem = subsystem
        self.dll_characteristics = dll_characteristics
        self.size_of_stack_reserve = size_of_stack_reserve
        self.size_of_stack_commit = size_of_stack_commit
        self.size_of_heap_reserve = size_of_heap_reserve
        self.size_of_heap_commit = size_of_heap_commit
        self.loader_flags = loader_flags
        self.number_of_rva_and_sizes = number_of_rva_and_sizes

    def get_dll_characteristics_list(self):
        characteristics = []
        for key, value in self.dll_characteristics_dict.items():
            if self.dll_characteristics & key == key:
                characteristics.append(value)
        return characteristics

    def __str__(self):
        characteristics_string = ', '.join(self.get_dll_characteristics_list())
        return f"""Optional Header:
        Magic: {self.magic_types.get(self.magic)} (0x{self.magic:04X})
        Linker Version: {self.major_linker_version}.{self.minor_linker_version}
        Code Size: {self.size_of_code} bytes
        Initialized Data Size: {self.size_of_initialized_data} bytes
        Uninitialized Data Size: {self.size_of_uninitialized_data} bytes
        Entry Point: 0x{self.address_of_entry_point:08X}
        Base of Code: 0x{self.base_of_code:08X}
        Image Base: 0x{self.image_base:016X}
        Section Alignment: {self.section_alignment} bytes
        File Alignment: {self.file_alignment} bytes
        OS Version: {self.major_os_version}.{self.minor_os_version}
        Image Version: {self.major_image_version}.{self.minor_image_version}
        Subsystem Version: {self.major_subsystem_version}.{self.minor_subsystem_version}
        Win32 Version: {self.win32_version_value}
        Image Size: {self.size_of_image} bytes
        Headers Size: {self.size_of_headers} bytes
        Checksum: 0x{self.check_sum:08X}
        Subsystem: {self.subsystems.get(self.subsystem)} (0x{self.subsystem:04X})
        DLL Characteristics: {characteristics_string} (0x{self.dll_characteristics:04X})
        Stack Reserve: {self.size_of_stack_reserve} bytes
        Stack Commit: {self.size_of_stack_commit} bytes
        Heap Reserve: {self.size_of_heap_reserve} bytes
        Heap Commit: {self.size_of_heap_commit} bytes
        Loader Flags: 0x{self.loader_flags:08X}
        Number of RVA and Sizes: {self.number_of_rva_and_sizes}"""

class OptionHeader32(OptionHeader):
    def __init__(self, base_of_data, *args):
        self.base_of_data = base_of_data
        super().__init__(*args)

    @classmethod
    def from_bytes(cls, data):
        fields = list(struct.unpack('<BBIIIIIIIIIHHHHHHIIIIHHIIIIII', data))
        base_of_data = fields.pop(7)
        return OptionHeader32(base_of_data, 267, *fields)

    def __str__(self):
        return f"""{super().__str__()}
    Base of Data: 0x{self.base_of_data:08X}"""

class OptionHeader64(OptionHeader):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return super().__str__()

    @classmethod
    def from_bytes(cls, data):
        fields = list(struct.unpack('<BBIIIIIQIIHHHHHHIIIIHHQQQQII', data))
        return OptionHeader64(523, *fields)