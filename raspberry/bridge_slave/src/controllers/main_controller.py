"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""

import asyncio
from typing import List

#from ..communications.ble_communication import BLECommunication
from ..communications.serial_communication import SerialCommunication
from ..communications.communication_interface import ICommunication

class MainController:
    """Controller of the main process"""

    def __init__(self, device_list: list):
        self._device_list = device_list

    def get_device_list(self) -> dict:
        """Returns all the devices currently connected

        Returns:
            dict: Dictionary with all the devices
        """
        return self._device_list

    async def _create_handler_list(self, device_list) -> List[ICommunication]:
        """Create handlers for all the devices
        
        Returns:
            List[ICommunication]: list of handlers
        """
        serial_devices = device_list["serial_devices"]
        
        serial_handlers = [
            SerialCommunication(device["port"], device["serial_number"]) for device in serial_devices
        ]

        #ble_devices = device_list["ble_devices"]
        #ble_handlers = [
        #    BLECommunication(device["address"]) for device in ble_devices
        #]

        return serial_handlers #+ ble_handlers

    async def _create_task_list(
        self,
        device_handler_list: List[ICommunication]
    ) -> list:
        """Returns a list of tasks to run concurrently
        
        Returns:
            List[ICommunication]: list of tasks
        """

        return [handler.read_data() for handler in device_handler_list]

    async def run(self) -> None:
        """Method to run all the tasks concurrently"""
        device_handler_list = await self._create_handler_list(self._device_list)
        task_list = await self._create_task_list(device_handler_list)
        await asyncio.gather(*task_list)
