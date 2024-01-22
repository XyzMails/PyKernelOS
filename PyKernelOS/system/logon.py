import os
import json

def login():
    settings_file_path = 'files/settings/settings.json'

    try:
        with open(settings_file_path, 'r') as file:
            settings = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # Create default settings if the file is not present or empty
        settings = {
            "anonymous_mode": False
        }

    if settings["anonymous_mode"]:
        entered_username = "anonymous"
        entered_hostname = "PyKernelOS"
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        print(f"[logon]: success! welcome, {entered_username}!")
        return entered_username, entered_hostname

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        print("+----------------------------------------+")
        print("| [logon]: welcome to PyKernelOS!        |")
        print("| [logon]: options:                      |")
        print("| [logon]: 1. login to PyKernelOS        |")
        print("| [logon]: 2. exit                       |")
        print("+----------------------------------------+")
        choice = input("[logon]: enter your choice (1-2): ")

        if choice == '1':
            entered_username = input("[logon]: enter your username: ").strip()
            if not entered_username:
                print("[logon]: Invalid username. Please try again.")
                continue
                
            entered_hostname = input("[logon]: enter your hostname: ").strip()
            if not entered_hostname:
                entered_hostname = "PyKernelOS"
                
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            print(f"[logon]: success! welcome, {entered_username}!")
            return entered_username, entered_hostname
        elif choice == '2':
            print("[logon]: exiting PyKernelOS. Goodbye!")
            exit()
        else:
            print("[logon]: Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    entered_username, entered_hostname = login()
    os.system(f'python system/main.py "{entered_username}" "{entered_hostname}"')
