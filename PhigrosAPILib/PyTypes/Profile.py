from datetime import datetime
from typing import TypedDict

class MetaData(TypedDict):
  _checksum: str
  prefix: str
  size: int


class GameFile(TypedDict):
  __type: str
  bucket: str
  createdAt: datetime
  key: str
  metaData: MetaData
  mime_type: str
  name: str
  objectId: str
  provider: str
  updatedAt: datetime
  url: str

class ModifiedAt(TypedDict):
  __type: str
  iso: str


class User(TypedDict):
  __type: str
  className: str
  objectId: str

class PlayerProfile(TypedDict):
  createdAt: datetime
  gameFile: GameFile
  modifiedAt: ModifiedAt
  name: str
  objectId: str
  summary: str
  updatedAt: datetime
  user: User
