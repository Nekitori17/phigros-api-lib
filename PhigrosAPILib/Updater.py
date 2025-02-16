import os
import json
import requests
from .Constants import *
from .PyTypes.SongInfo import *


def get_path(path: str) -> str:
  file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    path
  )

  return os.path.normpath(file_path)

class DataUpdater:
  def __init__(self):
    pass

  def update_song_info(self):
    song_infos: dict[str, SongInfo]  = {}

    data_from_source = requests.get(PHIGROS_SONG_INFO).text.split("\n")
    for line in data_from_source:
      if line.startswith("#") or line == "": continue
      line_data = line.split("\t")
      
      song_id = line_data[0]
      song_name = line_data[1]
      song_artist = line_data[2]
      illustrator = line_data[3]
      charter = line_data[4:]
      if len(charter) < 4:
        charter.append("N/A")
      
      song_infos[song_id] = {
        "name": song_name,
        "artist": song_artist,
        "illustrator": illustrator,
        "charter": charter
      }

    with open(get_path("./data/infos.json"), "w", encoding="utf-8") as fl:
      json.dump(song_infos, fl, ensure_ascii=False, indent=2)

  def update_chart_constants(self):
    chart_constants: dict[str, list[float]] = {}

    data_from_source = requests.get(PHIGROS_CONSTANTS).text.split("\n")
    for line in data_from_source:
      if line.startswith("#") or line == "": continue
      line_data = line.split("\t")
      
      chart_id = line_data[0]
      chart_constant = [float(x) for x in line_data[1:]]
      if len(chart_constant) < 4:
        chart_constant.append(0.0)

      chart_constants[chart_id] = chart_constant

    with open(get_path("./data/constants.json"), "w", encoding="utf-8") as fl:
      json.dump(chart_constants, fl, ensure_ascii=False, indent=2)
  
  def update_all(self):
    self.update_song_info()
    self.update_chart_constants()