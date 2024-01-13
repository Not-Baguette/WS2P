import json
import os
import json_manage as jsonm

def get_name():
    if jsonm.is_valid_json("config.json"):
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            return config["name"]
    else:
        return os.getlogin()

hello_world_response = {
    0: {"title": "Ruby here!", 
        "message": "Helloo! I'm Ruby, your personal assistant!", 
        "icon": "assets/rubygeneral.ico"},
    1: {"title": "Ruby here!", 
        "message": "Haii, Ruby's hereee for you!", 
        "icon": "assets/rubywink.ico"},
    2: {"title": "Ruby here!", 
        "message": f"Oh hey! I didn't expect you so suddenly but welcome {get_name()}!", 
        "icon": "assets/rubysparkle.ico"},
    3: {"title": f"Ruby here!", 
        "message": f"Glad to see you {get_name()}!", 
        "icon": "assets/rubyhappy.ico"},
}

red_response = {
    0: {"title": "Please know that...", 
        "message": f"I care about you, and I'm here for you. You're not alone in this {get_name()}.", 
        "icon": "assets/rubygeneral.ico"},
    1: {"title": "Remember", 
        "message": f"Your life matters, and there are people who want to help you through this {get_name()}!", 
        "icon": "assets/rubywink.ico"},
    2: {"title": "Ruby's memo for u!", 
        "message": f"Your feelings are valid! Don't let anyone tell you otherwise {get_name()}!", 
        "icon": "assets/rubysparkle.ico"},
    3: {"title": "Hey dummy! Important message for you", 
        "message": f"{get_name()}, I love you so much <3", 
        "icon": "assets/rubyhappy.ico"},
    4: {"title": "I care about you", 
        "message": "You're going to be okay!", 
        "icon": "assets/rubywink.ico"},
}

yellow_response = {
    0: {"title": "Remember", 
        "message": f"You're going to be okay {get_name()}!", 
        "icon": "assets/rubywink.ico"},
    1: {"title": "Hey read this dummy!", 
        "message": "you're not alone. im here for you <3", 
        "icon": "assets/rubywink.ico"},
    2: {"title": "Remember!", 
        "message": "You matter, and I believe in you.", 
        "icon": "assets/rubysparkle.ico"},
    3: {"title": "<3", 
        "message": f"Love you {get_name()}!", 
        "icon": "assets/rubyhappy.ico"},
}

request0_response = {
    0: {"title": "Awwww", 
        "message": f"Suree {get_name()} Give me a big hug!", 
        "icon": "assets/rubywink.ico"},
    1: {"title": "!!", 
        "message": "Hell yea, give me a big hugg!", 
        "icon": "assets/rubywink.ico"},
    2: {"title": "You bet!", 
        "message": "You don't even need to ask hehe", 
        "icon": "assets/rubysparkle.ico"},
    3: {"title": "<3", 
        "message": f"hugs you* Love you {get_name()}!", 
        "icon": "assets/rubyhappy.ico"},
}
