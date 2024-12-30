from .Record import Record
from typing import TypedDict, Union

class BestRecords(TypedDict):
  phi: Record
  b19: list[Record]
  overflow: Union[list[Record], list]