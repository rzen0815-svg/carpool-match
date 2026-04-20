from datetime import datetime, timedelta


def create_request(contact, date_str, time_str, destination, group_size):
    if destination not in ["福州站", "福州南站"]:
        raise ValueError("目的地只能是 福州站 或 福州南站")

    if group_size not in ["2", "3"]:
        raise ValueError("可接受人数只能是 2 或 3")

    try:
        request_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("日期或时间无效，请重新选择")

    now = datetime.now()

    if request_dt < now - timedelta(minutes=30):
        raise ValueError("这个时间已经过去太久了，请重新选择")

    if request_dt > now + timedelta(days=3):
        raise ValueError("目前最多只能预约未来三天内的拼车")

    request = {
        "contact": contact,
        "date": date_str,
        "time": time_str,
        "destination": destination,
        "group_size": group_size,
    }

    return request


def parse_datetime(person):
    return datetime.strptime(f'{person["date"]} {person["time"]}', "%Y-%m-%d %H:%M")


def can_match_two_people(person1, person2, max_minutes=20):
    if person1["destination"] != person2["destination"]:
        return False

    if person1["date"] != person2["date"]:
        return False

    if person1["group_size"] != "2" or person2["group_size"] != "2":
        return False

    dt1 = parse_datetime(person1)
    dt2 = parse_datetime(person2)

    time_diff = abs((dt1 - dt2).total_seconds()) / 60
    if time_diff > max_minutes:
        return False

    return True


def can_match_three_people(person1, person2, person3, max_minutes=20):
    if person1["destination"] != person2["destination"]:
        return False
    if person1["destination"] != person3["destination"]:
        return False

    if person1["date"] != person2["date"]:
        return False
    if person1["date"] != person3["date"]:
        return False

    if person1["group_size"] != "3":
        return False
    if person2["group_size"] != "3":
        return False
    if person3["group_size"] != "3":
        return False

    times = [
        parse_datetime(person1),
        parse_datetime(person2),
        parse_datetime(person3),
    ]
    earliest_time = min(times)
    latest_time = max(times)

    time_diff = (latest_time - earliest_time).total_seconds() / 60
    if time_diff > max_minutes:
        return False

    return True


def match_requests(requests):
    matched_groups = []
    used_contacts = set()

    for i in range(len(requests)):
        for j in range(i + 1, len(requests)):
            for k in range(j + 1, len(requests)):
                person1 = requests[i]
                person2 = requests[j]
                person3 = requests[k]

                if person1["contact"] in used_contacts:
                    continue
                if person2["contact"] in used_contacts:
                    continue
                if person3["contact"] in used_contacts:
                    continue

                if can_match_three_people(person1, person2, person3):
                    matched_groups.append([person1, person2, person3])
                    used_contacts.add(person1["contact"])
                    used_contacts.add(person2["contact"])
                    used_contacts.add(person3["contact"])

    for i in range(len(requests)):
        for j in range(i + 1, len(requests)):
            person1 = requests[i]
            person2 = requests[j]

            if person1["contact"] in used_contacts:
                continue
            if person2["contact"] in used_contacts:
                continue

            if can_match_two_people(person1, person2):
                matched_groups.append([person1, person2])
                used_contacts.add(person1["contact"])
                used_contacts.add(person2["contact"])

    waiting_list = []
    for person in requests:
        if person["contact"] not in used_contacts:
            waiting_list.append(person)

    return matched_groups, waiting_list
