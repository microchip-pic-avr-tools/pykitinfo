"""Gen4 Tools detection module
"""
from logging import getLogger
import platform
import pprint
import usb.core
import usb.util
from pyedbglib.serialport.serialportmap import SerialPortMap
from .gen4_tools import lookup_tool

logger = getLogger(__name__)

if platform.system() == "Windows":
    from .winusb import list_winusb_devices
    def list_gen4_winusb_tools():
        """List all gen4 winusb tools.

        :return: List of detected gen4 tools
        :rtype: list
        """
        tools = []
        winusb_devices = list_winusb_devices()
        for device in winusb_devices:
            logger.debug("Found WinUSB device \n%s", pprint.pformat(device))
            if device["vendor_id"] == 0x04d8:
                tool = lookup_tool(device["product_id"])
                if tool:
                    # Debugger properties
                    debugger = {
                        'device': '',
                        'serial_number': device['serial_number'],
                        'protocol': 'N/A',
                        # Use product name as kit name
                        'kitname' : tool['Name'],
                        'serial_port': 'N/A',
                    }
                    if hasattr(tool, "Serial port") and tool["Serial port"] is True:
                        serial_port_mapper = SerialPortMap()
                        try:
                            debugger['serial_port'] = \
                                serial_port_mapper.find_matching_tools_ports(device["serial_number"])[0]['port']
                        except IndexError:
                            debugger['serial_port'] = 'N/A'

                    usb_info = {
                    "interface": "winusb",
                    "packet_size": 0,
                    "product_id": device['product_id'],
                    "product_string": "Not read out",
                    "serial_number": device['serial_number'],
                    "vendor_id": device['vendor_id']
                    }

                    kit = {
                        'usb': usb_info,
                        'debugger': debugger
                    }
                    tools.append(kit)
        return tools

def list_gen4_libusb_tools():
    """List gen4 tools from libusb.

    :return: List of tools that were detected through libusb.
    :rtype: list
    """
    tools = []
    devices = usb.core.find(find_all=True, idVendor=0x04D8)
    for device in devices:
        tool = lookup_tool(device.idProduct)
        if tool:
            serial_number = device.serial_number
            product_name = device.product
            debugger = {
                'device': 'N/A',
                'serial_number': serial_number,
                'protocol': 'N/A',
                'kitname' : tool['Name'],
                'serial_port': 'N/A',
            }
            if hasattr(tool, "Serial port") and tool["Serial port"] is True:
                # TODO the serial port mapper does not work for tools that don't have a HID interface
                # so a new implementation of this is required to detect a serial port for Gen4 tools.
                serial_port_mapper = SerialPortMap()
                try:
                    debugger['serial_port'] = serial_port_mapper.find_matching_tools_ports(serial_number)[0]['port']
                except IndexError:
                    debugger['serial_port'] = 'N/A'

            usb_info = {
                "interface": "winusb",
                "packet_size": device.bMaxPacketSize0,
                "product_id": device.idProduct,
                "product_string": product_name,
                "serial_number": serial_number,
                "vendor_id": device.idVendor
                }
            kit = {
                'usb': usb_info,
                'debugger': debugger
            }
            tools.append(kit)
    return tools

def detect_gen4_tools():
    """Detect all gen4 USB tools.

    The tools are searched by using winusb library on Windows and libusb on all other platforms.
    :return: List of detected tools
    :rtype: list
    """
    logger.debug("Looking for Gen4 kits")
    if platform.system() == "Windows":
        tools = list_gen4_winusb_tools()
    else:
        tools = list_gen4_libusb_tools()
    return tools
