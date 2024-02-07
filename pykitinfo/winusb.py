"""WinUSB library wrapper functions
"""
from logging import getLogger
from ctypes import c_ulong
from ctypes import wstring_at, byref, sizeof, resize
from ctypes.wintypes import DWORD, BYTE
from .winsetupapi import SetupDiEnumDeviceInterfaces, SetupDiGetClassDevsW, SetupDiGetDeviceInterfaceDetailW,\
            SpDeviceInterfaceData, SpDeviceInterfaceDetailData, SpDevinfoData, USB_WINUSB_GUID, DIGCF, winapi_result,\
            DEVPROPKEY_DEVICE_PARENT, SetupDiGetDevicePropertyW

logger = getLogger(__name__)

def list_winusb_devices():
    """List winusb devices

    :return: List of winusb devices
    :rtype: list
    """
    required_size = c_ulong(0)
    member_index = DWORD(0)
    sp_device_info_data = SpDevinfoData()
    sp_device_info_data.cb_size = sizeof(SpDevinfoData)
    sp_device_interface_data = SpDeviceInterfaceData()
    sp_device_interface_data.cb_size = sizeof(sp_device_interface_data)
    sp_device_interface_detail_data = SpDeviceInterfaceDetailData()

    # Get a handle to a list of currently enumerated WinUSB devices
    h_info = SetupDiGetClassDevsW(byref(USB_WINUSB_GUID), None, None, (DIGCF.PRESENT | DIGCF.DEVICEINTERFACE))
    winapi_result(h_info)
    devices = []
    # iterate over the list of WinUSB devices to get more information on each of them
    while SetupDiEnumDeviceInterfaces(h_info, None, byref(USB_WINUSB_GUID), member_index,
                                        byref(sp_device_interface_data)):

        # Get required size for sp_device_interface_data
        ret = SetupDiGetDeviceInterfaceDetailW(h_info, byref(sp_device_interface_data), None, 0,
                                                byref(required_size), None)
        # Only raise an exception if required size value is also 0
        if ret == 0 and required_size.value == 0:
            winapi_result(ret)
        resize(sp_device_interface_detail_data, required_size.value)
        sp_device_interface_detail_data.cb_size = sizeof(SpDeviceInterfaceDetailData)
        ret = SetupDiGetDeviceInterfaceDetailW(h_info, byref(sp_device_interface_data),
                                        byref(sp_device_interface_detail_data), required_size, byref(required_size),
                                        byref(sp_device_info_data))
        winapi_result(ret)
        path = wstring_at(byref(sp_device_interface_detail_data, sizeof(DWORD)))

        device = parse_device_path(path)
        device["path"] = path
        # Different path types can have serial number in upper or lower case
        # To be consistent we reside to upper case which also matches the actual
        # format of the PICkit4 device serial numbers.
        device["serial_number"] = device["serial_number"].upper()

        # If we have an interface number it is a composite device
        # and we need to get the parent to obtain the serial number
        if "interface_number" in device:
            property_type = c_ulong(0)
            property_buffer = (BYTE * 256)()
            property_buffer_size = DWORD(sizeof(property_buffer))
            required_size = DWORD(0)
            # Get the device parent property
            ret = SetupDiGetDevicePropertyW(h_info, byref(sp_device_info_data),
                                        byref(DEVPROPKEY_DEVICE_PARENT),
                                        byref(property_type),
                                        property_buffer,
                                        property_buffer_size,
                                        byref(required_size),
                                        DWORD(0))
            winapi_result(ret)
            path = wstring_at(byref(property_buffer))
            parent_device = parse_device_path(path)
            parent_device["serial_number"] = parent_device["serial_number"].upper()
            parent_device["path"] = path
            new_parent_device = True
            # If the parent already exists just add the interface
            for dev in devices:
                if dev["serial_number"] == parent_device["serial_number"]:
                    dev["interfaces"][device["interface_number"]] = {
                        "path": path
                    }
                    new_parent_device = False
            # Add parent and interface
            if new_parent_device:
                parent_device["interfaces"] = [None for x in range(10)]
                parent_device["interfaces"][device["interface_number"]] = {
                    "path":device["path"]
                }
                devices.append(parent_device)
        else:
            device["interfaces"] = []
            devices.append(device)

        member_index.value = member_index.value + 1
        required_size.value = 0
        resize(sp_device_interface_detail_data, sizeof(SpDeviceInterfaceDetailData))
        sp_device_interface_data.cb_size = sizeof(sp_device_interface_data)
    return devices

def parse_device_path(path):
    r"""Parse Windows USB device path.

    Extracts USB vendor ID, product ID and serial number from a Windows device path.
    Example paths:
    \\?\usb#vid_03eb&pid_2175&mi_03#6&319d7dcd&1&0003#{dee824ef-729b-4a0e-9c14-b7117d33a817}
    \\?\usb#vid_04d8&pid_9018#bur182626045#{dee824ef-729b-4a0e-9c14-b7117d33a817}
    USB\VID_03EB&PID_2175\ATML3203081800009066

    :param path: Windows USB device path
    :type path: str
    :return: Vendor ID, product ID and serial number for non composite devices.
             Vendor ID, product ID, interface number for composite devices.
    :rtype: dict
    """
    device = {}
    try:
        _, vid_pid_mi, device["serial_number"],_ = path.split("#", 3)
    except ValueError:
        _, vid_pid_mi, device["serial_number"] = path.split("\\", 2)
    tmp = vid_pid_mi.lower().split("&")
    device["vendor_id"] = int(tmp[0].strip("vid_"), 16)
    device["product_id"] = int(tmp[1].strip("pid_"), 16)
    if len(tmp) == 3:
        try:
            # Try to determine interface number for composite devices
            device["interface_number"] = int(tmp[2].strip("mi_"))
            logger.debug("WinUSB device VID=0x%04X:PID=0x%04X:Interface%d", device['vendor_id'], device["product_id"],
                                                                            device['interface_number'])
        except ValueError:
            logger.debug("WinUSB device VID=0x%04X:PID=0x%04X:UnknownInterface", device['vendor_id'],
                                                                                 device["product_id"])
    else:
        logger.debug("WinUSB device VID=0x%04X:PID=0x%04X", device['vendor_id'], device["product_id"])
    return device
