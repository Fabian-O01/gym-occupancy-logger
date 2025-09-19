import csv
import datetime
import time
import requests
import re
import json
import locale

URL = "https://www.fitx.de/fitnessstudios/berlin-tempelhof"

def main():
    # get gym website HTML content and extract visitor count
    r = requests.get(URL, timeout=10)
    day_match = re.search(r'data-current-day-data="(\[.*?\])"', r.text)

    if not day_match:
        raise ValueError("No data found for current day.")
    
    day_list = json.loads(day_match.group(1))
    
    # get time in correct format
    locale.setlocale(locale.LC_TIME, "de_DE")
    today = datetime.date.today().strftime("%x")

    # write data to CSV file
    with open("data/gym_log_daily.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today] + day_list)

    # also fetch predicted visitor counts for the week on monday
    if datetime.date.today().weekday() >= 0:
        week_match = re.search(r'data-visitordata="(\[\[.*?\]\])"', r.text)

        if not week_match:
            raise ValueError("No data found for current week.")
        
        week_list = json.loads(week_match.group(1))

        # write data to CSV file
        with open("data/gym_log_weekly.csv", "a", newline="") as f:
            writer = csv.writer(f)
            for i in range(7):
                date = datetime.date.fromtimestamp(time.time() + 60*60*24*i).strftime("%x") # horriffic, I know
                writer.writerow([date] + week_list[i])

if __name__ == "__main__":
    main()