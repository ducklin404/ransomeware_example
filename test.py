import os
import winreg

def get_desktop_path():
    try:
        # Open registry key for user's Desktop path
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
            desktop_path = winreg.QueryValueEx(key, "Desktop")[0]
    except Exception as e:
        # Fallback if registry key fails
        desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
    return desktop_path

print(get_desktop_path())
