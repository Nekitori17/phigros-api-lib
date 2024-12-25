from typing import TypedDict

class SongInfo(TypedDict):
  sub_id: str
  song_name: str
  song_artist: str
  illustrator: str
  original: bool
  charter: list[str]
  version: str

class ChartConstants(TypedDict):
  sub_id: str
  constant: list[float]