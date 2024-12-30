import json
import os
from ..PyTypes.SongInfo import *

def get_path(path: str) -> str:
  file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    path
  )

  return os.path.normpath(file_path)

def load_chart_constants():
  chart_constants: dict[str, list[float]] = {}

  with open(get_path("../data/constants.json"), "r", encoding="utf-8") as fl:
    chart_constants = json.load(fl)

  return chart_constants

def load_song_info():
  song_info: dict[str, SongInfo] = {}

  with open(get_path("../data/infos.json"), "r", encoding="utf-8") as fl:
    song_info = json.load(fl)

  return song_info
