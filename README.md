[![MCHP](images/microchip.png)](https://www.microchip.com)

# pykitinfo - Python Kit Information
pykitinfo provides information about connected Microchip development kits and tools

pykitinfo will scan the USB subsystem for connected Microchip development kits, and provide information such as kit name, mounted device, serial port identifier, and extension information.

Install using pip from [pypi.org](https://pypi.org/project/pykitinfo/):
```bash
pip install pykitinfo
```

Browse source code on [github](https://github.com/microchip-pic-avr-tools/pykitinfo)

Read API documentation on [github](https://microchip-pic-avr-tools.github.io/pykitinfo)

pykitinfo currently supports:
- all PKOB nano (nEDBG), mEDBG and EDBG kits
- Atmel-ICE, Power Debugger, JTAGICE3
- PICkit3, PKOB
- PICkit4, Snap, PKOB4, PICkit5

## Usage
pykitinfo can be used as a library or as a CLI

### CLI usage
When installed using pip, pykitinfo CLI is located in the Python scripts folder.

#### CLI example - simple list of connected kits
```bash
pykitinfo
```

Displays a simple list of kits in the form:
Kit SERIAL-NUMBER: 'KIT-NAME' (DEVICE-NAME) on SERIAL-PORT

For example:
```bash
pykitinfo
Looking for Microchip kits...
Compatible kits detected: 6
Kit MCHP3349011800000000: 'AVR-IoT WA' (ATmega4808) on COM21
Kit MCHP3280021800000000: 'AVR128DA48 Curiosity Nano' (AVR128DA48) on COM17
Kit ATML2241020200000000: 'SAM L21 Xplained Pro' (ATSAML21J18A) on COM34
Kit J41800000000: 'Atmel-ICE CMSIS-DAP' () on N/A
Kit J50200000000: 'Power Debugger CMSIS-DAP' () on N/A
Kit ATML2323040200000000: 'mEDBG' (ATmega328P) on COM26
```

#### CLI example - simple list of connected kits with specific serial number
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

#### CLI example - brief lookup of serial port of connected kit
```bash
pykitinfo -b
```
Displays ONLY the serial port name of a connected kit.  This can be useful for command chaining.

For example:
```bash
pykitinfo -b -s 123456
COM12
```

#### CLI example - long form list of connected kits
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


### Library usage example
pykitinfo can be imported and used as a library.

```python
# Example usage of pykitinfo as a library
import logging
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.ERROR)
from pykitinfo import pykitinfo
kits = pykitinfo.detect_all_kits()
for kit in kits:
    print("Found kit: '{}'".format(kit['debugger']['kitname']))
```

## Notes for Linux® systems
This package uses pyedbglib and other libraries for USB transport and some udev rules are required. For details see the pyedbglib package: https://pypi.org/project/pyedbglib
