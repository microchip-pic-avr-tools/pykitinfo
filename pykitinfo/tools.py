"""
Tools list and lookup.
"""

MICROCHIP_VID = 0x04D8

MICROCHIP_NON_HID_TOOLS = [
            {
                "VID": MICROCHIP_VID,
                "PID": 0x8109,
                "Name": "MPLAB® PKoB4 In-Circuit Debugger",
            },
                        {
                "VID": MICROCHIP_VID,
                "PID": 0x810A,
                "Name": "MPLAB® PKoB4 Bootloader",
            },
            {
                # App FW Composite: Vendor + CDC
                "VID": MICROCHIP_VID,
                "PID": 0x810B,
                "Name": "MPLAB® PKoB4 In-Circuit Debugger",
                "Serial port": True
            },
            {
                # App FW Composite: Vendor + MSC
                "VID": MICROCHIP_VID,
                "PID": 0x810C,
                "Name": "MPLAB® PKoB4 In-Circuit Debugger",
                "Serial port": False
            },
            {
                # App FW Composite: Vendor + CDC + DGI
                "VID": MICROCHIP_VID,
                "PID": 0x810D,
                "Name": "MPLAB® PKoB4 In-Circuit Debugger",
                "Serial port": True
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x9012,
                "Name": "MPLAB® PICkit™4",
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x9013,
                "Name": "MPLAB® PM4",
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x9015,
                "Name": "MPLAB® ICD4",
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x9017,
                "Name": "MPLAB® PICkit™4 Bootloader",
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x9018,
                "Name": "MPLAB® Snap In-Circuit Debugger",
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x9019,
                "Name": "MPLAB® Snap™ Bootloader",
            },
            {
                #App FW Composite: Vendor_CDC
                "VID": MICROCHIP_VID,
                "PID": 0x901B,
                "Name": "MPLAB® PICkit™4",
                "Serial port": True
            },
            {
                # Composite: Vendor + CDC
                "VID": MICROCHIP_VID,
                "PID": 0x901C,
                "Name": "MPLAB® Snap In-Circuit Debugger",
                "Serial port": True
            },
            {
                #App FW Composite: Vendor_MSC
                "VID": MICROCHIP_VID,
                "PID": 0x901D,
                "Name": "MPLAB® PICkit™4",
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x901F,
                "Name": "MPLAB® ICE4 Bootloader",
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x9020,
                "Name": "MPLAB® ICE4",
            },
            {
                # Composite: Vendor + CDC
                "VID": MICROCHIP_VID,
                "PID": 0x9021,
                "Name": "MPLAB® ICE4",
                "Serial port": True
            },
            {
                # Composite: Vendor + MSC
                "VID": MICROCHIP_VID,
                "PID": 0x9022,
                "Name": "MPLAB® ICE4",
            },
            {
                # Composite: Vendor + CDC + DGI
                "VID": MICROCHIP_VID,
                "PID": 0x9023,
                "Name": "MPLAB® ICE4",
                "Serial port": True
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x9024,
                "Name": "MPLAB® ICE4 FX3 Trace Endpoint",
            },
            {
                # Composite: Vendor + CDC + DGI
                "VID": MICROCHIP_VID,
                "PID": 0x9028,
                "Name": "MPLAB® PICkit™4",
                "Serial port": True
            },
            {
                # Composite: Vendor + CDC + DGI
                "VID": MICROCHIP_VID,
                "PID": 0x9029,
                "Name": "MPLAB® Snap",
                "Serial port": True
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x902A,
                "Name": "MPLAB® ICD4 Bootloader",
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x902A,
                "Name": "MPLAB® ICD4 Bootloader",
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x9036,
                "Name": "MPLAB® PICkit™5",
                "Serial port": True
            },
            {
                "VID": MICROCHIP_VID,
                "PID": 0x9035,
                "Name": "MPLAB® PICkit™5 Bootloader",
            },
        ]

def lookup_tool(product_id):
    """Lookup tool based on USB product ID

    :param product_id: USB product ID
    :type product_id: int
    :return: If product was found, return dict with tool information.
    :rtype: dict if tool was found, otherwise None
    """
    for tool in MICROCHIP_NON_HID_TOOLS:
        if tool["PID"] == product_id:
            return tool
    return None
