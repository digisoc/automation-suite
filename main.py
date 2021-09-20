import asyncio
from threading import Thread

from src.server import start_flask_server
from src.digibot.controller import start_discord_server


if __name__ == "__main__":
    # start Flask server
    # t = Thread(target=start_flask_server)
    # t.start()
    # start DigiBot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_discord_server())
