import base64

PHIGROS_SERVICE_BASE_URL = "https://rak3ffdi.cloud.tds1.tapapis.cn/1.1"
PHIGROS_TAPTAP_HEADER = {
  "X-LC-Id": "rAK3FfdieFob2Nn8Am",
  "X-LC-Key": "Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0",
  "User-Agent": "LeanCloud-CSharp-SDK/1.0.3",
  "Accept": "application/json",
}

PHIGROS_FANDOM_WIKI_SONG_DATA_URL = "https://phigros.fandom.com/wiki/Phigros_Wiki:Song_Data?action=edit"

DECRYPT_KEY = base64.b64decode("6Jaa0qVAJZuXkZCLiOa/Ax5tIZVu+taKUN1V1nqwkks=")
DECRYPT_IV = base64.b64decode("Kk/wisgNYwcAV8WVGMgyUw==")