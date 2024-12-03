"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
	- Tommaso Mortara <>
"""
from dataclasses import dataclass, field
from typing import List
from ...utils import Utils

@dataclass
class EventDataClass:
    """Definirzione tipo di dato per Documento Evento"""
    stand_list: List[str]
    start_date: str
    end_date: str

    def get_stand_list(self) -> str:
        """Getter per lista id stand"""
        return self.stand_list

    def get_start_date(self) -> int:
        """Getter per data inizio evento"""
        return self.start_date

    def get_end_date(self) -> int:
        """Getter per da fine evento"""
        return self.end_date
