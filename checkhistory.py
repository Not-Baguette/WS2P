import os
import shutil
import sqlite3
import csv
import json
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from urllib.parse import urlparse


def get_chrome_history():
    try:
        if os.path.exists("C:\\temp\\.tempcache.csv"):
            os.remove("C:\\temp\\.tempcache.csv")
    except Exception:  # NOQA
        pass
    
    try:
        # base path for Chrome"s User Data directory
        base_path = os.path.join(os.getenv("APPDATA"), "..\\Local\\Google\\Chrome\\User Data")

        # list all subdirectories in the User Data directory
        profiles = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d)) and (d.startswith("Profile") or d == "Default")]

        for profile in profiles:
            history_path = os.path.join(base_path, profile, "History")
            if os.path.exists(history_path):
                temp_history_path = os.path.join("C:\\temp", f"{profile}_History")
                shutil.copyfile(history_path, temp_history_path)

                # connect to the SQLite database
                conn = sqlite3.connect(temp_history_path)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, last_visit_time FROM urls")

                def chrome_time_to_datetime(chrome_time):
                    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)
                rows = [(url, title, chrome_time_to_datetime(int(last_visit_time))) for url, title, last_visit_time in cursor.fetchall()]

                # write to csv file but don"t delete the previous data
                with open("C:\\temp\\.tempcache.csv", mode="a", newline="", encoding="utf-8") as decrypt_password_file:
                    decrypt_password_writer = csv.writer(decrypt_password_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    decrypt_password_writer.writerows(rows)

                # close the database connection
                conn.close()
    except Exception:  # NOQA
        pass
    
def get_firefox_history():
    try:
        if os.path.exists("C:\\temp\\.tempcache2.csv"):
            os.remove("C:\\temp\\.tempcache2.csv")
    except Exception:  # NOQA
        pass

    try:
        # base path for Firefox"s User Data directory
        base_path = os.path.join(os.getenv("APPDATA"), "..\\Roaming\\Mozilla\\Firefox\\Profiles")

        # list all subdirectories in the User Data directory
        profiles = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

        for profile in profiles:
            history_path = os.path.join(base_path, profile, "places.sqlite")
            if os.path.exists(history_path):
                temp_history_path = os.path.join("C:\\temp", f"{profile}_places.sqlite")
                shutil.copyfile(history_path, temp_history_path)

                # connect to the SQLite database
                conn = sqlite3.connect(temp_history_path)
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT url, title, last_visit_date FROM moz_places")
                except sqlite3.OperationalError:
                    break

                def firefox_time_to_datetime(firefox_time):
                    return datetime(1970, 1, 1) + timedelta(microseconds=firefox_time)
                
                rows = [(url, title, firefox_time_to_datetime(int(last_visit_date)) if last_visit_date is not None else None) for url, title, last_visit_date in cursor.fetchall()]
        
                # write to csv file but don"t delete the previous data
                with open("C:\\temp\\.tempcache2.csv", mode="a", newline="", encoding="utf-8") as decrypt_password_file:
                    decrypt_password_writer = csv.writer(decrypt_password_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    decrypt_password_writer.writerows(rows)

                # close the database connection
                conn.close()
    except Exception:  # NOQA
        pass

def wipe_extra_data(browser, delete_before=2):
    browser = browser.lower().strip()

    if browser == "firefox":
        filename = "C:\\temp\\.tempcache2.csv"
    elif browser == "chrome":
        filename = "C:\\temp\\.tempcache.csv"
    else:
        return "Invalid browser"
    
    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    # filter out rows where the date is older than X minutes (counting on utc+0)
    rows = [row for row in rows if parse((row[2] if row[2] else "1970-01-01T00:00:00") + "+00:00") > datetime.now(timezone.utc) - timedelta(minutes=delete_before)]
    # write the remaining rows back to the CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def history_manual_check():
    # TODO: Maybe set it up so news websites wont block you
    red_set_website = set()
    yellow_set_website = set()

    red_set_title = {"kill myself", "suicide", "cyanide", "suicidal", "end my life", "escape from pain", 
                        "can't take it anymore", "want to die", "suicide methods","final goodbye", "last resort", 
                        "end it all", "tie a noose"
                        }
    yellow_set_title = {"self-harm", "self-injury", "hopeless", "depressed", "lonely", "no one cares",
                           "overdose", "hanging", "drowning", "demoralized", "lost all hope", "withdrawal from life", 
                            "social withdrawal",  "dying inside", "want to disappear", "feeling numb", 
                            "emotional numbness", "emotionally numb", "no emotions", 
                            }

    """
    INFO: 
    INFORMATION:
    chrome_status/firefox_status:
    0 = No file
    1 = File exists but no data
    2 = File exists and has data
    3 = Tampered file
    """
    report_dict = {
        "chrome_status": None,
        "firefox_status": None,
        "red": [],
        "yellow": [],
    }

    def manage_status(csv_path, status_key, detected_key):
        if detected_key not in config:
            config[detected_key] = os.path.exists(csv_path)
            with open("config.json", "w") as file:
                json.dump(config, file)

        if config.get(detected_key):
            if os.path.exists(csv_path):
                with open(csv_path, "r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                    if rows:
                        report_dict[status_key] = 2
                        for row in rows:
                            parsed_uri = urlparse(row[0])
                            domain = "{uri.netloc}".format(uri=parsed_uri).replace("www.", "")
                            title = row[1].lower()
                            if any(domain.startswith(keyword) for keyword in red_set_website):
                                report_dict["red"].append(row)
                            elif any(domain.startswith(keyword) for keyword in yellow_set_website):
                                report_dict["yellow"].append(row)
                            elif any(keyword in title for keyword in red_set_title):
                                report_dict["red"].append(row)
                            elif any(keyword in title for keyword in yellow_set_title):
                                report_dict["yellow"].append(row)
                    else:
                        report_dict[status_key] = 1
            else:
                report_dict[status_key] = 3
        else:
            report_dict[status_key] = 0

    # Load the config file
    if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            config = json.load(file)
    else:
        config = {}

    manage_status("C:\\temp\\.tempcache.csv", "chrome_status", "chrome_detected")
    manage_status("C:\\temp\\.tempcache2.csv", "firefox_status", "firefox_detected")

    return report_dict

def regular_check(timeout=2):  # Timeout in minutes
    get_chrome_history()
    get_firefox_history()
    wipe_extra_data("chrome", timeout)
    wipe_extra_data("firefox", timeout)
    return history_manual_check()  # Separated so it'd be easier to debug
