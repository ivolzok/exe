import struct

class OptionHeader:
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