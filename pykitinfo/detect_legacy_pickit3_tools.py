"""
Detection for PICkit3-type tools.
These tools are generally HID-based and use the Microchip USB VID.
Examples: PICkit3, PKoB on Curiosity.
"""
from logging import getLogger
import hid
from .tools import MICROCHIP_VID

def detect_pickit3s(serialnumber=None):
    """
    Look for PICkit3 devices

    :param serialnumber: (partial) serial number to use
    :type serialnumber: str
    :return: kits and tools connected
    :rtype: list of dictionaries
    """
    logger = getLogger(__name__)
    logger.debug("Looking for PKoB/PICkit 3 kits")
    PICKIT3_PRODUCT_NAMES = ["PICkit 3", "Curiosity", "Explorer 16/32 PICkit on Board"]
    pickit_list = []
    devices = hid.enumerate(MICROCHIP_VID)
    for candidate in devices:
        candidate_serial = candidate['serial_number']
        # Filter out by serial number if specified
        if serialnumber and candidate_serial and not candidate_serial.endswith(serialnumber):
            continue
        if candidate['product_string'] in PICKIT3_PRODUCT_NAMES:
            # USB native properties
            usb_info = {
                "interface": "hid",
                "packet_size": 0,
                "product_id": candidate['product_id'],
                "product_string": candidate['product_string'],
                "serial_number": candidate_serial,
                "vendor_id": candidate['vendor_id']
            }
            # Debugger properties
            debugger = {
                'device': '',
                'serial_number': candidate_serial,
                'protocol': 'pk3',
                # Use product name as kit name
                'kitname' : candidate['product_string'],
                'serial_port': 'N/A',
            }
            # Full entry:
            kit = {
                'usb': usb_info,
                'debugger': debugger
            }
            pickit_list.append(kit)
    return pickit_list
