""" Module Imports """
import os
import discord
import random
from datetime import date

""" Import Helpers """
from .helpers import parse_schedule


class Task:
    def __init__(self, schedule: dict[str, list[dict[str, str]]]):
        self._schedule = schedule

    def get_schedule(self) -> dict[str, list[dict[str, str]]]:
        return self._schedule

    def set_schedule(self, schedule: dict[str, list[dict[str, str]]]) -> None:
        self._schedule = schedule
