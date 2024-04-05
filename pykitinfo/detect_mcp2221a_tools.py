from logging import getLogger
from .tools import MICROCHIP_VID
import hid
import serial.tools.list_ports

MCP2221A_PID = 0x00DD

def detect_mcp2221a_kits(serial_number=None):
    """
    Look for all compatible MCP2221A kits

    :param serial_number: (partial) serial number to use
    :type serial_number: str
    :return: List of detected tools
    :rtype: list
    """

    logger = getLogger(__name__)
    logger.debug("Looking for MCP2221A kits")

    devices = hid.enumerate(MICROCHIP_VID, MCP2221A_PID)
    port_map = map_mcp2221a_to_serial_port(devices)
    kits = []

    for device in devices:
        if serial_number and device['serial_number'] and not device['serial_number'].endswith(serial_number):
            continue

        mapped_port = list(filter(lambda dev: dev['tool'] == device, port_map))

        usb_info = {
            "interface": "hid",
            "packet_size": 0,
            "product_id": device['product_id'],
            "product_string": device['product_string'],
            "serial_number": device['serial_number'],
            "vendor_id": device['vendor_id']
        }

        debugger = {
            'device': 'N/A',
            'serial_number': device['serial_number'],
            'protocol': 'N/A',
            # Use product name as kit name
            'kitname' : device['product_string'],
            'serial_port': 'N/A' if len(mapped_port) == 0 else mapped_port[0]['port'],
        }

        kit = {
            'usb': usb_info,
            'debugger': debugger
        }

        kits.append(kit)

    return kits

def map_mcp2221a_to_serial_port(devices):
    """Map MCP2221A devices to serial ports

    :param devices: List of MCP2221A devices
    :type devices: list(dict)
    :return: List containing mapped serial ports to devices
    :rtype: list(dict)
    """

    logger = getLogger(__name__)

    portmap = []
    available_comports = serial.tools.list_ports.comports()

    usbports = set([p for p in available_comports if "USB" in p.hwid and MICROCHIP_VID == p.vid and p.pid == MCP2221A_PID])
    used_comports = set()
    devices_missing_serial_number = []

    for dev in devices:
        if not dev['serial_number'] or dev['serial_number'] == "":
            devices_missing_serial_number.append(dev)
        else:
            remaining_comports = usbports.symmetric_difference(used_comports)

            for port in remaining_comports:
                if dev['serial_number'] == port.serial_number:
                    portmap.append({"tool": dev, "port": port.device})
                    used_comports.add(port)
                    break

    # Now we should have left only the devices and ports from MCP2221A devices that don't have serial number
    # Here we can only map a single device

    if len(devices_missing_serial_number) > 1:
        logger.debug("Too many MCP2221 devices without serial number connected. Cannot map these to serial ports")
    elif len(devices_missing_serial_number) > 0 and len(usbports) > 0:
        portmap.append({"tool": devices_missing_serial_number[0], "port": list(usbports)[0].device})

    return portmap
