from typing import Optional, TypedDict, Union, Literal

class FormatField(TypedDict):
  format: str

Format = Union[FormatField, dict[int, str]]

class Difficulty(TypedDict):
  level: Union[float, Literal["N/A"]]
  notes: int
  charter: Optional[Union[Format, str]]

class GateWay(TypedDict):
  song: str
  method: str

class SongDataBaseInfo(TypedDict):
  title: Optional[str]
  pack: str
  gateway: Optional[GateWay]
  unlock: Optional[str]
  image: Optional[str]
  ez: Difficulty
  hd: Difficulty
  in_: Difficulty
  at: Optional[Difficulty]
  legacy: Optional[Difficulty]
  artist: Union[Format, str]
  duration: str
  charter: Union[Format, str]
  illustration: Union[Format, str]
  original: bool
  notes: Optional[int]
  removed: Optional[bool]
  version: str
