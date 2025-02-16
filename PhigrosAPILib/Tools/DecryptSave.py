from ..Constants import *
from .ByteReader import ByteReader
from ..PyTypes.Record import Record
from .ReadFile import SaveFileReader
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class DecryptSave:
  def __init__(self, url: str) -> None:
    self.save_file = SaveFileReader(url)

  def decrypt_records(self):
    cipher = AES.new(DECRYPT_KEY, AES.MODE_CBC, DECRYPT_IV).decrypt(self.save_file.read_record())
    record_raw = unpad(cipher, AES.block_size)

    records: list[Record] = []
    reader = ByteReader(record_raw)
    for i in range(reader.read_var_short()):
      song_id = reader.read_string()[:-2]
      record = reader.read_record(song_id)
      
      if record:
        records.extend(record)
    
    return records
  
  def decrypt_progress(self):
    cipher = AES.new(DECRYPT_KEY, AES.MODE_CBC, DECRYPT_IV).decrypt(self.save_file.read_progress()[1:])
    progress_raw = unpad(cipher, AES.block_size)
    
    decipher = ByteReader(progress_raw)
    player_profile = decipher.read_progress()

    return player_profile