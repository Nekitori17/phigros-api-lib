#!/usr/bin/env python3
import click
from PhigrosAPILib.Updater import Updater

@click.command(help="Update the entire Phigros database.")
def main():
    updater = Updater()
    updater.update_all()
    click.echo("Updated song info and chart constants")

if __name__ == "__main__":
    main()