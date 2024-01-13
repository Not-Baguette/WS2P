import hashlib; import json; import time; import sys; import os; import ctypes; import random as rd
import aes_implementation as aes
import json_manage as jsonm
from plyer import notification
from tools import *
from textlines import *
import multiprocessing
import checkhistory
import PIL.Image
import pyautogui
import pystray


check_every = 1  # Minutes
blocktime = 20  # Minutes
exceptions = ["open.spotify.com", "discord.com", "cdn.discordapp.com", "web.whatsapp.com", 
              "media-cgk1-1.cdn.whatsapp.net", "media.tenor.com", "media.discordapp.net"
              "discord-attachments-uploads-prd.storage.googleapis.com",]

def create_toast(title, message, icon, timeout=5):
    notification.notify(
        title=title,
        message=message,
        app_icon=resource_path(icon),
        timeout=timeout,
    )
    time.sleep(timeout + 1) # So it doesnt spam the notification

def first_run():
    with open("config.json", "w") as config_file:
            config_file.write(json.dumps({"first_run": True}))
        
    create_toast("Introduction!", f"My Name is Ruby! Nice to meet you {os.getlogin()}!", "assets/rubyexplain.ico")
    create_toast("Introduction!", "Or do you prefer other name to call you? If so please write it on the dialogbox"
                 , "assets/rubywink.ico")
        
    response = pyautogui.prompt('Enter your name please! Leave it blank if you want me to call you by your \
                                username')
    if response != "":
        jsonm.append_to_json_file("config.json", {"name": response})
    else:
        jsonm.append_to_json_file("config.json", {"name": os.getlogin()})
        response = os.getlogin()

    introduction_response = {
    0: {"title": "Introduction!",
        "message": f"Alright, {response} it is!", 
        "icon": "assets/rubysparkle.ico"},
    1: {"title": "Introduction!",
        "message": "If you need to change it, you can edit it via the system tray icon!", 
        "icon": "assets/rubyexplain.ico"},
    2: {"title": "Introduction!",
        "message": "I'm here to help you with your daily life!", 
        "icon": "assets/rubyexplain.ico"},
    3: {"title": "Introduction!",
        "message": "I am the avatar of WS2P, Windows Suicide Prevention Protocol",
        "icon": "assets/rubyexplain.ico"},
    4:  {"title": "Introduction!",
        "message": "I will make sure it's my job that you remember that you're loved!",
        "icon": "assets/rubyexplainhappy.ico"},
    5: {"title": "Processing..",
        "message": "Let me set myself up a second...",
        "icon": "assets/rubyprocessing.ico"}
    }

    for _, value in introduction_response.items():
        create_toast(value["title"], value["message"], value["icon"], timeout=5)

    insert_to_startup()
    aes.set_aes_key()

    create_toast("Last notification!", "I'm done! please note that I will periodically comment on your activities!",
                  "assets/rubysparkle.ico")

def prompt_password():
    password = pyautogui.prompt(text="If this menu is buggy, try type while holding down the window", 
                                        title="Ruby here!" , default="Enter password here")
    try:
        password = password.strip()
        bits  = password.encode("utf-8")
        key = hashlib.sha256(bits)
        hash = key.hexdigest()
    except AttributeError:
        create_toast("Ruby here!", "No password entered, try again!", "assets/rubyalert.ico")
        return
    except Exception as e:
        create_toast("Ruby here!", f"Aaaa something went wrong: {e}", "assets/rubyalert.ico")
        return
    
    return hash

def firewall_connection(exception_list, blocktime=20):  # Minutes
    exceptions = ";".join(exception_list)
    result = set_proxy_server("127.0.0.1", 8080, exceptions)
    if result != 0:
        create_toast("Ruby here!", f"Failed to set the firewall: {str(result)}", "assets/rubyalert.ico")
    else:
        create_toast("Ruby here!", "Successfully set the firewall!", "assets/rubyalert.ico")

    time.sleep(blocktime * 60)
    
    result = disable_proxy_server()
    if result != 0:
        create_toast("Ruby here!", f"Failed to disable the firewall: {str(result)}", "assets/rubyalert.ico")
    else:
        create_toast("Ruby here!", "Successfully disabled the firewall!", "assets/rubyalert.ico")

def tray_icon(run):
    def change_name(**kwargs):
        if os.path.exists("config.json"):
            response = pyautogui.prompt("Enter your name please! Leave it blank if you want me to call you by your \
                                        username")
            try:
                response = response.strip()
            except AttributeError:  # Cancelled
                create_toast("Ruby here!", "Operation Cancelled!", "assets/rubyalert.ico")
                return

            if response == "":
                response = os.getlogin()
            else:
                jsonm.append_to_json_file("config.json", {"name": response})

            create_toast("Ruby here!", f"Alright, {response} it is!", "assets/rubysparkle.ico")
        else:
            create_toast("Ruby here!", "No config.json found, please run the program again!", "assets/rubyalert.ico")

    def user_prompted_firewall():
        blocktime = pyautogui.prompt(text="How long do you want to block your internet access? (in minutes)", 
                                     title="Ruby here!" , default="20")
        if blocktime == None:
            create_toast("Ruby here!", "Operation Cancelled!", "assets/rubyalert.ico")
        else:
            try:
                firewall_connection(exception_list=exceptions, blocktime=blocktime)
                create_toast("Ruby here!", f"Firewall set for {blocktime} minutes!", "assets/rubysparkle.ico")
            except Exception as e:
                create_toast("Ruby here!", f"Aaaa something went wrong: {e}", "assets/rubyalert.ico")
    
    def user_prompted_disable_firewall():
        hash = prompt_password()

        if hash == "39987a95069f78787724b55c69acfc32ee9d32ab31fc86b83164dfb268558b2e":
            disable_proxy_server()
            create_toast("Ruby here!", "Firewall disabled!", "assets/rubysparkle.ico")
        else:
            create_toast("Ruby here!", "Wrong password, try again!", "assets/rubyalert.ico")

    def quit_ruby(icon, item):
            hash = prompt_password()
            
            # TODO: Real pw "I love Mei"
            if hash == "39987a95069f78787724b55c69acfc32ee9d32ab31fc86b83164dfb268558b2e":
                create_toast("Ruby here!", "Quitting!", "assets/rubyalert.ico")
                run.value = False
                icon.stop()
            else:
                create_toast("Ruby here!", "Wrong password, try again!", "assets/rubyalert.ico")

    # Make system tray             
    image = PIL.Image.open(resource_path("assets/icon.ico"))

    menu = pystray.Menu(
        pystray.MenuItem("Change Name", change_name),
        pystray.MenuItem("I need hugs", lambda: create_toast(**request0_response[rd.randint(0, len(request0_response) - 1)])),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Firewall connection", user_prompted_firewall),
        pystray.MenuItem("Disable Firewall", user_prompted_disable_firewall),
        pystray.MenuItem("Quit", quit_ruby),
        )

    icon = pystray.Icon("RubySSP", image, "Ruby", menu)

    icon.run()

def main():
    if sys.platform.startswith('win') and sys.argv[0].endswith(".exe"):
        # On Windows calling this function when using the compiled version is necessary else a major bug arises
        multiprocessing.freeze_support()

    # Firstrun & Running from startup
    if not(jsonm.is_valid_json("config.json")) or sys.argv[0].startswith(
        os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Microsoft", "Start Menu", "Programs")):
        # Try to get the backup to fall back, if fail then first run
        backup_status = jsonm.json_fix(mode="fallback", enc=True, key=aes.get_key())
        if backup_status != 0:
            first_run()
        
    else:
        fix_res = jsonm.json_fix(mode="backup", enc=True, key=aes.get_key())
        create_toast(**hello_world_response[rd.randint(0, len(hello_world_response) - 1)])

    # Idea - Affection Level, the more you use the computer, the more affection you get from Ruby
    
    # System tray
    run = multiprocessing.Value(ctypes.c_bool, True)  # boolean, True
    p = multiprocessing.Process(target=tray_icon, args=(run,))
    p.start()

    while run.value:
        time.sleep(check_every * 60)  # For some reason this wont work if I tried putting it on the end
        if run.value is False: # Incase the user quits while the program is sleeping
            break

        try:
            check_result = checkhistory.regular_check(timeout=check_every)
        except json.decoder.JSONDecodeError:
            fix_res = jsonm.json_fix(mode="fallback", enc=True, key=aes.get_key())
            if fix_res == 0:
                check_result = checkhistory.regular_check(timeout=check_every)
                continue
            elif fix_res == 1:
                create_toast("Help!", "Something has gone wrong while checking your history!", 
                             "assets/rubyerror.ico")

        if check_result["chrome_status"] in (0,1) and check_result["firefox_status"] in (0,1):
            continue

        elif check_result["chrome_status"] == 2 or check_result["firefox_status"] == 2:
            if check_result["red"] != []:
                create_toast("Ruby here!", "Hey...", "assets/rubyalert.ico", timeout=2)
                create_toast("Ruby here!", "I noticed you've been visiting some sites that might be harmful to you",
                              "assets/rubyalert.ico")
                create_toast("Ruby here!", "For example,", "assets/rubyalert.ico", timeout=3)
                for site in check_result["red"]:
                    create_toast("Ruby here!", site[1], "assets/rubyalert.ico")
                create_toast("Sorry!", f"I'm firewalling your internet access to spotify, discord, and whatsapp \
                             for {blocktime} minutes, please take a break!", "assets/rubyalert.ico")
                create_toast(**red_response[rd.randint(0, len(hello_world_response) - 1)])
                firewall_connection(exception_list=exceptions, blocktime=blocktime)
                create_toast("Welcome back!", "I hope you're alright now, if not please seek a friend to help",
                                "assets/rubyalert.ico")

            elif check_result["yellow"] != []:
                with open('config.json', 'r+') as file:
                    config = json.load(file)
                    warnings = config.get('warnings', [])
                    warnings.append(time.time())
                    # Remove warnings older than 1 hour
                    warnings = [w for w in warnings if time.time() - w < 3600]
                    config['warnings'] = warnings
                    file.seek(0)
                    json.dump(config, file)
                    file.truncate()

                if jsonm.is_valid_json("config.json"):
                    jsonm.json_fix(mode="backup", enc=True, key=aes.get_key())
                else:
                    jsonm.json_fix(mode="fallback", enc=True, key=aes.get_key())

                if len(warnings) >= 3:
                    create_toast("Ruby here!", "Hey...", "assets/rubyangry.ico", timeout=2)
                    create_toast("Ruby here!", f"I told you twice {get_name()}...", "assets/rubyangry.ico")
                    firewall_connection(exception_list=exceptions, blocktime=blocktime)
                    create_toast("Ruby here!", f"I'll firewall your internet for {blocktime} {get_name()}, \
                                 Please take a breather and know that I care about you", 
                                 "assets/rubyalert.ico", timeout=10)
                else:
                    create_toast("Ruby here!", "Hey...", "assets/rubyalert.ico", timeout=2)
                    create_toast("Ruby here!", "Are you alright hun? You've visited pages like-", 
                                "assets/rubyalert.ico")
                    i = 0
                    for site in check_result["yellow"]:
                        create_toast("Ruby here!", site[1], "assets/rubyalert.ico", timeout=3)
                        i += 1
                        if i == 5:
                            break
                    create_toast("Ruby here!", "I hope you're alright. If you're not, here's a message for u!", 
                                "assets/rubyalert.ico")
                    create_toast(**yellow_response[rd.randint(0, len(hello_world_response) - 1)])
                    

            elif check_result["chrome_status"] == 3 or check_result["firefox_status"] == 3:  # Overriden if 2 is detected
                create_toast("Ruby here!", "Hey...", "assets/rubyalert.ico", timeout=2)
                create_toast("Ruby here!", "I noticed some abnormalities on my checks", "assets/rubyalert.ico")
                create_toast("Ruby here!", "Please don't tamper with the files if you were!", "assets/rubyangry.ico")
                create_toast("Ruby here!", "If you weren't, enjoy your day! I hope this issue isnt persistent!", 
                            "assets/rubyhappy.ico", timeout=10)

        if jsonm.is_valid_json("config.json"):
            jsonm.json_fix(mode="backup", enc=True, key=aes.get_key())
        else:
            jsonm.json_fix(mode="fallback", enc=True, key=aes.get_key())

if __name__ == "__main__":
    main()
