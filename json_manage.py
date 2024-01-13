import json
import shutil
import os
import aes_implementation as aes

def append_to_json_file(filename, new_data):
    with open(filename, 'r+') as f:
        data = json.load(f)
        data.update(new_data)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def json_fix(mode, enc=True, key=None, delete_backup=False):
    backup_path = f"{os.getenv('LOCALAPPDATA')}\\Google\\Chrome\\User Data\\config_backup.json"
    original_path = "config.json"
    
    # check backup_path exists (make sure to remove the config_backup.json from the dir)
    if not os.path.exists(backup_path):
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        open(backup_path, 'w').close()

    # BACKUP MODE
    if mode == "backup":
        try:
            shutil.copyfile(original_path, backup_path)
            if enc:
                aes.encrypt_file(backup_path, key)
            return 0
        except Exception as e:
            return e
    
    # FALLBACK MODE
    elif mode == "fallback":
        if (os.path.exists(backup_path) and enc is False and key == None) or \
            (os.path.exists(backup_path + ".enc") and enc is True and key != None):  # Double check
            _, ext = os.path.splitext(backup_path)
        elif not os.path.exists(backup_path) and not os.path.exists(backup_path + ".enc"):
            return 1  # No backup found
        else:
            return 2  # Invalid Config

        if ext == '.json':
            if enc == True and key != None:
                aes.decrypt_file(backup_path, key, delete=delete_backup)
            shutil.copyfile(backup_path, original_path)
            os.remove(backup_path)
            return 0  # Success
        else:
            open(original_path, 'w').close()
            return 2  # No backup found, but a clean file was created
    else:
        return 1  # Invalid mode

def is_valid_json(file_path):
    try:
        with open(file_path, 'r') as file:
            a = json.load(file)
            try:
                a['name'] # Check if the name key exists, if no then the file is invalid
            except KeyError:
                return False
        return True
    except json.JSONDecodeError:
        return False
    except FileNotFoundError:
        return False