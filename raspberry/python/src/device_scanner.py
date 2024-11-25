"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
from asyncio import Lock
from typing import List
import pyudev
from bleak import BleakScanner

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
        # todo: Scan BLE devices asynchronously
        #print("Scanning for BLE devices...")
        #ble_result = await self._scan_ble_devices()

        # Scan serial devices
        print("Scanning for serial devices...")
        serial_devices = await self._scan_serial_devices()

        return { "serial_devices": serial_devices } #, "ble_devices": ble_result, }

    async def _scan_serial_devices(self) -> List[dict]:
        """
        Scans for serial devices connected to the system.

        Returns:
            list[dict]: A list of serial devices.
        """
        context = pyudev.Context()
        return [
            {
                "port": device.device_node,
                "description": device.get("ID_USB_MODEL", "Unknown"),
                "serial_number": device["ID_SERIAL_SHORT"]
            }
            for device in context.list_devices(subsystem="tty")
            if "ID_SERIAL_SHORT" in device
        ]

    async def _scan_ble_devices(self) -> dict:
        """Scan for ble devices

        Returns:
            list[dict]: list of ble devices 
        """
        async with Lock():
            ble_devices = await BleakScanner.discover()
            return [
                {"name": device.name or "Unknown", "address": device.address}
                for device in ble_devices
            ]
