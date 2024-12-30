## Phigros API Lib

A python package for accessing to phigros api

## Installation
```bash
pip install PhigrosAPILib
```

## Usage
```py
from PhigrosAPILib.Core import PhigrosAPI

client = PhigrosAPI("<<SESSION_TOKEN>>")  # Initialize PhigrosAPI client with session token
client.save                               # Player raw save data
client.player_summary                     # Player summary
client.user_info                          # Account information
client.records                            # Played song records
client.get_best_records(5)                # Best records with overflow of 5
```

## Update

Update song and chart database

```bash
$ > updatePhiDB
```

or

```py

from PhigrosAPILib.Updater import DataUpdater

updater = DataUpdater()
updater.update_all()
```

## Credit

[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)

[Phigros Source](https://github.com/7aGiven/Phigros_Resource)