from typing import TypedDict

class Completion(TypedDict):
  EZ: list[int]
  HD: list[int]
  IN: list[int]
  AT: list[int]

class PlayerSummary(TypedDict):
  username: str
  updated_at: str
  url: str
  save_ver: int
  challenges: int
  rks: float
  display_rks: str
  game_ver: int
  avatar: str
  completion: Completion