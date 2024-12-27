from typing import TypedDict
from PhigrosAPILib.PyTypes.Record import Record

class BestRecords(TypedDict):
  phi: Record
  b19: list[Record]
  overflow: int