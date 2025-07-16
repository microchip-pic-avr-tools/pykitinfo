""" Genx tools API"""
from enum import Enum, unique

GET_PKOB_CONFIG_AREA_TRANSMIT_SIZE_IN_BYTES                    =    9
# Transmit offsets
API_COMMAND_OPCODE_TRANSMIT_OFFSET                             =    0

class GenxError(Exception):
    """Generic Genx exeption"""

@unique
class CommandErrors(Enum):
    """
    API Command Error Codes

    .. data:: API_NO_ERROR
        0x00 - No error or issues occurred -- the API command operation was successful.

    Bootloader API low-level EEFC intrinsic flash-related errors:

    .. data:: API_FLASH_EEFC_MECCEMSB_ERROR
        0x60 - Multiple errors detected and NOT corrected on 64 MSB part of the flash memory.

    .. data:: API_FLASH_EEFC_UECCEMSB_ERROR
        0x61 - One unique error detected but corrected on 64 MSB data bus of the flash memory.

    .. data:: API_FLASH_EEFC_MECCELSB_ERROR
        0x62 - Multiple errors detected and NOT corrected on 64 LSB part of the flash memory.

    .. data:: API_FLASH_EEFC_UECCELSB_ERROR
        0x63 - One unique error detected but corrected on 64 LSB data bus of the flash memory.

    .. data:: API_FLASH_EEFC_FLERR_ERROR
        0x64 - A Flash memory error occurred at the end of programming (erase/verify or write/verify test has failed).

    .. data:: API_FLASH_EEFC_FLOCKE_ERROR
        0x65 - Programming/erase of at least one locked region has happened.

    .. data:: API_FLASH_EEFC_FCMDE_ERROR
        0x66 - An invalid command and/or a bad keyword was sent to the flash controller.

    Bootloader API higher-level EEFC custom errors:

    .. data:: API_FLASH_EEFC_FSR_FRDY_BIT_TIMEOUT_ERROR
        0x70 - A flash ready status flag timeout error has occurred.

    .. data:: API_FLASH_EEFC_ILLEGAL_WAIT_STATE_VALUE
        0x71 - An illegal flash wait state value was received.

    .. data:: API_FLASH_EEFC_LOCK_ATTEMPT_FAILED
        0x72 - A lock attempt on a flash lock region failed.

    .. data:: API_FLASH_EEFC_UNLOCK_ATTEMPT_FAILED
        0x73 - An unlock attempt on a flash lock region failed.

    .. data:: API_FLASH_EEFC_NOT_INITIALIZED
        0x74 - An attempt to use the flash driver before it was initialized error.

    Bootloader API higher-level flash/EEPROM-related errors:

    .. data:: API_FLASH_ILLEGAL_TYPE_REQUEST
        0x80 - An operation on an invalid flash type was requested. Legal flash types are 'PFM' or 'BFM'.

    .. data:: API_FLASH_ADDR_NOT_PAGE_ALIGNED
        0x81 - The address argument received is not page-aligned.

    .. data:: API_FLASH_ADDR_NOT_16_PAGE_ALIGNED
        0x82 - The address argument received is not aligned to a 16-native page boundary.

    .. data:: API_FLASH_POST_WRITE_VERIFY_FAILED
        0x83 - The flash memory post-write verification operation indicates the flash memory write was not successful.

    .. data:: API_FLASH_PAGE_WR_REQ_BUT_NOT_ERASED
        0x84 - A flash page was found not to be erased when a row write was requested.

    .. data:: API_FLASH_POST_ERASE_BLANK_FAILURE
        0x85 - Flash memory was found not to be erased during the post-erase blank check.

    .. data:: API_FLASH_ILLEGAL_APPLICATION_ADDRESS
        0x86 - An address outside of Application space was received.

    .. data:: API_FLASH_BOOT_WR_REQ_BUT_NOT_ERASED
        0x87 - An attempt was made to write to a non-erased flash area of the Bootloader.

    .. data:: API_FLASH_BOOT_ERASE_NOT_IMPLEMENTED
        0x88 - Erasing the Bootloader from within the Bootloader (old design) has been deprecated.

    .. data:: API_FLASH_BOOT_WRITE_NOT_IMPLEMENTED
        0x89 - Writing (re-flashing) the Bootloader from within the Bootloader (old design) has been deprecated.

    .. data:: API_SERIAL_EEPROM_ACCESS_ERROR
        0xB0 - Error accessing the I2C serial EEPROM.

    Bootloader API general/miscellaneous errors:

    .. data:: API_CRC_MISMATCH_RAM_BOOT_IMAGE
        0xC0 - CRC signature mismatch on the boot image RAM buffer received.

    .. data:: API_ILLEGAL_ARGUMENT
        0xC1 - An illegal argument was received.

    .. data:: API_ILLEGAL_LOCK_MEMORY_RANGE_ARGUMENT
        0xC2 - An illegal lock memory range argument was received.

    .. data:: API_IMAGE_CRC_MISMATCH_RAM_VS_BOOT
        0xC3 - CRC signature mismatch between received RAM image and post-write of entire Bootloader.

    FPGA Programming API related errors:

    .. data:: API_FPGA_PROGRAMMING_FAILED
        0xD0 - FPGA program failed

    .. data:: API_FPGA_PROGRAMMING_USB_READ_FAILED
        0xD1 - Host USB read fail during FPGA programming

    .. data:: API_FPGA_PROGRAMMING_USB_WRITE_FAILED
        0xD2 - Host USB write fail during FPGA programming

    .. data:: API_FPGA_PROGRAMMING_USB_CMD_TX_FAIL
        0xD3 - HOST USB command transmit failed

    .. data:: API_FPGA_PROGRAMMING_USB_INVALID_RESPONSE
        0xD4 - Host USB got wrong response

    .. data:: API_UNKNOWN_ERROR
        0xF0 - Unassigned error code (it is a firmware bug if client code ever receives this code).
    """
    API_NO_ERROR                              = 0x00
    API_FLASH_EEFC_MECCEMSB_ERROR             = 0x60
    API_FLASH_EEFC_UECCEMSB_ERROR             = 0x61
    API_FLASH_EEFC_MECCELSB_ERROR             = 0x62
    API_FLASH_EEFC_UECCELSB_ERROR             = 0x63
    API_FLASH_EEFC_FLERR_ERROR                = 0x64
    API_FLASH_EEFC_FLOCKE_ERROR               = 0x65
    API_FLASH_EEFC_FCMDE_ERROR                = 0x66
    API_FLASH_EEFC_FSR_FRDY_BIT_TIMEOUT_ERROR = 0x70
    API_FLASH_EEFC_ILLEGAL_WAIT_STATE_VALUE   = 0x71
    API_FLASH_EEFC_LOCK_ATTEMPT_FAILED        = 0x72
    API_FLASH_EEFC_UNLOCK_ATTEMPT_FAILED      = 0x73
    API_FLASH_EEFC_NOT_INITIALIZED            = 0x74
    API_FLASH_ILLEGAL_TYPE_REQUEST            = 0x80
    API_FLASH_ADDR_NOT_PAGE_ALIGNED           = 0x81
    API_FLASH_ADDR_NOT_16_PAGE_ALIGNED        = 0x82
    API_FLASH_POST_WRITE_VERIFY_FAILED        = 0x83
    API_FLASH_PAGE_WR_REQ_BUT_NOT_ERASED      = 0x84
    API_FLASH_POST_ERASE_BLANK_FAILURE        = 0x85
    API_FLASH_ILLEGAL_APPLICATION_ADDRESS     = 0x86
    API_FLASH_BOOT_WR_REQ_BUT_NOT_ERASED      = 0x87
    API_FLASH_BOOT_ERASE_NOT_IMPLEMENTED      = 0x88
    API_FLASH_BOOT_WRITE_NOT_IMPLEMENTED      = 0x89
    API_SERIAL_EEPROM_ACCESS_ERROR            = 0xB0
    API_CRC_MISMATCH_RAM_BOOT_IMAGE           = 0xC0
    API_ILLEGAL_ARGUMENT                      = 0xC1
    API_ILLEGAL_LOCK_MEMORY_RANGE_ARGUMENT    = 0xC2
    API_IMAGE_CRC_MISMATCH_RAM_VS_BOOT        = 0xC3
    API_FPGA_PROGRAMMING_FAILED               = 0xD0
    API_FPGA_PROGRAMMING_USB_READ_FAILED      = 0xD1
    API_FPGA_PROGRAMMING_USB_WRITE_FAILED     = 0xD2
    API_FPGA_PROGRAMMING_USB_CMD_TX_FAIL      = 0xD3
    API_FPGA_PROGRAMMING_USB_INVALID_RESPONSE = 0xD4
    API_UNKNOWN_ERROR                         = 0xF0

@unique
class Commands(Enum):
    """Genx commands

    Commands for managing firmware upgrade modes, flash memory operations, and tool diagnostics.

    Attributes:
        ENTER_FW_UPGRADE_MODE (int): Forces the tool in a non-volatile enabling of Bootloader upgrade mode.
            Application support: YES / Bootloader support: NO
        GET_FIRMWARE_INFO (int): Retrieves firmware information.
            Application support: YES / Bootloader support: YES
        ERASE_FLASH (int): Erases flash memory.
            Application support: NO / Bootloader support: YES for erasing PFM, NO for erasing BFM
        WRITE_FLASH_PFM (int): Writes Program Flash Memory (PFM) only.
            Application support: NO / Bootloader support: YES
        WRITE_FLASH_BFM (int): Writes Boot Flash Memory (BFM) only.
            Application support: NO / Bootloader support: NO
        GET_CRC (int): Provides CRC-32 signatures of various flash areas.
            Application support: NO / Bootloader support: YES
        JUMP_TO_APPLICATION (int): Disables Bootloader upgrade mode and jumps to application.
            Application support: NO / Bootloader support: YES
        SOFTWARE_RESET (int): Software resets the tool's MCU.
            Application support: YES / Bootloader support: YES
        DIAGNOSTIC_INFO (int): Provides tool & MCU diagnostic information.
            Application support: NO / Bootloader support: YES
        ERASE_FLASH_PAGE_PFM (int): Erases a single page of Program Flash Memory (PFM).
            Application support: NO / Bootloader support: YES
        WRITE_FLASH_PFM_REV_2 (int): Writes Program Flash Memory (PFM) with cleaner implementation.
            Application support: NO / Bootloader support: YES
        ENTER_FW_UPGRADE_MODE_REV_2 (int): Forces Bootloader mode state without echoing response.
            Application support: YES / Bootloader support: NO
        JUMP_TO_APPLICATION_REV_2 (int): Disables Bootloader upgrade mode without echoing response.
            Application support: NO / Bootloader support: YES
        SOFTWARE_RESET_REV_2 (int): Software resets the tool's MCU without echoing response.
            Application support: YES / Bootloader support: YES
        REFLASH_BOOTLOADER (int): Updates the bootloader with a new image.
            Application support: YES / Bootloader support: NO
        SET_SUB_APP_ADDRESSES (int): Changes sub-application base addresses.
            Application support: NO / Bootloader support: YES
        SET_SUB_APP_INDEX (int): Changes Sub-Application firmware images.
            Application support: YES / Bootloader support: YES
        GET_PKOB_CONFIG_AREA (int): Reads MPLAB PKoB Board Configuration Data Area.
            Application support: YES / Bootloader support: NO
        GET_TOOL_INFORMATION (int): Queries tool information through NON-USB interfaces.
            Application support: YES / Bootloader support: NO
        GET_ICE4_TRANSPORT_CONF (int): Queries ICE4 tool transport conf information via USB.
            Application support: YES / Bootloader support: NO
        SET_ICE4_TRANSPORT_CONF (int): Sets new ICE4 tool transport conf information via USB.
            Application support: YES / Bootloader support: NO
    """
    ENTER_FW_UPGRADE_MODE = 0xE0
    GET_FIRMWARE_INFO = 0xE1
    ERASE_FLASH = 0xE2
    WRITE_FLASH_PFM = 0xE3
    WRITE_FLASH_BFM = 0xE4
    GET_CRC = 0xE5
    JUMP_TO_APPLICATION = 0xE6
    SOFTWARE_RESET = 0xE7
    DIAGNOSTIC_INFO = 0xE8
    ERASE_FLASH_PAGE_PFM = 0xE9
    WRITE_FLASH_PFM_REV_2 = 0xEA
    ENTER_FW_UPGRADE_MODE_REV_2 = 0xEB
    JUMP_TO_APPLICATION_REV_2 = 0xEC
    SOFTWARE_RESET_REV_2 = 0xED
    REFLASH_BOOTLOADER = 0xEE
    SET_SUB_APP_ADDRESSES = 0xEF
    SET_SUB_APP_INDEX = 0xF0
    GET_PKOB_CONFIG_AREA = 0xF1
    GET_TOOL_INFORMATION = 0xF2
    GET_ICE4_TRANSPORT_CONF = 0xF3
    SET_ICE4_TRANSPORT_CONF = 0xF4

class GenxContoller():
    """ Genx tools API"""
    # USB endpoint addresses for Gen 4 & Gen 5 tools:
    COMMAND_CHANNEL_USB_IN_ENDPOINT_ADDRESS  = 0x81
    COMMAND_CHANNEL_USB_OUT_ENDPOINT_ADDRESS = 0x02

    DATA_CHANNEL_USB_IN_ENDPOINT_ADDRESS     = 0x83
    DATA_CHANNEL_USB_OUT_ENDPOINT_ADDRESS    = 0x04

    GET_PKOB_CONFIG_AREA_RESPONSE_SIZE_IN_BYTES  = 514
    GET_PKOB_CONFIG_AREA_RESPONSE_RAW_DATA_OFFSET = 1
    GET_PKOB_CONFIG_AREA_RESPONSE_ERROR_CODE_OFFSET = 513

    # Receive offsets:
    API_COMMAND_OPCODE_RESPONSE_ECHO_OFFSET =   0

    def __init__(self, device):
        self.usb_device = device

    def send_command(self, command, timeout_ms=1000):
        """Send a command

        :param command: Command to send
        :type command: bytes | bytearray
        :param timeout: Timeout in milliseconds for the write operation, defaults to 1000 ms
        :type timeout_ms: int, optional
        :return: Number of bytes that have been sent
        :rtype: int
        """
        bytes_written = self.usb_device.write(self.COMMAND_CHANNEL_USB_OUT_ENDPOINT_ADDRESS, command, timeout=timeout_ms)
        return bytes_written

    def get_command_response(self, response_size, timeout_ms=1000):
        """Fetch a command response

        :param response_size: Size of the expected response
        :type response_size: int
        :param timeout_ms: Timeout in milliseconds for the read operation, defaults to 1000 ms
        :type timeout: int, optional
        :return: Response
        :rtype: bytes
        """
        response = self.usb_device.read(self.COMMAND_CHANNEL_USB_IN_ENDPOINT_ADDRESS, response_size, timeout=timeout_ms)
        return bytes(response)

    def command_transaction(self, command, response_size):
        """Execute a command and response transaction

        :param command: Command
        :type command: bytes | bytearray
        :param response_size: Expected response size
        :type response_size: int
        :raises GenxError: For detected errors in the transaction
        :return: Response
        :rtype: bytes
        """
        bytes_sent = self.send_command(command)
        if bytes_sent != len(command):
            raise GenxError("USB send error")
        response= self.get_command_response(response_size)
        # Check command echo
        if response[self.API_COMMAND_OPCODE_RESPONSE_ECHO_OFFSET] != Commands.GET_PKOB_CONFIG_AREA.value:
            err_txt = "Invalid command response. " +\
                f"Expected {Commands.GET_PKOB_CONFIG_AREA.name}(0x{Commands.GET_PKOB_CONFIG_AREA.value:02x}) "+\
                f"but got 0x{response[self.API_COMMAND_OPCODE_RESPONSE_ECHO_OFFSET]:02x}"
            print(err_txt)
            raise GenxError(err_txt)
        return response

    # TODO: Not sure if there is a factory config block but in any case this has to stay so
    # that this API matches the EDBG API when used with pydebuggerconfig
    def read_config_block(self, factory=False):
        """Read the PKoB4 configuration block

        :param factory: True for factory configuration block, defaults to False
        :type factory: bool, optional
        :raises GenxError: 
        :return: Raw configuration data
        :rtype: bytes
        """
        command_buffer = bytearray(GET_PKOB_CONFIG_AREA_TRANSMIT_SIZE_IN_BYTES)
        command_buffer[API_COMMAND_OPCODE_TRANSMIT_OFFSET] = Commands.GET_PKOB_CONFIG_AREA.value
        command_buffer[1] = 0x00
        command_buffer[2] = 0x00
        command_buffer[3] = 0x00
        command_buffer[4] = 0x00
        command_buffer[5] = 0x00
        command_buffer[6] = 0x00
        command_buffer[7] = 0x00
        command_buffer[8] = 0x00
        response = self.command_transaction(command_buffer, self.GET_PKOB_CONFIG_AREA_RESPONSE_SIZE_IN_BYTES)

        # Check for error codes
        error_code = response[self.GET_PKOB_CONFIG_AREA_RESPONSE_ERROR_CODE_OFFSET]
        if error_code != CommandErrors.API_NO_ERROR.value:
            try:
                error_code_name = f"Error code {CommandErrors(error_code).name}"
            except ValueError:
                error_code_name = "Invalid error code "
            finally:
                raise GenxError(f"Command error. {error_code_name} {error_code:02x}")

        config_data = response[self.GET_PKOB_CONFIG_AREA_RESPONSE_RAW_DATA_OFFSET:-1]
        return config_data
