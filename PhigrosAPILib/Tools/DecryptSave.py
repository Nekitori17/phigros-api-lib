from PhigrosAPILib.Important import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from PhigrosAPILib.PyTypes.Record import Record
from PhigrosAPILib.Tools.ByteReader import ByteReader
from PhigrosAPILib.Tools.ReadFile import SaveFileReader

def decrypt_records(url: str):
  reader_save_file = SaveFileReader(url)

  cipher = AES.new(DECRYPT_KEY, AES.MODE_CBC, DECRYPT_IV).decrypt(reader_save_file.read_record())
  record_raw = unpad(cipher, AES.block_size)

  records: list[Record] = []
  reader = ByteReader(record_raw)
  for i in range(reader.read_var_short()):
    song_id = reader.read_string()[:-2]
    record = reader.read_record(song_id)
    
    if record:
      records.extend(record)
  
  return records