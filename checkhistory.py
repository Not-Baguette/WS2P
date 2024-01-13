import os
import shutil
import sqlite3
import csv
import json
import json_manage as jsonm
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from urllib.parse import urlparse

chrome_base_path = os.path.join(os.getenv("APPDATA"), "..\\Local\\Google\\Chrome\\User Data")
chromium_base_path = os.path.join(os.getenv("APPDATA"), "..\\Local\\Chromium\\User Data")
firefox_base_path = os.path.join(os.getenv("APPDATA"), "..\\Roaming\\Mozilla\\Firefox\\Profiles")

def get_browser_history_chromium(base_path, abv_name):
    try:
        if os.path.exists(f"C:\\temp\\.tempcache{abv_name}.csv"):
            os.remove(f"C:\\temp\\.tempcache{abv_name}.csv")
    except Exception:  # NOQA
        pass

    try:
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
                with open(f"C:\\temp\\.tempcache{abv_name}.csv", mode="a", newline="", encoding="utf-8") as decrypt_password_file:
                    decrypt_password_writer = csv.writer(decrypt_password_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    decrypt_password_writer.writerows(rows)

                # close the database connection
                conn.close()
                return True
    except Exception:  # NOQA
        return False

def get_firefox_history(base_path, abv_name):
    try:
        if os.path.exists(f"C:\\temp\\.tempcache{abv_name}.csv"):
            os.remove(f"C:\\temp\\.tempcache{abv_name}.csv")
    except Exception:  # NOQA
        pass

    try:
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
                with open(f"C:\\temp\\.tempcache{abv_name}.csv", mode="a", newline="", encoding="utf-8") as decrypt_password_file:
                    decrypt_password_writer = csv.writer(decrypt_password_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    decrypt_password_writer.writerows(rows)

                # close the database connection
                conn.close()
                return True
    except Exception:  # NOQA
        return False

def wipe_extra_data(browser, delete_before=2):
    browser = browser.lower().strip()

    if browser == "firefox":
        filename = "C:\\temp\\.tempcache2.csv"
    elif browser == "chrome":
        filename = "C:\\temp\\.tempcache1.csv"
    elif browser == "chromium":
        filename = "C:\\temp\\.tempcache1a.csv"
    else:
        return False
    
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
        # filter out rows where the date is older than X minutes (counting on utc+0)
        rows = [row for row in rows if parse((row[2] if row[2] else "1970-01-01T00:00:00") + "+00:00") > datetime.now(timezone.utc) - timedelta(minutes=delete_before)]
        # write the remaining rows back to the CSV file
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        return True
    except Exception:  # NOQA
        return False

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
    3 = Tampered files
    """
    report_dict = {
        "chrome_status": None,
        "chromium_status": None,
        "firefox_status": None,
        "red": [],
        "yellow": [],
    }

    status = {
        "chrome_detected": None,
        "chromium_detected": None,
        "firefox_detected": None,
        }

    def detect():
        # TODO: Optimize this later
        if os.path.exists(chrome_base_path):
            status["chrome_detected"] = True
        else:
            status["chrome_detected"] = False

        if os.path.exists(chromium_base_path):
            status["chromium_detected"] = True

        else:
            status["chromium_detected"] = False

        if os.path.exists(firefox_base_path):
            status["firefox_detected"] = True
        else:
            status["firefox_detected"] = False

        return status

    def check_hist(csv_path, status_key, json_detected_key, local_detected_key):
        # Tamper check
        if config.get(json_detected_key) is local_detected_key:
            pass
        elif config.get(json_detected_key) == None and local_detected_key is True:
            jsonm.append_to_json_file("config.json", {json_detected_key: local_detected_key})  # Installed
        else:
            report_dict[status_key] = 3
            
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
    
    try:
        status = detect()
        # Load the config file
        if os.path.exists("config.json"):
            with open("config.json", "r") as file:
                config = json.load(file)
        else:
            config = {}

        if status["chrome_detected"]:
            check_hist("C:\\temp\\.tempcache1.csv", "chrome_status", "chrome_detected", status["chrome_detected"])
        if status["chromium_detected"]:
            check_hist("C:\\temp\\.tempcache1a.csv", "chromium_status", "chromium_detected", status["chromium_detected"])
        if status["firefox_detected"]:
            check_hist("C:\\temp\\.tempcache2.csv", "firefox_status", "firefox_detected", status["firefox_detected"])
    except Exception as e:  # NOQA
        print("Error", e)

    return report_dict

def regular_check(timeout=2):  # Timeout in minutes
    ch_res = get_browser_history_chromium(chrome_base_path, "1")
    ch2_res = get_browser_history_chromium(chromium_base_path, "1a")
    ff_res = get_firefox_history(firefox_base_path, "2")

    if ch_res:
        wipe_extra_data("chrome", timeout)
    if ch2_res:
        wipe_extra_data("chromium", timeout)
    if ff_res:
        wipe_extra_data("firefox", timeout)

    return history_manual_check()  # Separated so it'd be easier to debug