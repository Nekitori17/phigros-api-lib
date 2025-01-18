from typing import TypedDict

class PlayerProgress(TypedDict):
  is_first_run: bool
  legacy_chapter_finished: bool
  already_show_collection_tip: bool
  already_show_auto_unlock_in_tip: bool
  completed: str
  song_update_info: int
  challenge_mode_rank: int
  money: list[int]
  unlock_flag_of_spasmodic: int
  unlock_flag_of_igallta: int
  unlock_flag_of_rrharil: int
  flag_of_song_record_key: int
  random_version_unlocked: int
  chapter8_unlock_begin: bool
  chapter8_unlock_second_phase: bool
  chapter8_passed: bool
  chapter8_song_unlocked: int