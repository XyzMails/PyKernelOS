import os
import json
from colorama import Fore, Style

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
        print(f"{Fore.GREEN}[logon]: success! welcome, {entered_username}!{Style.RESET_ALL}")
        return entered_username, entered_hostname

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        print("+----------------------------------------+")
        print(f"| {Fore.CYAN}[logon]: welcome to PyKernelOS!{Style.RESET_ALL}        |")
        print(f"| {Fore.YELLOW}[logon]: options:{Style.RESET_ALL}                      |")
        print(f"| {Fore.GREEN}[logon]: 1. login to PyKernelOS{Style.RESET_ALL}        |")
        print(f"| {Fore.RED}[logon]: 2. exit{Style.RESET_ALL}                       |")
        print("+----------------------------------------+")
        choice = input(f"{Fore.CYAN}[logon]: enter your choice (1-2): {Style.RESET_ALL}")

        if choice == '1':
            entered_username = input(f"{Fore.GREEN}[logon]: enter your username: {Style.RESET_ALL}").strip()
            if not entered_username:
                print(f"{Fore.RED}[logon]: Invalid username. Please try again.{Style.RESET_ALL}")
                continue

            entered_hostname = input(f"{Fore.YELLOW}[logon]: enter your hostname: {Style.RESET_ALL}").strip()
            if not entered_hostname:
                entered_hostname = "PyKernelOS"

            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            print(f"{Fore.GREEN}[logon]: success! welcome, {entered_username}!{Style.RESET_ALL}")
            return entered_username, entered_hostname
        elif choice == '2':
            print(f"{Fore.YELLOW}[logon]: exiting PyKernelOS. Goodbye!{Style.RESET_ALL}")
            exit()
        else:
            print(f"{Fore.RED}[logon]: Invalid choice. Please enter a valid option.{Style.RESET_ALL}")

if __name__ == "__main__":
    entered_username, entered_hostname = login()
    os.system(f'python system/main.py "{entered_username}" "{entered_hostname}"')
