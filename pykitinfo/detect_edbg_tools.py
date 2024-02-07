"""
Detection for EDBG-based tools.
These tools are generally HID-based, are CMSIS-DAP implentations and use the Atmel USB VID
Examples: Atmel-ICE, nEDBG/PKOB nano used on Curiosity Nano kits
"""
from logging import getLogger
from pyedbglib.hidtransport.hidtransportfactory import hid_transport
from pyedbglib.protocols.cmsisdap import CmsisDapUnit
from pyedbglib.protocols.edbgprotocol import EdbgProtocol
from pyedbglib.serialport.serialportmap import SerialPortMap
from pyedbglib.protocols.avrcmsisdap import AvrCommandError
from pydebuggerconfig.backend import board_config_manager

NUM_ID_CHANNELS_EDBG = 8    # Maximum 8 extensions, 1-indexed
NUM_ID_CHANNELS_NEDBG = 1   # Single ID channel


def _detect_compatible_hid_devices(transport, serialnumber=None):
    """
    Look for all connected HID-based kits

    :param serialnumber: (partial) serial number to use
    :type serialnumber: str
    :return: kits and tools connected
    :rtype: list of dictionaries
    """
    kit_list = []
    for i in transport.devices:
        # Filter out by serial number if specified
        if serialnumber and i.serial_number and not i.serial_number.endswith(serialnumber):
            continue
        usb = {}
        usb['interface'] = 'hid'
        usb['product_string'] = i.product_string
        usb['serial_number'] = i.serial_number
        usb['packet_size'] = i.packet_size
        usb['product_id'] = i.product_id
        usb['vendor_id'] = i.vendor_id
        kit_list.append(usb)
    return kit_list


def _get_kitname(serialnumber):
    """
    Looks up kitname given a connected kit's serial number
    :return: kit name
    """
    with board_config_manager(serialnumber_substring=serialnumber) as board_cfg:
        board_cfg.config_read_from_board()
        for register in board_cfg.specification_xml['board'].findall("./registers/register"):
            offset = int(register.attrib['offset'], 16)
            size = int(register.attrib['size'])
            if register.attrib['name'] == "KITNAME":
                return ''.join(chr(i) for i in board_cfg.data_array['board'][offset:offset + size]).strip('\0')
    return ''

def _edbg_config_request(field):
    """
    Format a minimalistic EDBG GET_CONFIG request
    """
    request = [EdbgProtocol.AVR_GET_CONFIG]
    request.append (1) # 1 element
    request.append (field)
    request.append (ord('?')) # dummy
    request.extend ([0, 0]) # offset
    request.extend ([32, 0]) # size
    return bytearray(request)

def detect_edbg_kits(serialnumber=None):
    """
    Look for all compatible EDBG-based kits

    :param serialnumber: (partial) serial number to use
    :type serialnumber: str
    :return: kits and tools connected
    :rtype: list of dictionaries
    """
    logger = getLogger(__name__)
    logger.debug("Looking for xEDBG kits")
    kit_list = []
    transport = hid_transport()
    usb_devices = _detect_compatible_hid_devices(transport, serialnumber=serialnumber)

    # Run through the top-level list
    for device in usb_devices:
        kit = {
            'usb': device
        }
        # Probe each edbg-like kit
        if not transport.connect(device['serial_number']):
            logger.error("Unable to connect to kit")
            continue

        # Find out CMSIS-DAP level info
        unit = CmsisDapUnit(transport)
        info = unit.dap_info()

        # Some EDBG versions do NOT have the dap_info 'device' tag populated for non-ARM parts.
        # Sneak in and collect the data from the EDBG config instead
        if info['product'][:4] == 'EDBG' and info['device_name'] == '':
            try:
                cmd = _edbg_config_request(0x04) # 4 == 'TARGET DEVICE NAME'
                # raw command routed via the HK interface
                response = unit.dap_command_response(cmd)
                info['device_name'] = response[6:6 + 32].split(b'\0')[0].decode()
            except: #pylint: disable=bare-except
                # resort to ''
                pass

        debugger = {
            'device': info['device_name'],
            'product': info['product'],
            'serial_number': info['serial'],
            'protocol': 'edbg'
        }
        kit['debugger'] = debugger

        # nEDBG uses kit config have kitnames
        if 'nedbg' in debugger['product'].lower():
            # Which ID channels are available (used later)
            ID_CHANNELS = range(1, NUM_ID_CHANNELS_NEDBG+1)
            # Disconnect before using pydebuggerconfig backend
            transport.disconnect()
            debugger['kitname'] = _get_kitname(device['serial_number'])
            # Reconnect for further probing
            transport.connect(device['serial_number'])
        # mEDBG and EDBG need different lookup
        elif 'edbg' in debugger['product'].lower().split()[0]:
            # Which ID channels are available (used later)
            ID_CHANNELS = range(1, NUM_ID_CHANNELS_EDBG+1)
            # Look for extra info
            cmd = _edbg_config_request(0x02) # 2 == 'KIT NAME'
            # raw command routed via the HK interface
            response = unit.dap_command_response(cmd)
            debugger['kitname'] = response[6:6 + 32].split(b'\0')[0].decode()
        else:
            # Which ID channels are available (used later)
            ID_CHANNELS = []
            # Else use debugger name as kit name
            debugger['kitname'] = debugger['product']

        # Some kits can have guessable serial ports
        if debugger['product'].lower().split()[0] in ['nedbg', 'medbg', 'edbg', 'power', 'mplab']:
            spm = SerialPortMap()
            try:
                debugger['serial_port'] = spm.find_matching_tools_ports(debugger['serial_number'])[0]['port']
            except IndexError:
                debugger['serial_port'] = 'N/A'
        else:
            debugger['serial_port'] = 'N/A'

        # EDBG and nEDBG products support extensions, which can be probed for
        if debugger['product'].lower().split()[0] in ['edbg', 'nedbg']:
            edbg = EdbgProtocol(transport)
            # Look for extensions
            extensions = []
            # Refresh the ID chip and read the ID data
            edbg.refresh_id_chip()
            for ext in ID_CHANNELS:
                try:
                    id_data = edbg.read_id_chip(ext)
                except (NotImplementedError, AvrCommandError):
                    break
                if id_data[0] != 0:
                    # Parse out extension fields
                    ext_details = ''.join(chr(i) for i in id_data).split('\0')
                    extension = {
                        'ext' : ext,
                        'manufacturer' : ext_details[0],
                        'name' : ext_details[1],
                        'power' : ext_details[2],
                        'serial_number' : ext_details[3],
                    }
                    extensions.append(extension)
            kit['extensions'] = extensions

        transport.disconnect()

        kit_list.append(kit)

    return kit_list
