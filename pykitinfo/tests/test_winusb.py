"""Unittests for WinUSB library wrapper
"""
import unittest
import platform

if platform.system() == "Windows":
    from ..winusb import parse_device_path

    class TestWinUsb(unittest.TestCase):
        """Tests for winusb library"""

        def setUp(self):
            pass

        def test_parse_windows_path(self):
            """Test parse windwos path function.
            """
            test_path_icd4 = r"\\?\usb#vid_04d8&pid_9015#jit172820226#{dee824ef-729b-4a0e-9c14-b7117d33a817}"
            test_path_snap = r"\\?\usb#vid_04d8&pid_9018#bur182626045#{dee824ef-729b-4a0e-9c14-b7117d33a817}"
            # nEDBG is a composite device and the 3rd interface (DGI) is registered in WinUSB
            # Composite device paths do not have a serial number, instead they use a unique Windows generated string
            # based on e.g. physical USB port address and/or interface number
            test_path_nedbg = \
                    r"\\?\usb#vid_03eb&pid_2175&mi_03#f&1bc0a34f&0&0003#{dee824ef-729b-4a0e-9c14-b7117d33a817}"
            device = parse_device_path(test_path_snap)
            self.assertTrue(device["vendor_id"] == 0x04d8 and
                            device["product_id"] == 0x9018 and
                            device["serial_number"] == "bur182626045")

            device = parse_device_path(test_path_icd4)
            self.assertTrue(device["vendor_id"] == 0x04d8 and
                            device["product_id"] == 0x9015 and
                            device["serial_number"] == "jit172820226")

            device = parse_device_path(test_path_nedbg)
            self.assertTrue(device["vendor_id"] == 0x03eb and
                            device["product_id"] == 0x2175 and
                            device["serial_number"] == "f&1bc0a34f&0&0003")
