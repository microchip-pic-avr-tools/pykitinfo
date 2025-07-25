"""
Python Kit Information
~~~~~~~~~~~~~~~~~~~~~~

pykitinfo provides information about connected Microchip development kits and tools.

pykitinfo will scan the USB subsystem for connected Microchip development kits, and provide information such as kit name, mounted device, serial port identifier, and extension information.

pykitinfo is available:
    * install using pip from pypi: https://pypi.org/project/pykitinfo
    * browse source code on github: https://github.com/microchip-pic-avr-tools/pykitinfo
    * read API documentation on github: https://microchip-pic-avr-tools.github.io/pykitinfo
    * read the changelog on pypi:  https://pypi.org/project/pykitinfo

pykitinfo currently supports:
    * all PKOB nano (nEDBG), mEDBG and EDBG kits
    * Atmel-ICE, Power Debugger, JTAGICE3
    * PICkit3, PKOB
    * PICkit4, Snap, PKOB4, PICkit5
    * MCP2221A

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

# Build number part of version will be replaced by build number from Jenkins.
# For local builds the build number is 0 and the 'snapshot' is added as Local Version Identifier
__version__ = "1.4.1.26"

# The GIT commit ID and build date are generated by Jenkins when building the package
COMMIT_ID = 'c8a955dd7d2162a890d34ce6aca7a5eb73f1cbb2'
BUILD_DATE = '2025-07-23 11:04:14'

logging.getLogger(__name__).addHandler(logging.NullHandler())
