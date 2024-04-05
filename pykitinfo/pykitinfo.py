"""
Python Kit Info
"""
from logging import getLogger
import json
from .detect_microchip_tools import detect_microchip_tools
from .detect_edbg_tools import detect_edbg_kits
from .detect_legacy_pickit3_tools import detect_pickit3s
from .detect_mcp2221a_tools import detect_mcp2221a_kits

STATUS_SUCCESS = 0
STATUS_FAILURE = 1

from . import __version__ as VERSION
from . import BUILD_DATE, COMMIT_ID

def pykitinfo(args):
    """
    Main program
    """
    logger = getLogger(__name__)
    if args.version or args.release_info:
        print("pykitinfo version {}".format(VERSION))
        if args.release_info:
            print("Build date: {}".format(BUILD_DATE))
            print("Commit ID:  {}".format(COMMIT_ID))
        return STATUS_SUCCESS

    # Populate kit list
    logger.debug("Detecting kits...")
    kit_list = detect_all_kits(serialnumber=args.serialnumber)

    # Display output, except in 'brief' mode which displays only serial port info
    if not args.brief:
        print("Looking for Microchip kits...")
        print("Compatible kits detected: {}".format(len(kit_list)))

    if args.long:
        # Display dict form
        print(json.dumps(kit_list, sort_keys=True, indent=2, ensure_ascii=False))
    else:
        # Display short form
        for kit in kit_list:
            if args.brief:
                print("{}".format(kit['debugger']['serial_port']))
            else:
                print("Kit {}: '{}' ({}) on {}".format(kit['usb']['serial_number'],
                                                       kit['debugger']['kitname'],
                                                       kit['debugger']['device'],
                                                       kit['debugger']['serial_port']))
    return STATUS_SUCCESS

def detect_all_kits(serialnumber=None):
    """
    Look for all compatible connected kits

    :param serialnumber: (partial) serial number to use
    :type serialnumber: str
    :return: kits and tools connected
    :rtype: list of dictionaries
    """
    kit_list = []
    kit_list += detect_edbg_kits(serialnumber)
    kit_list += detect_pickit3s(serialnumber)
    kit_list += detect_microchip_tools(serialnumber)
    kit_list += detect_mcp2221a_kits(serialnumber)

    return kit_list
