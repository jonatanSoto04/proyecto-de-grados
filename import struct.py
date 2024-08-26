import struct

def check_dll_architecture(dll_path):
    with open(dll_path, 'rb') as file:
        file.seek(0x3C)
        pe_offset = struct.unpack('<I', file.read(4))[0]
        file.seek(pe_offset + 4)
        machine_type = struct.unpack('<H', file.read(2))[0]

        if machine_type == 0x8664:
            return "64-bit"
        elif machine_type == 0x14C:
            return "32-bit"
        else:
            return "Unknown architecture"

dll_path = r'C:\\Users\\User\\Documents\\proyectogrado\\Futronic\\SDK 4.2\\Bin\\ftrJSDK.dll'
print(f"The DLL is: {check_dll_architecture(dll_path)}")