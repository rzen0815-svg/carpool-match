import json
import os
from pathlib import Path
from datetime import datetime


DATA_FILE = Path(os.getenv("DATA_FILE_PATH", "data.json"))


def load_requests():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_requests(requests):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(requests, f, ensure_ascii=False, indent=2)


def delete_request_by_contact(contact):
    requests_list = load_requests()
    new_list = []

    for person in requests_list:
        if person["contact"] != contact:
            new_list.append(person)

    save_requests(new_list)

    return len(new_list) != len(requests_list)


def remove_expired_requests():
    requests_list = load_requests()
    now = datetime.now()

    new_list = []

    for person in requests_list:
        request_time = datetime.strptime(person["time"], "%H:%M")

        request_time = request_time.replace(year=now.year, month=now.month, day=now.day)

        time_diff = (request_time - now).total_seconds() / 60

        if time_diff >= -30:
            new_list.append(person)

    save_requests(new_list)
