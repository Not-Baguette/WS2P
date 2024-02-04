import shutil
import os
import sys
import winreg
import subprocess

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # Running as bundled executable
        base_path = sys._MEIPASS
    else:
        # Running as standalone script
        base_path = os.path.abspath("")

    return os.path.join(base_path, relative_path)

def insert_to_startup():
    # copy the file to C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\programs\\{FILE_NAME}
    PATH = sys.argv[0]
    target_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "programs")
    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    # Incase the file is already in it, else copy it
    try:
        shutil.copy(PATH, target_path)
    except shutil.SameFileError:
        # Kill the task
        subprocess.run(['taskkill', '/F', '/IM', os.path.basename(PATH)], check=True)
        # Delete the file
        os.remove(os.path.join(target_path, os.path.basename(PATH)))
        # Copy the file again
        shutil.copy(PATH, target_path)

    user = os.getlogin()
    # Check if it's run as .py or .exe
    if sys.argv[0].endswith(".py"):
        FILE_NAME = sys.argv[0][sys.argv[0].rfind("/") + 1:]
    else:
        FILE_NAME = sys.argv[0][sys.argv[0].rfind("\\") + 1:]

    # Open the key, this would raise an WindowsError if the key doesn't exist
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0,
                             winreg.KEY_ALL_ACCESS)
    except WindowsError:
        # Create the key since it does not exist
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run")

    # Set the value on Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    winreg.SetValueEx(key, "Ruby Autorun", 0, winreg.REG_SZ,
                      f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\programs\\{FILE_NAME}")
    winreg.CloseKey(key)

def set_proxy_server(proxy_server, port, exceptions):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\\Microsoft\Windows\\CurrentVersion\\Internet Settings",
                                0, winreg.KEY_WRITE)

            # Set the proxy server address and port
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, f"{proxy_server}:{port}")
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, exceptions)
            winreg.CloseKey(key)

            return 0
        except Exception as e:
            return e

def disable_proxy_server():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings',
                            0, winreg.KEY_WRITE)

        # Disable the "use a proxy server for your LAN" option
        winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)

        return 0
    except Exception as e:
        return e
