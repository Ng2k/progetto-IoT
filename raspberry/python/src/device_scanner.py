"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""

from bleak import BleakScanner
from serial.tools import list_ports

class DeviceScanner:
    """
    A class to scan and list nearby devices, both BLE and serially connected.
    """

    async def scan_devices(self) -> dict:
        """
        Scans for nearby BLE devices and serial devices asynchronously.

        Returns:
            dict: A dictionary containing BLE devices and serial devices.
        """
        # Scan BLE devices asynchronously
        print("Scanning for ble devices...")
        ble_result = self._scan_ble_devices()

        # Scan serial devices
        print("Scanning for serial devices...")
        serial_devices = self._scan_serial_devices()

        return {"ble_devices": ble_result, "serial_devices": serial_devices}

    async def _scan_serial_devices(self) -> list[dict]:
        """
        Scans for serial devices connected to the system.

        Returns:
            list[dict]: A list of serial devices.
        """
        ports = list_ports.comports()
        return [
            {
                "port": port.device,
                "description": port.description
            } for port in ports
        ]

    async def _scan_ble_devices(self) -> dict:
        """Scan for ble devices

        Returns:
            list[dict]: list of ble devices 
        """
        print("Scanning for BLE devices...")
        ble_devices = await BleakScanner.discover()
        return [
            {"name": device.name or "Unknown", "address": device.address}
            for device in ble_devices
        ]
