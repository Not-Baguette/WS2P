# WS2P
Windows Suicide Preventation Protocol, to stop you or anyone from suicides or act as a parental control
<p align="center">
  <img width=300 height=300 src="https://github.com/Not-Baguette/WS2P/assets/94969176/3aab3df2-04aa-4567-8614-4498f8ae6683" alt="Ruby"/>
</p>

<sub>Current version: 1.0.3 Alpha [UNSTABLE]</sub>
## Features & Usage
- Firewall any connections during a crisis
- System tray icon
- Friendly & Cute avatar <3
- Browser checks
- A quite persistent app so it is hard to remove (incase the user wants to delete her to stop her from stopping them)
- Json auto backup/rollback feature (Self-repair)
- Configureable firewall time, check time, and blocked sites/keywords via source code
- Configureable authority access via source code
- Cheer up messages when you're down
- Nearly no UI since it works seamlessly on your background and communicates via Toast notifications
- Run at Startup so you don't need to bother reopening her every single restart

This is Ruby's System Tray
![Tray](https://github.com/Not-Baguette/WS2P/assets/94969176/f42a2d1d-6185-4111-9c2f-db3e8e42586d)
But do not be fooled! You cannot just disable the firewall or quit that easily, you will be prompted with a password that is hashed in the code via SHA-256. However you can ask to change your name, hugs, or firewall your connection off.

## How to run
Before you run this, you must fulfill the compatibility (and requirements if you're running via source code)
### Compatibility (Before you run)
- Windows 11 [Tested]
- Windows 10 [Should be working fine too]
Should also be running either `Chrome` or `Firefox` but other browsers should be easy to integrate

### Requirements (For running via source code)
For requirements, it should work with python 3.9 (theoritically) or up, but 3.12.0 is used for development. you can check [requirements.txt](https://github.com/Not-Baguette/WS2P/blob/main/requirements.txt) for required packages.

### Source Code
- Install python from [the Official site](https://www.python.org/)
- Run `pip install requirements.txt` on the download directory
- Run `main.py`

### Compiled version
- Run `main.exe`

## Compile
The code is currently **compatible** with pyinstaller. You can compile via pyinstaller via this command below
```
pyinstaller -F -w --hidden-import "cryptography" --hidden-import "plyer.platforms.win.notification" --add-data "assets/*.ico;assets" --add-binary "assets;assets" -i assets/icon.ico main.py
```

## Ideas for the future
- Play games with Ruby
- More text lines for Ruby
- Random chat topics
- Affection level
- Self-update
- And yes this is getting more similar to `DDLC: Monika After Story`

## Credits
- [Ruby Source Image](https://picrew.me/en/image_maker/494736)
- [exhq for the idea](https://github.com/MirageLink/miragedaemon/commit/410369ec6f6ef61f781dd26804a007334fff92dc)
