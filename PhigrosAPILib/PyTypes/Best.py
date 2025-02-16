from .Record import Record
from typing import TypedDict, Union

class BestRecords(TypedDict):
  phi: list[Record]
  b27: list[Record]
  overflow: Union[list[Record], list]