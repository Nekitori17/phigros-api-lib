from typing import TypedDict

class Taptap(TypedDict):
  access_token: str
  avatar: str
  kid: str
  mac_algorithm: str
  mac_name: str
  name: str
  openid: str
  token_type: str
  unionid: str

class AuthData(TypedDict):
  taptap: Taptap

class PlayerInfo(TypedDict):
  ACL: any
  authData: AuthData
  avatar: str
  createAt: str
  emailVerified: bool
  mobilePhoneVerified: bool
  nickname: str
  objectId: str
  sessionToken: str
  shortId: str
  updatedAt: str
  username: str