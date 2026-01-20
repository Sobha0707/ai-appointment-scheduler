import json
import re
from datetime import datetime, timedelta

TIMEZONE = "Asia/Kolkata"

def extract_entities(text):
    department = None
    date_phrase = None
    time_phrase = None

    # department
    if "dentist" in text.lower():
        department = "dentist"
    elif "doctor" in text.lower():
        department = "doctor"

    # date phrases
    if "next friday" in text.lower():
        date_phrase = "next friday"
    elif "tomorrow" in text.lower():
        date_phrase = "tomorrow"
    elif "next monday" in text.lower():
        date_phrase = "next monday"

    # time
    time_match = re.search(r'(\d{1,2})\s*(am|pm)', text.lower())
    if time_match:
        time_phrase = time_match.group(0)

    return department, date_phrase, time_phrase


def normalize_date(date_phrase):
    today = datetime.now()

    if date_phrase == "tomorrow":
        return today + timedelta(days=1)

    if date_phrase == "next friday":
        days_ahead = (4 - today.weekday()) % 7
        return today + timedelta(days=days_ahead + 7)

    if date_phrase == "next monday":
        days_ahead = (0 - today.weekday()) % 7
        return today + timedelta(days=days_ahead + 7)

    return None


def normalize_time(time_phrase):
    try:
        return datetime.strptime(time_phrase, "%I%p").strftime("%H:%M")
    except:
        return None


def process_text(text):
    department, date_phrase, time_phrase = extract_entities(text)

    if not department or not date_phrase or not time_phrase:
        return {
            "input": text,
            "status": "needs_clarification",
            "message": "Ambiguous or missing date/time/department"
        }

    date_obj = normalize_date(date_phrase)
    time_value = normalize_time(time_phrase)

    if not date_obj or not time_value:
        return {
            "input": text,
            "status": "needs_clarification",
            "message": "Unable to normalize date or time"
        }

    return {
        "appointment": {
            "department": department.capitalize(),
            "date": date_obj.strftime("%Y-%m-%d"),
            "time": time_value,
            "tz": TIMEZONE
        },
        "status": "ok"
    }


def main():
    results = []

    with open("input.txt", "r") as file:
        for line in file:
            text = line.strip()
            if text:
                result = process_text(text)
                results.append(result)

    with open("output.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Output saved to output.json")