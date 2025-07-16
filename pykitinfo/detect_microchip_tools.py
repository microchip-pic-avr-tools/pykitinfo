"""
Detection for Microchip non-HID class tools
These tools are generally Vendor class USB interface and use the Microchip USB VID
Examples: PICkit4 (not in 'AVR mode') and PICkit5
"""
from logging import getLogger
import libusb_package
import usb
from pyedbglib.serialport.serialportmap import SerialPortMap
from pydebuggerconfig.boardconfig import BoardConfig
from pydebuggerconfig.pydebuggerconfig_errors import PydebuggerconfigError
import serial.tools.list_ports
from .tools import lookup_tool
from .tools import MICROCHIP_VID
from .genx import GenxContoller, GenxError


logger = getLogger(__name__)

# pylint: disable=too-few-public-methods
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
    def __init__(self): #pylint: disable=super-init-not-called
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
            if f"PID={MICROCHIP_VID:04X}" in port.hwid:
                self.portmap.append({"tool" : VendorClassTool(port.serial_number), "port": port.device})

def get_kit_info(device):
    """Get the kit info from PKoB4

    :param device: pyusb USB device
    :type device: Device
    """
    kit_info = {}
    try:
        genx_tool = GenxContoller(device)
        board = BoardConfig()
        # Hack to inject GenxController into BoardConfig
        board.protocol = genx_tool
        board.transport = True
        board.transport_connected = True
        board.config_read_from_board()

        kit_info["kitname"] = board.register_get("KITNAME").replace('\u0000', '')
        kit_info["device"] = board.register_get("DEVNAME").replace('\u0000', '')
        kit_info["manufacturer"] = board.register_get("MNFRNAME").replace('\u0000', '')
        kit_info["serialnumber"] = board.register_get("SERNUM").replace('\u0000', '')
    # The TypeError is here only until pydebuggerconfig library is fixed and returns
    # a library specific error based on PydebuggerconfigError
    except (TypeError, PydebuggerconfigError, GenxError) as exc:
        logger.warning("Could not read detailed tool information: %s", exc)
        kit_info["kitname"] = "N/A"
        kit_info["device"] = "N/A"
        kit_info["manufacturer"] = "N/A"
        kit_info["serialnumber"] = "N/A"

    return kit_info

def generate_kit_info(device, tool, serial_number):
    """Generate kit info

    :param device: pyusb device
    :type device: device
    :param tool: Tool information
    :type tool: dict
    :param serial_number: Tool serial number
    :type serial_number: str
    :return: Kit information
    :rtype: dict
    """
    try:
        product_name = device.product
    except ValueError as exc:
        logger.debug("Device VID=0x%04x PID=%04x %s", device.idVendor, device.idProduct, exc)
        product_name = "N/A"

    debugger = {
        'device': '',
        'serial_number': serial_number,
        'protocol': 'N/A',
        'kitname' : tool['Name'],
        'serial_port': 'N/A',
    }

    # TODO Once the CMSIS based PKoB supports kit-info we can change this to
    # read out the info again
    if "pkob4" in tool['Name'].lower() and "cmsis" not in tool['Name'].lower():
        kit_info = get_kit_info(device)
        debugger["device"] = kit_info["device"]
        debugger["kitname"] = kit_info["kitname"]

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
    return kit

def list_libusb_tools(serialnumber=None):
    """
    List all Microchip Vendor class tools that libusb can find

    :param serialnumber: (partial) serial number to use
    :type serialnumber: str
    :return: List of tools that were detected through libusb.
    :rtype: list
    """
    tools = []
    devices =  libusb_package.find(find_all=True, idVendor=MICROCHIP_VID)
    for device in devices:
        tool = lookup_tool(device.idProduct)
        if tool:
            try:
                serial_number = device.serial_number
                if serial_number is None:
                    raise ValueError("Tool has no serial number")
                # Some tools pad the serial number with \u0000 but these must be stripped
                # for comparison with OS detected serial numbers
                serial_number = serial_number.replace('\u0000', '')
            except ValueError as exc:
                logger.debug("Device VID=0x%04x PID=%04x %s", device.idVendor, device.idProduct, exc)
                serial_number = "N/A"
            if serialnumber and serial_number and not serial_number.endswith(serialnumber):
                continue

            if tool:
                try:
                    kit = generate_kit_info(device, tool, serial_number)
                    tools.append(kit)
                except usb.core.USBError as exc:
                    logger.error("Device VID=0x%04x PID=%04x %s", device.idVendor, device.idProduct, exc)
    return tools


def detect_microchip_tools(serialnumber=None):
    """
    Detect all USB tools in the Gen4/5 family.

    The tools are searched by using winusb library on Windows and libusb on all other platforms.
    :param serialnumber: (partial) serial number to use
    :type serialnumber: str
    :return: List of detected tools
    :rtype: list
    """

    logger.debug("Looking for Microchip USB Vendor Class tools")
    tools = list_libusb_tools(serialnumber)
    return tools
