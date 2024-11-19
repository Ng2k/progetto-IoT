"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""

class DataPrinter:
    """
    A class responsible for printing the received data.
    """

    @staticmethod
    def print_data(data: str) -> None:
        """
        Prints the received data.

        Args:
            data (str): The data to be printed.
        """
        print("Received:", data)
