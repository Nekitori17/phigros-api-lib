import struct
from typing import Union, TypedDict
from ..PyTypes.Record import Record
from ..PyTypes.Progress import PlayerProgress
from .LoadJson import load_song_info, load_chart_constants

class ScoreAcc(TypedDict):
  score: int
  acc: float

difficulty = ["EZ", "HD", "IN", "AT", "Legacy"]
chart_constant_list = load_chart_constants()
song_info_list = load_song_info()

def get_bool(num, index):
  return bool(num & 1 << index)

class ByteReader:
  def __init__(self, data: bytes):
    self.data = data
    self.position = 0
    self.bit_position = 0

  def read_bool(self) -> bool:
    if self.bit_position == 8:
      self.bit_position = 0
      self.position += 1
    result = (self.data[self.position] & (1 << self.bit_position)) != 0
    self.bit_position += 1
    return result

  def align_to_byte(self):
    if self.bit_position:
      self.position += 1
      self.bit_position = 0

  def read_byte(self) -> int:
    self.align_to_byte()
    result = self.data[self.position]
    self.position += 1
    return result

  def read_short(self) -> int:
    self.align_to_byte()
    result = self.data[self.position] + (self.data[self.position + 1] << 8)
    self.position += 2
    return result

  def read_var_short(self) -> int:
    self.align_to_byte()
    num = self.data[self.position]
    if num < 128:
      self.position += 1
      return num
    result = (num & 0x7F) + (self.data[self.position + 1] << 7)
    self.position += 2
    return result

  def read_string(self) -> str:
    length = self.read_var_short()
    if length == 0:
      return ''
    result = self.data[self.position:self.position + length].decode('utf-8', errors='ignore')
    self.position += length
    return result

  def read_score_acc(self) -> ScoreAcc:
    self.align_to_byte()
    self.position += 8
    score_acc = struct.unpack("if", self.data[self.position - 8:self.position])
    return {"score": score_acc[0], "acc": score_acc[1]}

  def read_record(self, song_id: str) -> Union[list[Record], None]:
    end_position = self.position + self.data[self.position] + 1

    self.position += 1
    exists = self.data[self.position]

    self.position += 1
    fc = self.data[self.position]

    self.position += 1

    if song_id in chart_constant_list:
      constants = chart_constant_list[song_id]
      records: list[Record] = []
      
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
      
      self.position = end_position
      return records
    
    self.position = end_position
    return None

  def read_progress(self) -> PlayerProgress:
    progress: PlayerProgress = {
      "is_first_run": self.read_bool(),
      "legacy_chapter_finished": self.read_bool(),
      "already_show_collection_tip": self.read_bool(),
      "already_show_auto_unlock_in_tip": self.read_bool(),
      "completed": self.read_string(),
      "song_update_info": self.read_byte(),
      "challenge_mode_rank": self.read_short(),
      "money": [self.read_var_short() for _ in range(5)],
      "unlock_flag_of_spasmodic": self.read_byte(),
      "unlock_flag_of_igallta": self.read_byte(),
      "unlock_flag_of_rrharil": self.read_byte(),
      "flag_of_song_record_key": self.read_byte(),
      "random_version_unlocked": self.read_byte(),
      "chapter8_unlock_begin": self.read_bool(),
      "chapter8_unlock_second_phase": self.read_bool(),
      "chapter8_passed": self.read_bool(),
      "chapter8_song_unlocked": self.read_byte()
    }
    return progress