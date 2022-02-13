import argparse
import asyncio
from threading import Thread

from src.digibot.controller import start_discord_server
from src.loop import start_client_loop
from src.server import start_flask_server

parser = argparse.ArgumentParser("DigiBot")
parser.add_argument(
    "-f",
    "--flask",
    action="store_true",
    help="Start a Flask server on a separate thread",
)
args = parser.parse_args()

if __name__ == "__main__":
    # start Flask server
    if args.flask:
        t = Thread(target=start_flask_server)
        t.start()
    # start DigiBot
    start_client_loop()
