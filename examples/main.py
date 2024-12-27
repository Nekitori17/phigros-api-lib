from PhigrosAPILib.Core import PhigrosAPI

client = PhigrosAPI("<<SESSION_TOKEN>>")  # Initialize PhigrosAPI client with session token
client.save                               # Player raw save data
client.player_summary                     # Player summary
client.user_info                          # Account information
client.records                            # Played song records
client.get_best_records(5)                # Best records with overflow of 5