"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
import asyncio

from .log_handler import LogHandler
from .device_scanner import DeviceScanner

from .controllers.main_controller import MainController

async def main():
    """Start the program"""
    log_handler = LogHandler()

    device_scanner = DeviceScanner(LogHandler)
    devices_available = await device_scanner.scan_devices()
    controller = MainController(devices_available, LogHandler)

    # Run the application
    await controller.run()

if __name__ == "__main__":
    asyncio.run(main())
