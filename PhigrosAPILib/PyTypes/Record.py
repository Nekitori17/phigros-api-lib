from typing import TypedDict

class Record(TypedDict):
  song_id: str
  song_name: str
  song_artist: str
  level: int
  difficulty: float
  fc: bool
  rks: float
  score: int
  acc: float
