"""
Author:
    - Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""

import abc

class ICommunication(metaclass=abc.ABCMeta):
    """Interface for the communication classes"""
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, "read_data") and callable(subclass.read_data))

    @abc.abstractmethod
    async def read_data(self) -> None:
        """Starts reading data from the device"""
        raise NotImplementedError
