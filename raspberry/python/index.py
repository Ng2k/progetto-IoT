"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
import asyncio

from .src.controllers.main_controller import MainController
from .src.device_scanner import DeviceScanner

if __name__ == "__main__":
    device_scanner = DeviceScanner()
    devices_available = device_scanner.scan_devices()
    controller = MainController(devices_available)

    # Run the application
    asyncio.run(controller.run())
