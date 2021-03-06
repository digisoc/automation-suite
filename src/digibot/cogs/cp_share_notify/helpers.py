""" Module Imports """
import re
from collections import defaultdict
from typing import Dict, List, TypedDict

import pandas as pd

""" Constants """
DATE_FORMAT = "%Y-%m-%d"
DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")
ROW_AXIS = 0
COLUMN_AXIS = 1


class ScheduleEntry(TypedDict):
    """
    A typed dictionary for a schedule entry
    """

    name: str
    event: str
    server_id: int


SCHEDULE_TYPE = Dict[str, List[ScheduleEntry]]


def parse_schedule(file_name: str, server_id: int) -> SCHEDULE_TYPE:
    """
    Parses a given CPShare schedule and returns a dictionary which maps dates (key)
    to a list of dictionaries (value) containing CP sharer information

    Args:
        file_name (str): name of schedule csv file

    Returns:
        schedule (dict): maps date (str) -> list of users (dict) where users (dict):
            name (str)
            event (str)
            server_id (int)
    """
    schedule = defaultdict(list)

    # import schedule
    df = pd.read_csv(file_name)

    # remove empty rows from end
    rows_to_drop = 0
    encountered_empty = False
    for row in df.values[::-1]:
        empty_row = all(pd.isnull(cell) for cell in row)
        if empty_row:
            encountered_empty = True
        elif encountered_empty:
            break
        rows_to_drop += 1

    df = df.head(-rows_to_drop)

    # remove fully empty columns
    df = df.dropna(how="all", axis=COLUMN_AXIS)

    # label columns
    column_labels = [
        "Event Info",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    # remove extra columns on the RHS
    df = df.iloc[:, : len(column_labels)]
    df.columns = column_labels

    # iterate through rows to extract data
    scan_date = False
    current_dates = None
    prev_event = None

    for row in df.values:
        event_info = row[0]
        cell_values = row[1:]
        is_empty_event = pd.isnull(event_info)

        # reset and scan date next iteration
        # PRIME TIME is used to indicate start of new week
        if event_info == "PRIME TIME":
            current_dates = None
            prev_event = None
            # date info is on the row after PRIME TIME
            # so toggle scan date to scan next iter
            scan_date = True
            continue

        # date row
        elif scan_date:
            current_dates = cell_values
            scan_date = False
            continue

        # normal row
        for day_index, name in enumerate(cell_values):
            if not pd.isnull(name) and name != "EVENT DAY":
                share_date = current_dates[day_index]
                print(
                    name,
                    share_date,
                    event_info if not is_empty_event else prev_event,
                )

                # add to schedule
                schedule[share_date].append(
                    {
                        "name": name,
                        "event": event_info if not is_empty_event else prev_event,
                        "server_id": server_id,
                        "schedule_file": file_name,
                    }
                )

        # store current event info for when
        # the row doesn't have any event info
        if not is_empty_event:
            prev_event = event_info

    # sort users for each day by name
    for users in schedule.values():
        users.sort(key=lambda user: user["name"])

    return schedule


if __name__ == "__main__":
    TEST_CSV_FILE = "test_schedule.csv"
    schedule = parse_schedule(TEST_CSV_FILE, -1)
    print(f"{schedule=}")
