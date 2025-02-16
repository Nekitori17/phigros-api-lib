import struct
import base64
import requests
from .Constants import *
from .Tools.DecryptSave import *
from .PyTypes.Record import Record
from .PyTypes.Best import BestRecords
from .PyTypes.Player import PlayerInfo
from .PyTypes.Profile import PlayerProfile
from .PyTypes.Summary import PlayerSummary

class PhigrosAPI:
  def __init__(self, session_token: str):
    """Initializes the PhigrosAPI client.

    Args:
        session_token (str): The session token from the ".userdata" file (property "sessionToken").
    """
    self.__httpHeaders = {
      **PHIGROS_TAPTAP_HEADER,
      "X-LC-Session": session_token
    }
    self.user_info = self.get_user()
    self.save = self.get_save()
    self.player_summary = self.get_player_summary()
    self.player_progress = self.get_player_progress()

  def get_user(self):
    """Retrieves the user's information from the Phigros API.

    Returns:
        PlayerInfo: A dictionary containing the user's information.
    """
    response = requests.get(
      f"{PHIGROS_SERVICE_BASE_URL}/users/me",
      headers= self.__httpHeaders
    )

    result: PlayerInfo = response.json()
    return result
  
  def get_player_summary(self):
    """Retrieves and parses the player's summary data from the save file.

    Returns:
        PlayerSummary: A dictionary containing the player's summary information.
    """
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
    """Retrieves the player's save data from the Phigros API.

    Returns:
        PlayerProfile: A dictionary containing the player's save data.
    """
    response = requests.get(
      f"{PHIGROS_SERVICE_BASE_URL}/classes/_GameSave",
      headers=self.__httpHeaders,
      params={"limit": 1}
    )

    data_save_list: list[PlayerProfile] = response.json().get("results")
    if len(data_save_list) == 0:
      raise Exception("No save data found")
    
    return data_save_list[0]

  def get_records(self):
    """Retrieves and decrypts the player's records from the save file.

    Returns:
        list[Record]: A list of dictionaries, each containing a record's information.
    """
    decrypted = DecryptSave(self.save["gameFile"]["url"])
    records = decrypted.decrypt_records()
    return records
  
  def get_player_progress(self):
    """Retrieves and decrypts the player's progress data from the save file.

    Returns:
        PlayerProgress: A dictionary containing the player's progress information.
    """
    decrypted = DecryptSave(self.save["gameFile"]["url"])
    player_progress = decrypted.decrypt_progress()
    return player_progress
  
  def get_best_records(self, overflow: int = 0):
    """Retrieves the player's best records, categorized into Phi, top 27, and overflow.

    Args:
        overflow (int, optional): The number of records to include in the overflow category. Defaults to 0.

    Returns:
        BestRecords: A dictionary containing three lists of records:
            - phi: A list of Phigros records (perfect scores).
            - b27: A list of the top 27 records (excluding Phigros records).
            - overflow: A list of additional records beyond the top 27, specified by the `overflow` parameter.

    Note:
        Records are sorted by their RKS value in descending order.
    """
    records = self.get_records()

    phi_records: list[Record] = [record for record in records if record["score"] == 1000000]
    phi_records.sort(key=lambda x: x["rks"], reverse=True)
    best_phi_records = phi_records[:3]

    best_phi_set = {id(record) for record in best_phi_records}
    records = [record for record in records if id(record) not in best_phi_set]
    records.sort(key=lambda x: x["rks"], reverse=True)

    best_records: BestRecords = {
      "phi": best_phi_records,
      "b27": records[0:27],
      "overflow": records[27:27 + overflow]
    }
  
    return best_records