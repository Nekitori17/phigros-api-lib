import requests
from io import BytesIO
from zipfile import ZipFile

class SaveFileReader:
  def __init__(self, url: str):
    self.url = url
    self.zip_file = requests.get(url).content

  def read_record(self) -> bytes:
    with ZipFile(BytesIO(self.zip_file)) as zf:
      with zf.open("gameRecord") as game_record:
        if game_record.read(1) != b"\x01":
          raise Exception("Invalid record")
        return game_record.read()

  def read_progress(self) -> bytes:
    with ZipFile(BytesIO(self.zip_file)) as zf:
      with zf.open("gameProgress") as game_progress:
        return game_progress.read()

  def read_user(self) -> bytes:
    with ZipFile(BytesIO(self.zip_file)) as zf:
      with zf.open("user") as user:
        return user.read()