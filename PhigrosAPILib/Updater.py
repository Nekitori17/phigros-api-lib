import os
import re
import json
import regex
from Important import *
from typing import Union
from bs4 import BeautifulSoup
from PyTypes.Database import *
from PyTypes.SongInfo import *
from urllib.request import urlopen

difficulties = ["ez", "hd", "in", "at", "legacy"]


def get_path(path: str) -> str:
  file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    path
  )

  return os.path.normpath(file_path)

DATA_FROM_WIKI_TMP_FILE = get_path("./tmp/dataFromWiki.json")

def string_cleaner(input_str: str) -> str:
    no_html_tags = regex.sub(r"<[^>]*>", "", input_str)
    no_html_encoding = regex.sub(r"&#[xX]?[a-fA-F0-9]+;", "", no_html_tags)
    cleaned_str = regex.sub(r"[^\p{L}\d]", "", no_html_encoding)

    return cleaned_str

def format_field(field: Union[str, FormatField]) -> str:
  if isinstance(field, str):
    return field

  result = field["format"]
  pattern = r"<<<(\d+)(?:\|([^\|>]+))?>>>" 

  def replacer(match: re.Match) -> str:
    number = match.group(1)
    unicode_value = match.group(2)

    if unicode_value:
      return unicode_value

    return field[number]

  result = re.sub(pattern, replacer, result)

  return result

class UpdateDataBase:
  def __init__(self, url: str):
    self.url = url

  def clean_textarea(self, raw_text: str) -> str:
    raw_text = re.sub(r'(?<=\s)(\d+)(?=\s*:)', r'"\1"', raw_text)
    raw_text = re.sub(r'(\d+\s*:\s*".*?"\s*#.*?)(\s*)$', r'\1,\2', raw_text)

    error_string: dict[str, str] = {
      '<<<1|RDRT -p "19":08:31>>>': "<<<1|RDRT -p 19:08:31>>>",
      '<<<1|RDRT -p "20":02:21>>>': "<<<1|RDRT -p 20:02:21>>>",
      'RDRT -p "20":08:31': "RDRT -p 20:08:31",
      'RWND -p "16493":62786:92551': "RWND -p 16493:62786:92551"
    }

    for key, value in error_string.items():
      raw_text = raw_text.replace(key, value)
        
    return raw_text

  def get_json_from_wiki(self):
    response = urlopen(self.url)
    content = response.read().decode("utf-8")
    
    soup = BeautifulSoup(content, "html.parser")
    soup.encode("utf-8")
    
    textarea = soup.find("textarea", id="wpTextbox1").text
    json_string = self.clean_textarea(textarea)

    return json_string
  
  def file_processing(self) -> dict[str, SongDataBaseInfo]:
    with open(DATA_FROM_WIKI_TMP_FILE, "w+", encoding="utf-8") as open_file:
      open_file.write(self.get_json_from_wiki())
    
    with open(DATA_FROM_WIKI_TMP_FILE, "r", encoding="utf-8") as open_file:
      wiki_data = json.load(open_file)

    return wiki_data

  def write_chart_constants(self):
    wiki_data = self.file_processing()

    chart_constants: dict[str, ChartConstants] = {}
    for song_name, song_info in wiki_data.items():
      chart_id = f"{string_cleaner(song_name)}.{string_cleaner(format_field(song_info["artist"]))}"
      sub_id = ""
      if "title" in song_info.keys():
        sub_id = f"{string_cleaner(song_info["title"])}.{string_cleaner(format_field(song_info["artist"]))}"

      chart_constant: list[float] = []
      for difficulty in difficulties:
        if difficulty in song_info.keys():
          if song_info[difficulty]["level"] != "N/A":
            chart_constant.append(float(song_info[difficulty]["level"]))
          else:
            chart_constant.append(0.0)
        else:
          chart_constant.append(0.0)

      chart_constants[chart_id] = {
        "sub_id": sub_id,
        "constant": chart_constant
      }

    with open(get_path("./data/constants.json"), "w", encoding="utf-8") as fl:
      fl.write(json.dumps(chart_constants, indent=2, ensure_ascii=False))

  def write_song_info(self):
    wiki_data = self.file_processing()

    song_infos: dict[str, SongInfo] = {}
    for song_name, song_info in wiki_data.items():
      song_id = f"{string_cleaner(song_name)}.{string_cleaner(format_field(song_info["artist"]))}"
      sub_id = ""
      if "title" in song_info.keys():
        sub_id = f"{string_cleaner(song_info["title"])}.{string_cleaner(format_field(song_info["artist"]))}"

      main_charter = format_field(song_info["charter"])
      song_charter: list[str] = []

      for difficulty in difficulties:
        if difficulty in song_info.keys():
          if "charter" in song_info[difficulty].keys():
            song_charter.append(format_field(song_info[difficulty]["charter"]))
          else:
            song_charter.append(main_charter)
        else:
          song_charter.append("N/A")

      song_infos[song_id] = {
        "song_name": song_info["title"] if "title" in song_info.keys() else song_name,
        "sub_id": sub_id,
        "song_artist": format_field(song_info["artist"]),
        "illustration": format_field(song_info["illustration"]),
        "original": bool(song_info["original"]) if "original" in song_info.keys() else False,
        "charter": song_charter,
        "version": song_info["version"]
      }

    with open(get_path("./data/infos.json"), "w", encoding="utf-8") as open_file:
      json.dump(song_infos, open_file, indent=2, ensure_ascii=False)

  def update_all(self):
    self.write_song_info()
    self.write_chart_constants()

if __name__ == "__main__":
  updater = UpdateDataBase(PHIGROS_FANDOM_WIKI_SONG_DATA_URL)
  updater.update_all()