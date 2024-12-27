import struct
import base64
import requests
from PhigrosAPILib.Important import *
from PhigrosAPILib.PyTypes.Record import Record
from PhigrosAPILib.PyTypes.Best import BestRecords
from PhigrosAPILib.PyTypes.Player import PlayerInfo
from PhigrosAPILib.PyTypes.Summary import PlayerSummary
from PhigrosAPILib.PyTypes.Profile import PlayerProfile
from PhigrosAPILib.Tools.DecryptSave import decrypt_records

class PhigrosAPI:
  def __init__(self, session_token: str):
    self.httpHeaders = {
      **PHIGROS_TAPTAP_HEADER,
      "X-LC-Session": session_token
    }
    self.user_info = self.get_user()
    self.save = self.get_save()
    self.player_summary = self.get_player_summary()
    self.records = self.get_records()

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

  def get_records(self):
    records = decrypt_records(self.save["gameFile"]["url"])
    return records
  
  def get_best_records(self, overflow: int = 0):
    records = self.records

    phi_records: list[Record] = []
    for record in records:
      if record["score"] == 1000000:
        phi_records.append(record)

    phi_records.sort(key=lambda x: x["rks"], reverse=True)

    best_phi_records = phi_records[0]

    records.remove(best_phi_records)
    records.sort(key=lambda x: x["rks"], reverse=True)

    best_records: BestRecords = {
      "phi": best_phi_records,
      "b19": records[0:19],
      "overflow": records[19:19 + overflow]
    }
  
    return best_records