import argparse
import asyncio
from threading import Thread

from src.digibot.controller import start_discord_server
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_discord_server())
