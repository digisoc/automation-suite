import asyncio

from src.digibot.controller import start_discord_server

LOOP = None


def start_client_loop() -> None:
    # runs async function on event loop
    # NOTE: python versions > 3.10: asyncio.get_event_loop replaced with asyncio.get_running_loop
    global LOOP
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(start_discord_server())


def get_loop() -> asyncio.AbstractEventLoop:
    return LOOP


if __name__ == "__main__":
    start_client_loop()
