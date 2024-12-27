import struct
from typing import Union, TypedDict
from PhigrosAPILib.PyTypes.Record import Record
from PhigrosAPILib.Tools.LoadJson import load_song_info, load_chart_constants

class ScoreAcc(TypedDict):
  score: int
  acc: float

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

  def read_score_acc(self) -> ScoreAcc:
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
      constants = chart_constant_list[song_id]

      records: Union[list[Record], None] = []
      for level in range(len(constants)):
        if get_bool(exists, level):
          score_acc = self.read_score_acc()
          pre_rks = (score_acc["acc"] - 55) / 45

          record: Record = {
            "id": song_id,
            "name": song_info_list[song_id]["name"],
            "artist": song_info_list[song_id]["artist"],
            "level": difficulty[level],
            "constant": constants[level],
            "score": score_acc["score"],
            "acc": score_acc["acc"],
            "rks": pre_rks * pre_rks * constants[level],
            "fc": get_bool(fc, level),
          }
         
          records.append(record)
    else:
      records = None
    self.position = end_position
    return records