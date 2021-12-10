"""Windows kernel API wrapper
"""
import platform
from ctypes import Structure, c_void_p
from ctypes import windll
from ctypes.wintypes import DWORD, HANDLE, LPCWSTR, BOOL


if platform.architecture()[0].startswith('64'):
    WIN_PACK = 8
else:
    WIN_PACK = 1

#Flags controlling file acccess
GENERIC_WRITE = 0x40000000
GENERIC_READ = 0x80000000

FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002

OPEN_EXISTING = 3
OPEN_ALWAYS = 4
FILE_ATTRIBUTE_NORMAL = 0x80
FILE_FLAG_OVERLAPPED = 0x40000000

class LpSecurityAttributes(Structure):
    """Security attributes structure"""
    _pack_ = WIN_PACK
    _fields_ = [("n_length", DWORD), ("lp_security_descriptor", c_void_p),
                ("b_Inherit_handle", BOOL)]

CreateFile = windll.kernel32.CreateFileW
CreateFile.argtypes = [LPCWSTR, DWORD, DWORD, c_void_p, DWORD, DWORD, HANDLE]
CreateFile.restype = HANDLE

CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = BOOL
