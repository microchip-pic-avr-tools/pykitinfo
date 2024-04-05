# pykitinfo
pykitinfo provides information about connected Microchip development kits and tools

## Overview
pykitinfo will scan the USB subsystem for connected Microchip development kits, and provide information such as kit name, mounted device, serial port identifier, and extension information.

pykitinfo is available:

* install using pip from pypi: https://pypi.org/project/pykitinfo
* browse source code on github: https://github.com/microchip-pic-avr-tools/pykitinfo
* read API documentation on github: https://microchip-pic-avr-tools.github.io/pykitinfo

pykitinfo currently supports:
* all PKOB nano (nEDBG), mEDBG and EDBG kits
* Atmel-ICE, Power Debugger, JTAGICE3
* PICkit3, PKOB
* PICkit4, Snap, PKOB4, PICkit5
* MCP2221A

## Usage
pykitinfo can be used as a library or as a CLI

## Example - simple list of connected kits
```bash
pykitinfo
```
Displays a simple list of kits in the form:
Kit SERIAL-NUMBER: 'KIT-NAME' (DEVICE-NAME) on SERIAL-PORT

For example:
```bash
pykitinfo
Looking for Microchip kits...
Compatible kits detected: 8
Kit MCHP3349011800000000: 'AVR-IoT WA' (ATmega4808) on COM21
Kit MCHP3280021800000000: 'AVR128DA48 Curiosity Nano' (AVR128DA48) on COM17
Kit ATML2241020200000000: 'SAM L21 Xplained Pro' (ATSAML21J18A) on COM34
Kit J41800000000: 'Atmel-ICE CMSIS-DAP' () on N/A
Kit J50200000000: 'Power Debugger CMSIS-DAP' () on N/A
Kit ATML2323040200000000: 'mEDBG' (ATmega328P) on COM26
Kit BUR180115004: 'Explorer 16/32 PICkit on Board' () on N/A
Kit 020063002RYN000091: 'Curiosity Nano Explorer' (N/A) on COM74
```

## Example - simple list of connected kits with specific serial number
```bash
pykitinfo -s <serialnumber ending>
```
Displays a simple list of kits in the form:
Kit SERIAL-NUMBER: 'KIT-NAME' (DEVICE-NAME) on SERIAL-PORT

For example:
```bash
pykitinfo -s 29
Looking for Microchip kits...
Compatible kits detected: 1
Kit MCHP3352011800000029: 'PIC-IoT WA' (PIC24FJ128GA705) on COM22
```

## Example - brief lookup of serial port of connected kit
```bash
pykitinfo -b
```
Displays ONLY the serial port name of a connected kit.  This can be useful for command chaining.

For example:
```bash
pykitinfo -b -s 123456
COM12
```

## Example - long form list of kits
```bash
pykitinfo -l
```

Displays a JSON formatted list of dictionaries.

For example:
```bash
pykitinfo -l
Looking for Microchip kits...
Compatible kits detected: 2
[
  {
    "debugger": {
      "device": "ATmega4808",
      "kitname": "AVR-IoT WA",
      "product": "nEDBG CMSIS-DAP",
      "protocol": "edbg",
      "serial_number": "MCHP3349011800000000",
      "serial_port": "COM21"
    },
    "usb": {
      "interface": "hid",
      "packet_size": 64,
      "product_id": 8565,
      "product_string": "nEDBG CMSIS-DAP",
      "serial_number": "MCHP3349011800000000",
      "vendor_id": 1003
    }
  },
  {
    "debugger": {
      "device": "AVR128DA48",
      "kitname": "AVR128DA48 Curiosity Nano",
      "product": "nEDBG CMSIS-DAP",
      "protocol": "edbg",
      "serial_number": "MCHP3280021800000000",
      "serial_port": "COM17"
    },
    "usb": {
      "interface": "hid",
      "packet_size": 64,
      "product_id": 8565,
      "product_string": "nEDBG CMSIS-DAP",
      "serial_number": "MCHP3280021800000000",
      "vendor_id": 1003
    }
  }
]
```

## Example - library usage
```python
# Example: using pykitinfo as a library
import logging
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.ERROR)
from pykitinfo import pykitinfo
kits = pykitinfo.detect_all_kits()
for kit in kits:
    print("Found kit: '{}'".format(kit['debugger']['kitname']))
```

## Notes for Linux® systems
This package uses pyedbglib and other libraries for USB transport and some udev rules are required. For details see the pyedbglib package: https://pypi.org/project/pyedbglib