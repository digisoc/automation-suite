""" Module Imports """
import re
import pandas as pd
from collections import defaultdict

""" Constants """
DATE_FORMAT = "%Y-%m-%d"
DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")
SCHEDULE_TYPE = dict[str, list[dict[str, str]]]


def notify_user(ctx, name, event, share_type) -> None:
    pass


def parse_schedule(file_name: str) -> SCHEDULE_TYPE:
    """
    Parses a given CP schedule and returns a dictionary which maps dates (key)
    to a list of dictionaries (value) containing CP sharer information

    Args:
        file_name (str): name of schedule csv file

    Returns:
        schedule (dict): maps date (str) -> list of users (dict) where users (dict):
            name (str: str)
            event (str: str)
            share_type (str: str)
    """
    schedule = defaultdict(list)

    # import schedule
    df = pd.read_csv(file_name)

    # drop first, second-last and last columns
    df = df.drop(df.columns[[0, -2, -1]], axis=1)

    # label columns
    df.columns = [
        "Event Info",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    df.head()

    # remove PRIME TIME rows
    condition = df["Event Info"] != "PRIME TIME"
    df = df[condition]

    # iterate through rows to extract data
    current_dates = None
    current_type = None
    prev_event = None

    for row in df.values:
        event_info = row[0]
        cell_values = row[1:]
        is_empty_event = pd.isnull(event_info)
        is_empty_cells = all(pd.isnull(cell) for cell in cell_values)

        if is_empty_cells and is_empty_event:
            # end of date section (full null row)
            current_dates = []

        elif is_empty_cells:
            # start of new event type (remaining cells null)
            current_type = event_info

        elif all(
            DATE_PATTERN.match(cell) is not None
            for cell in cell_values
            if not pd.isnull(cell)
        ):
            # check date row
            current_dates = cell_values

        else:
            # normal row
            for day_index, name in enumerate(cell_values):
                if not pd.isnull(name) and name != "EVENT DAY":
                    share_date = current_dates[day_index]
                    print(
                        name,
                        share_date,
                        event_info if not is_empty_event else prev_event,
                        current_type,
                    )
                    # add to schedule
                    schedule[share_date].append(
                        {
                            "name": name,
                            "event": event_info if not is_empty_event else prev_event,
                            "share_type": current_type,
                        }
                    )
            if not is_empty_event:
                prev_event = event_info

    return schedule
