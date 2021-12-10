"""Windows setup API wrapper
"""
import platform
from ctypes import Structure, POINTER, c_ulong, c_void_p
from ctypes import windll, GetLastError,FormatError
from ctypes.wintypes import DWORD, WORD, BYTE, WCHAR, HANDLE, LPCWSTR, BOOL, ULONG

SPDRP_HARDWAREID = 1
SPDRP_FRIENDLYNAME = 12
SPDRP_LOCATION_PATHS = 35
SPDRP_MFG = 11

if platform.architecture()[0].startswith('64'):
    WIN_PACK = 8
else:
    WIN_PACK = 1

class DEVPROPKEY(Structure):
    """DEVPROPKEY Windows OS structure"""
    _pack_ = WIN_PACK
    _fields_ = [("data1", DWORD),
                ("data2", WORD),
                ("data3", WORD),
                ("data4", BYTE * 8),
                ("pid", ULONG)]

DEVPROPKEY_DEVICE_PARENT = DEVPROPKEY(0x4340a6c5, 0x93fa, 0x4706,
                                    (BYTE * 8)(0x97, 0x2c, 0x7b, 0x64, 0x80, 0x08, 0xa5, 0xa7), 8)

class GUID(Structure):
    """GUID Windows OS structure"""
    _pack_ = 1
    _fields_ = [("data1", DWORD),
                ("data2", WORD),
                ("data3", WORD),
                ("data4", BYTE * 8)]

class SpDeviceInterfaceData(Structure):
    """Device Interface Data structure"""
    _pack_ = WIN_PACK
    _fields_ = [("cb_size", DWORD),
                ("interface_class_guid", GUID),
                ("flags", DWORD),
                ("reserved", POINTER(c_ulong))
                ]

class SpDeviceInterfaceDetailData(Structure):
    """Device Interface Detail Data structure"""
    _pack_ = WIN_PACK
    _fields_ = [("cb_size", DWORD),
                ("device_path", WCHAR * 1)
               ]

class SpDevinfoData(Structure):
    """Device Info Data structure"""
    _pack_ = WIN_PACK
    _fields_ = [("cb_size", DWORD),
                ("class_guid", GUID),
                ("dev_inst", DWORD),
                ("reserved", POINTER(c_ulong))
               ]
USB_WINUSB_GUID = GUID(0xdee824ef, 0x729b, 0x4a0e, (BYTE * 8)(0x9c, 0x14, 0xb7, 0x11, 0x7d, 0x33, 0xa8, 0x17))
USB_DEVICE_GUID = GUID(0xA5DCBF10, 0x6530, 0x11D2, (BYTE * 8)(0x90, 0x1F, 0x00, 0xC0, 0x4F, 0xB9, 0x51, 0xED))
USB_COMPOSITE_GUID = GUID(0x36FC9E60, 0xC465, 0x11CF, (BYTE * 8)(0x80, 0x56, 0x44, 0x45, 0x53, 0x54, 0x00, 0x00))

class DIGCF:
    """
    Flags controlling what is included in the device information set built
    by SetupDiGetClassDevs
    """
    DEFAULT         = 0x00000001  # only valid with DIGCF.DEVICEINTERFACE
    PRESENT         = 0x00000002
    ALLCLASSES      = 0x00000004
    PROFILE         = 0x00000008
    DEVICEINTERFACE = 0x00000010

class WinApiException(Exception):
    "Rough Windows API exception type"
    pass

def winapi_result(result):
    """Validate WINAPI BOOL result, raise exception if failed"""
    if not result:
        last_error = GetLastError()
        raise WinApiException(f"{last_error} (0x{last_error:x}): {FormatError()}")
    return result

setupapi = windll.setupapi

SetupDiGetClassDevsW = setupapi.SetupDiGetClassDevsW
SetupDiGetClassDevsW.restype  = HANDLE
SetupDiGetClassDevsW.argtypes = [
    POINTER(GUID), # __in_opt  const GUID *ClassGuid,
    LPCWSTR, # __in_opt  PCTSTR Enumerator,
    HANDLE,  # __in_opt  HWND hwndParent,
    DWORD,   # __in      DWORD Flags
    ]

SetupDiEnumDeviceInterfaces = setupapi.SetupDiEnumDeviceInterfaces
SetupDiEnumDeviceInterfaces.restype = BOOL
SetupDiEnumDeviceInterfaces.argtypes = [
    HANDLE,                     # _In_ HDEVINFO DeviceInfoSet,
    POINTER(SpDevinfoData),   # _In_opt_ PSP_DEVINFO_DATA DeviceInfoData,
    POINTER(GUID),              # _In_ const GUIDi *InterfaceClassGuid,
    DWORD,                      # _In_ DWORD MemberIndex,
    POINTER(SpDeviceInterfaceData), # _Out_ PSP_DEVICE_INTERFACE_DATA DeviceInterfaceData
    ]

SetupDiGetDeviceInterfaceDetailW = setupapi.SetupDiGetDeviceInterfaceDetailW
SetupDiGetDeviceInterfaceDetailW.restype = BOOL
SetupDiGetDeviceInterfaceDetailW.argtypes = [
    HANDLE, # __in       HDEVINFO DeviceInfoSet,
    POINTER(SpDeviceInterfaceData), # __in PSP_DEVICE_INTERFACE_DATA DeviceIn
    # __out_opt  PSP_DEVICE_INTERFACE_DETAIL_DATA DeviceInterfaceDetailData,
    POINTER(SpDeviceInterfaceDetailData),
    DWORD, # __in       DWORD DeviceInterfaceDetailDataSize,
    POINTER(DWORD), # __out_opt  PDWORD RequiredSize,
    POINTER(SpDevinfoData), # __out_opt  PSP_DEVINFO_DATA DeviceInfoData
    ]

SetupDiGetDeviceRegistryPropertyW = setupapi.SetupDiGetDeviceRegistryPropertyW
SetupDiGetDeviceRegistryPropertyW.restype = BOOL
SetupDiGetDeviceRegistryPropertyW.argtypes = [
    c_void_p,
    POINTER(SpDevinfoData),
    DWORD,
    POINTER(DWORD),
    c_void_p,
    DWORD,
    POINTER(DWORD)
    ]

SetupDiGetDevicePropertyW = setupapi.SetupDiGetDevicePropertyW
SetupDiGetDevicePropertyW.restype = BOOL
SetupDiGetDevicePropertyW.argtypes = [
    c_void_p,                       # in  HDEVINFO         DeviceInfoSet
    POINTER(SpDevinfoData), # in  PSP_DEVINFO_DATA DeviceInfoData
    POINTER(DEVPROPKEY),            # in  const DEVPROPKEY *PropertyKey
    POINTER(ULONG),                 # out DEVPROPTYPE      *PropertyType
    POINTER(BYTE),                  # out PBYTE            PropertyBuffer
    DWORD,                          # in  DWORD            PropertyBufferSize
    POINTER(DWORD),                 # out PDWORD           RequiredSize
    DWORD                           # in  DWORD            Flags
]

SetupDiGetDevicePropertyKeys = setupapi.SetupDiGetDevicePropertyKeys
SetupDiGetDevicePropertyKeys.restype = BOOL
SetupDiGetDevicePropertyKeys.argtypes = [
    c_void_p,                       # in  HDEVINFO         DeviceInfoSet
    POINTER(SpDevinfoData), # in  PSP_DEVINFO_DATA DeviceInfoData
    POINTER(DEVPROPKEY),            # out DEVPROPKEY       *PropertyKeyArray
    DWORD,                          # in  DWORD            PropertyKeyCount
    POINTER(DWORD),                 # out PDWORD           RequiredPropertyKeyCount
    DWORD                           # in  DWORD            Flags
]
