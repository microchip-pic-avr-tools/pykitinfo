"""
Python Kit Information
~~~~~~~~~~~~~~~~~~~~~~

pykitinfo provides information about connected Microchip development kits and tools.

pykitinfo will scan the USB subsystem for connected Microchip development kits, and provide information such as kit name, mounted device, serial port identifier, and extension information.

pykitinfo is available:
    * install using pip from pypi: https://pypi.org/project/pykitinfo
    * browse source code on github: https://github.com/microchip-pic-avr-tools/pykitinfo
    * read API documentation on github: https://microchip-pic-avr-tools.github.io/pykitinfo
    * read the changelog on github: https://github.com/microchip-pic-avr-tools/pykitinfo/blob/main/CHANGELOG.md

pykitinfo currently supports:
    * all PKOB nano (nEDBG), mEDBG and EDBG kits
    * Atmel-ICE, Power Debugger, JTAGICE3
    * PICkit4, Snap (AVR mode)
    * PICkit3, PKoB, PICkit4, PKOB4, Snap (PIC mode) - partial support

CLI usage example
~~~~~~~~~~~~~~~~~
See examples on pypi: https://pypi.org/project/pykitinfo

Library usage example
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # pykitinfo uses python logging module
    import logging
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.ERROR)

    # detect all compatible kits
    from pykitinfo import pykitinfo
    kits = pykitinfo.detect_all_kits()

    # display results
    for kit in kits:
        print("Found kit: '{}'".format(kit['debugger']['kitname']))

"""
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
