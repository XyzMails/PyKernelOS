import os
import sys
import time
import json

def bootloader():
    total_steps = 7
    for step in range(1, total_steps + 1):
        progress = int((step / total_steps) * 100)
        print(f"[loading os]: Initializing kernel components... ({progress}% complete)")
        time.sleep(1)

    print("[loading os]: Kernel initialization complete.")
    time.sleep(1)

    print("[loading os]: Press any key to log in.")
    input()

    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Launch logon.py if it exists, otherwise, show BSOD
    logon_script = 'system/logon.py'
    if os.path.isfile(logon_script):
        launch_logon(logon_script)
    else:
        bsod()

def launch_logon(logon_script):
    try:
        os.system(f'python {logon_script}')  # Replace 'logon.py' with the actual script name
    except FileNotFoundError as e:
        print("[uh oh! :C] You encountered an error and, for the best of it, we will turn off this OS.")
        print("[uh oh! :C] If the error still persists, you should contact our community server.")
        print("[discord]: https://discord.gg/NvrdskeTSp")
        print("[uh oh! :C] Technical Code:")
        print(f"[code {type(e).__name__}] {e}")

        sys.exit(1)  # Exit the script with an error code

def bsod():
    print("[uh oh!! ;c]: You encountered an error and, for the best of it, we will turn off this OS.")
    print("[info]: If the error still persists, you should contact our community server.")
    print("[discord]: https://discord.gg/NvrdskeTSp")
    print("[info]: Technical Code:")
    print(f"[code]: 001a")
    sys.exit(1)  # Exit the script with an error code

def load_os():
    bootloader()

def settings():
    settings_file_path = 'files/settings/settings.json'
    
    try:
        with open(settings_file_path, 'r') as file:
            settings = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # Create default settings if the file is not present or empty
        settings = {
            "debug_mode": False,
            "anonymous_mode": False
        }

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("SETTINGS")
        print("1. Debug Mode: ", "ON" if settings["debug_mode"] else "OFF")
        print("2. Anonymous Mode: ", "ON" if settings["anonymous_mode"] else "OFF")
        print("3. Save and Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            settings["debug_mode"] = not settings["debug_mode"]
        elif choice == '2':
            settings["anonymous_mode"] = not settings["anonymous_mode"]
        elif choice == '3':
            with open(settings_file_path, 'w') as file:
                json.dump(settings, file, indent=4)
            break

if __name__ == "__main__":
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("MENU")
        print("1. Load OS")
        print("2. Settings")
        print("3. Exit")

        menu_choice = input("Enter your choice (1-3): ")

        if menu_choice == '1':
            load_os()
        elif menu_choice == '2':
            settings()
        elif menu_choice == '3':
            sys.exit()
        else:
            input("Invalid choice. Press Enter to continue...")
