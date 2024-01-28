import os
import sys
import time
import json
import platform
import requests
import subprocess
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from colorama import Fore, Style

class PyKernelOS:
    def __init__(self):
        self.apps_directory = "apps"
        self.entered_username = None
        self.hostname = None
        self.settings = self.load_settings()



    def load_settings(self):
        settings_file_path = 'files/settings/settings.json'
        try:
            with open(settings_file_path, 'r') as file:
                settings = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # Create default settings if the file is not present or empty
            settings = {
                "debug_mode": False
            }

        return settings

    def set_username(self, entered_username, entered_hostname):
        self.entered_username = entered_username
        self.hostname = entered_hostname

    def run(self):
        while True:
            self.display_welcome()
            print(" ")
            apps = self.get_apps()
            self.display_systemstuff()
            print(" ")

            if not apps:
                print("[error]: no apps detected.")
                break

            self.display_apps(apps)
            if self.settings["debug_mode"]:
                choice = input(f"[debug.{self.entered_username}@{self.hostname}]: desktop (1-b): ").lower()
            else:
                choice = input(f"[{self.entered_username}@{self.hostname}]: desktop (1-b): ").lower()

            if choice == 'q':
                print("[kernel]: setting OS mode to logon.")
                self.return_to_logon()
                break
            if choice == 'r':
                self.reboot()
                break
            elif choice == 'rf':
                continue
            if choice == 'b':
                self.return_to_bios()
                break
            elif choice.isdigit():
                app_index = int(choice)
                if 1 <= app_index <= len(apps):
                    app_path = os.path.join(self.apps_directory, apps[app_index - 1])
                    self.launch_app(app_path)
                else:
                    print("[kernel]: invalid app choice. please enter a valid number.")
            else:
                print("[kernel]: invalid input. please enter a valid choice.")

    def get_apps(self):
        try:
            apps = [file for file in os.listdir(self.apps_directory) if file.endswith(".ap3")]
            return apps
        except FileNotFoundError:
            print(f"Directory '{self.apps_directory}' not found.")
            return []

    def return_to_logon(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            os.system('python system/logon.py')  # Run logon.py
        except Exception as e:
            print("[kernel]: Error returning to logon:", e)

    def reboot(self):
        try:
            for i in range(3, 0, -1):
                print(f"[kernel]: rebooting in {i}")
                time.sleep(1)
            print("[kernel]: rebooting now!")
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            subprocess.run(['python', 'bios/bootables/PyKernelOS.boot'])  # Run bootloader
        except Exception as e:
            print("[kernel]: Error rebooting:", e)

    def return_to_bios(self):
        try:
            for i in range(3, 0, -1):
                print(f"[kernel]: returning to bios in {i}")
                time.sleep(1)
            print("[kernel]: returning to bios now")
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            subprocess.run(['python', 'bios/bios.py'])  # Run bios.py
        except Exception as e:
            print("[kernel]: Error returning to bios:", e)

    def launch_app(self, app_path):
        self.display_countdown()

        # Execute the app
        if app_path.endswith(".ap3"):
            try:
                with open(app_path, 'r') as file:
                    app_code = file.read()
                print("[kernel]: Launching!")
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
                exec(app_code)
                print("[kernel]: App executed successfully.")
            except Exception as e:
                print("[kernel]: Error running the app:", e)

            self.display_returning_message()

    def display_countdown(self):
        for i in range(3, 0, -1):
            print(f"[kernel]: Launching app in {i}")
            time.sleep(1)

    def display_welcome(self):
        if self.entered_username is not None:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            print("+----------------------------------------+")
            print("|              [debuginfo]:              |")
            print("+----------------------------------------+")
            debug_status = "true" if self.settings["debug_mode"] else "false"
            print(f"[debug]: {debug_status}")
            print(f"[os-introduce]: welcome to PyKernelOS, {self.entered_username}!")
            print(f"[os-check]: user: {self.entered_username}")
            print(f"[os-check]: host: {self.hostname}")
            print("[os-check]: everything seems to be OK.")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            print("[os-introduce]: welcome to PyKernelOS")
            print("[os-check]: everything seems to be OK.")

    def display_apps(self, apps):
        print("+-------------------------------+")
        print("|            [apps]:            |")
        print("+-------------------------------+")
        for i, app in enumerate(apps, start=1):
            print(f"[ {i} ]  -  {app}")
        print("")

    def display_systemstuff(self):
        print("+---------------------------------------+")
        print("|                                       |")
        print("|           [system stuff]:             |")
        print("|                                       |")
        print("| [ q ] - set OS to logon               |")
        print("| [ r ] - reboot                        |")
        print("| [ rf ] - refresh                      |")
        print("| [ b ] - go back to bios               |")
        print("|                                       |")
        print("+---------------------------------------+")

    def display_returning_message(self):
        print("[kernel]: Returning to main kernel in 2 seconds...")
        time.sleep(2)

# Main
if __name__ == "__main__":
    simple_os = PyKernelOS()
    if len(sys.argv) > 2:
        entered_username = sys.argv[1]
        entered_hostname = sys.argv[2]
        simple_os.set_username(entered_username, entered_hostname)
    simple_os.run()
