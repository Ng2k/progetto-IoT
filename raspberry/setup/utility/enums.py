"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
from enum import Enum

class Colors(Enum):
	"""
	Enumerazione dei colori disponibili.
	"""
	BOLD_PINK = '\033[1;95m'
	BOLD_CYAN = '\033[1;36m'
	BOLD_YELLOW = '\033[1;33m'
	BOLD_GREEN = '\033[1;32m'
	BOLD_RED = '\033[1;31m'
	BOLD_BLUE = '\033[1;34m'
	BOLD_PURPLE = '\033[1;35m'
	WHITE = '\033[1;37m'
	GRAY = '\033[1;90m'
	GREEN = '\033[0;32m'
	COLOR_OFF = '\033[0m'

class OperationTags(Enum):
	"""
	Enumerazione dei tag disponibili.
	"""
	NONE = ""
	TITLE = f"{Colors.BOLD_PINK.value}[TITLE] {Colors.COLOR_OFF.value}"
	INFO = f"{Colors.BOLD_CYAN.value}[INFO] {Colors.COLOR_OFF.value}"
	TASK = f"{Colors.BOLD_YELLOW.value}[TASK] {Colors.COLOR_OFF.value}"
	SUCCESS = f"{Colors.BOLD_GREEN.value}[SUCCESS] {Colors.COLOR_OFF.value}"
	ERROR = f"{Colors.BOLD_RED.value}[ERROR] {Colors.COLOR_OFF.value}"
	COMMAND = f"{Colors.BOLD_YELLOW.value}[COMMAND] {Colors.COLOR_OFF.value}"
	DESCRIPTION = f"{Colors.WHITE.value}[DESCRIPTION] {Colors.COLOR_OFF.value}"