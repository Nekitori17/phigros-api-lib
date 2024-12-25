import struct
from typing import Union
from PyTypes.Record import Record
from Tools.LoadJson import load_song_info, load_chart_constants

difficulty = ["EZ", "HD", "IN", "AT", "Legacy"]
chart_constant_list = load_chart_constants()
song_info_list  = load_song_info()

def get_bool(num, index):
  return bool(num & 1 << index)

class ByteReader:
  position: int = 0

  def __init__(self, data: bytes):
    self.data = data

  def read_var_short(self):
    num = self.data[self.position]
    if num < 128:
      self.position += 1
    else:
      self.position += 2
    return num

  def read_string(self):
    length = self.data[self.position]
    self.position += length + 1
    return self.data[self.position - length : self.position].decode("utf-8", errors="ignore")

  def read_score_acc(self):
    self.position += 8
    scoreAcc = struct.unpack("if", self.data[self.position - 8 : self.position])
    return {"score": scoreAcc[0], "acc": scoreAcc[1]}

  def read_record(self, song_id: str):
    end_position = self.position + self.data[self.position] + 1

    self.position += 1
    exists = self.data[self.position]

    self.position += 1
    fc = self.data[self.position]

    self.position += 1

    if song_id in chart_constant_list:
      diffs = chart_constant_list[song_id]

      records: Union[list[Record], list] = []
      for level in range(len(diffs["constant"])):
        if get_bool(exists, level):
          scoreAcc: Record = self.read_score_acc()
          scoreAcc["song_id"] = song_id
          scoreAcc["song_name"] = song_info_list[song_id]["song_name"]
          scoreAcc["song_artist"] = song_info_list[song_id]["song_artist"]
          scoreAcc["level"] = difficulty[level]
          scoreAcc["difficulty"] = diffs["constant"][level]
          scoreAcc["rks"] = (scoreAcc["acc"] - 55) / 45
          scoreAcc["rks"] = (
            scoreAcc["rks"] * scoreAcc["rks"] * scoreAcc["difficulty"]
          )
          scoreAcc["fc"] = get_bool(fc, level)
          records.append(scoreAcc)
    else:
      records = []
    self.position = end_position
    return records