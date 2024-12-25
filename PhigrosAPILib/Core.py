import json
import struct
import base64
import requests
from Important import *
from PyTypes.Player import PlayerInfo
from PyTypes.Profile import PlayerProfile
from PyTypes.Summary import PlayerSummary
from Tools.DecryptSave import decrypt_record

class PhigrosAPI:
  def __init__(self, session_token: str):
    self.httpHeaders = {
      **PHIGROS_TAPTAP_HEADER,
      "X-LC-Session": session_token
    }
    self.user_info = self.get_user()
    self.save = self.get_save()
    self.player_summary = self.get_player_summary()

  def get_user(self):
    response = requests.get(
      f"{PHIGROS_SERVICE_BASE_URL}/users/me",
      headers= self.httpHeaders
    )

    result: PlayerInfo = response.json()
    return result
  
  def get_player_summary(self):
    result = self.save
    username = self.user_info["nickname"]
    updatedAt = result["updatedAt"]
    url = result["gameFile"]["url"]

    summary = base64.b64decode(result["summary"])
    summary = struct.unpack("=BHfBx%ds12H" % summary[8], summary)
    player_summary: PlayerSummary = {
      "username": username,
      "updated_at": updatedAt,
      "url": url,
      "save_ver": summary[0],
      "challenges": summary[1],
      "rks": summary[2],
      "display_rks": f"{summary[2]:.2f}",
      "game_ver": summary[3],
      "avatar": summary[4].decode(),
      "completion": {
        "EZ": summary[5:8],
        "HD": summary[8:11],
        "IN": summary[11:14],
        "AT": summary[14:17]
      }
    }

    return player_summary

  def get_save(self):
    response = requests.get(
      f"{PHIGROS_SERVICE_BASE_URL}/classes/_GameSave",
      headers=self.httpHeaders,
      params={"limit": 1}
    )

    data_save_list: list[PlayerProfile] = response.json().get("results")
    if len(data_save_list) == 0:
      raise Exception("No save data found")
    
    return data_save_list[0]

  def get_record(self):
    return decrypt_record(self.save["gameFile"]["url"])
  
  
client = PhigrosAPI("uucc0dsqyist6aaji8ttji401")
print(json.dumps(client.get_record(), indent=2))