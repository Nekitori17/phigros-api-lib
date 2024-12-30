#!/usr/bin/env python3
import click
from colorama import *
from .Updater import DataUpdater

@click.command(help="Update the entire Phigros database.")
def main():
  init()
  ascii_art = """
+==========================================================+
|                                                          |
|   ___ _    _                   _   ___ ___ _    _ _      |
|  | _ \ |_ (_)__ _ _ _ ___ ___ /_\ | _ \_ _| |  (_) |__   |
|  |  _/ ' \| / _` | '_/ _ (_-</ _ \|  _/| || |__| | '_ \  |
|  |_| |_||_|_\__, |_| \___/__/_/ \_\_| |___|____|_|_.__/  |
|             |___/                                        |
|                                                          |
+==========================================================+
  """

  click.echo(Fore.CYAN + ascii_art + Style.RESET_ALL)
  click.echo(Fore.YELLOW + "Updating... This may take a while" + Style.RESET_ALL)

  updater = DataUpdater()
  try:
    updater.update_all()
    click.echo(Fore.GREEN + "Update completed successfully!" + Style.RESET_ALL)
  except Exception as e:
    click.echo(Fore.RED + f"An error occurred during the update: {e}" + Style.RESET_ALL)
    click.echo(Fore.RED + "Please try again or check your internet connection." + Style.RESET_ALL)

if __name__ == "__main__":
  main()
