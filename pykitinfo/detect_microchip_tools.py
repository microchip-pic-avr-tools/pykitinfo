"""
Detection for Microchip non-HID class tools
These tools are generally Vendor class USB interface and use the Microchip USB VID
Examples: PICkit4 (not in 'AVR mode') and PICkit5
"""
from logging import getLogger
import platform
import pprint
import usb.core
import usb.util
from pyedbglib.serialport.serialportmap import SerialPortMap
import serial.tools.list_ports
from .tools import lookup_tool
from .tools import MICROCHIP_VID

logger = getLogger(__name__)

class VendorClassTool ():
    """
    Class for holding information about Vendor class tools
    """
    def __init__ (self, serial_number):
        self.serial_number = serial_number

class MicrochipVendorClassToolsSerialPortMap(SerialPortMap):
    """
    This is a utility to find virtual serial port name based on the tool's device serial number.
    A sub-set of functionality is supported compared to the pyedbglib version for HID/CMSIS-DAP tools.
    """
    def __init__(self):
        """
        Create map of tools and ports based on serial number matching. Method used is
        very different on Windows and other platforms.
        """
        # Hook onto logger
        self.logger = getLogger(__name__)

        self.portmap = []
        usbports = [p for p in serial.tools.list_ports.comports() if "USB" in p.hwid]

        for port in usbports:
            if port.serial_number is None:
                # On Mac MCP2221 serial port on some Curiosity Development Boards have proven to not have a serial
                # number associated, so to avoid an exception when trying to map the serial port to a serial number
                # this port is just ignored
                self.logger.debug("No serial number associated with %s, ignoring",
                                  port.hwid)
                continue
            if "PID={:04X}".format(MICROCHIP_VID) in port.hwid:
                self.portmap.append({"tool" : VendorClassTool(port.serial_number), "port": port.device})

if platform.system() == "Windows":
    from .winusb import list_winusb_devices
    def list_winusb_tools(serialnumber=None):
        """
        List all Microchip Vendor class tools bound to winusb

        :param serialnumber: (partial) serial number to use
        :type serialnumber: str
        :return: List of detected tools
        :rtype: list
        """
        tools = []
        winusb_devices = list_winusb_devices()
        for device in winusb_devices:
            logger.debug("Found WinUSB device \n%s", pprint.pformat(device))
            device_serial = device['serial_number']
            if serialnumber and device_serial and not device_serial.endswith(serialnumber):
                continue
            if device["vendor_id"] == MICROCHIP_VID:
                tool = lookup_tool(device["product_id"])
                if tool:
                    # Debugger properties
                    debugger = {
                        'device': '',
                        'serial_number': device_serial,
                        'protocol': 'N/A',
                        # Use product name as kit name
                        'kitname' : tool['Name'],
                        'serial_port': 'N/A',
                    }
                    if "Serial port" in tool and tool["Serial port"] is True:
                        serial_port_mapper = MicrochipVendorClassToolsSerialPortMap()
                        try:
                            sp_list = serial_port_mapper.find_matching_tools_ports(device_serial)
                            debugger['serial_port'] = sp_list[0]['port']
                        except IndexError:
                            # Unable to determine serial port
                            debugger['serial_port'] = 'N/A'

                    usb_info = {
                    "interface": "winusb",
                    "packet_size": 0,
                    "product_id": device['product_id'],
                    "product_string": "Not read out",
                    "serial_number": device_serial,
                    "vendor_id": device['vendor_id']
                    }

                    kit = {
                        'usb': usb_info,
                        'debugger': debugger
                    }
                    tools.append(kit)
        return tools

def list_libusb_tools(serialnumber=None):
    """
    List all Microchip Vendor class tools bound to libusb

    :param serialnumber: (partial) serial number to use
    :type serialnumber: str
    :return: List of tools that were detected through libusb.
    :rtype: list
    """
    tools = []
    devices = usb.core.find(find_all=True, idVendor=MICROCHIP_VID)
    for device in devices:
        serial_number = device.serial_number
        if serialnumber and serial_number and not serial_number.endswith(serialnumber):
            continue
        tool = lookup_tool(device.idProduct)
        if tool:
            product_name = device.product
            debugger = {
                'device': '',
                'serial_number': serial_number,
                'protocol': 'N/A',
                'kitname' : tool['Name'],
                'serial_port': 'N/A',
            }
            if "Serial port" in tool and tool["Serial port"] is True:
                serial_port_mapper = MicrochipVendorClassToolsSerialPortMap()
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

def detect_microchip_tools(serialnumber=None):
    """
    Detect all USB tools in the PICkit4/PICkit5 family.

    The tools are searched by using winusb library on Windows and libusb on all other platforms.
    :param serialnumber: (partial) serial number to use
    :type serialnumber: str
    :return: List of detected tools
    :rtype: list
    """
    logger.debug("Looking for PICkit4/PICkit5 tools")
    if platform.system() == "Windows":
        tools = list_winusb_tools(serialnumber)
    else:
        tools = list_libusb_tools(serialnumber)
    return tools
