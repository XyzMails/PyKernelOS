import os
import sys
import time
import json
import pygame
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
                print(f"{Fore.RED}[error]: no apps detected.{Style.RESET_ALL}")
                break

            self.display_apps(apps)
            if self.settings["debug_mode"]:
                choice = input(f"[{Fore.CYAN}debug.{self.entered_username}@{self.hostname}{Style.RESET_ALL}]: desktop (1-b): ").lower()
            else:
                choice = input(f"[{Fore.YELLOW}{self.entered_username}@{self.hostname}{Style.RESET_ALL}]: desktop (1-b): ").lower()

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
                    print(f"{Fore.RED}[kernel]: invalid app choice. please enter a valid number.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[kernel]: invalid input. please enter a valid choice.{Style.RESET_ALL}")

    def get_apps(self):
        try:
            apps = [file for file in os.listdir(self.apps_directory) if file.endswith(".ap3")]
            return apps
        except FileNotFoundError:
            print(f"{Fore.RED}Directory '{self.apps_directory}' not found.{Style.RESET_ALL}")
            return []

    def return_to_logon(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            os.system('python system/logon.py')  # Run logon.py
        except Exception as e:
            print(f"{Fore.RED}[kernel]: Error returning to logon: {e}{Style.RESET_ALL}")

    def reboot(self):
        try:
            for i in range(3, 0, -1):
                print(f"{Fore.YELLOW}[kernel]: rebooting in {i}{Style.RESET_ALL}")
                time.sleep(1)
            print(f"{Fore.YELLOW}[kernel]: rebooting now!{Style.RESET_ALL}")
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            subprocess.run(['python', 'bios/bootables/PyKernelOS.boot'])  # Run bootloader
        except Exception as e:
            print(f"{Fore.RED}[kernel]: Error rebooting: {e}{Style.RESET_ALL}")

    def return_to_bios(self):
        try:
            for i in range(3, 0, -1):
                print(f"{Fore.YELLOW}[kernel]: returning to bios in {i}{Style.RESET_ALL}")
                time.sleep(1)
            print("[kernel]: returning to bios now")
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            subprocess.run(['python', 'bios/bios.py'])  # Run bios.py
        except Exception as e:
            print(f"{Fore.RED}[kernel]: Error returning to bios: {e}{Style.RESET_ALL}")

    def launch_app(self, app_path):
        self.display_countdown()

        # Execute the app
        if app_path.endswith(".ap3"):
            try:
                with open(app_path, 'r') as file:
                    app_code = file.read()
                print(f"{Fore.GREEN}[kernel]: Launching!{Style.RESET_ALL}")
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
                exec(app_code)
                print(f"{Fore.GREEN}[kernel]: App executed successfully.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[kernel]: Error running the app: {e}{Style.RESET_ALL}")

            self.display_returning_message()

    def display_countdown(self):
        for i in range(3, 0, -1):
            print(f"{Fore.YELLOW}[kernel]: Launching app in {i}{Style.RESET_ALL}")
            time.sleep(1)

    def display_welcome(self):
        if self.entered_username is not None:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            print(f"+----------------------------------------+")
            print(f"|              {Fore.YELLOW}[debuginfo]:{Style.RESET_ALL}              |")
            print(f"+----------------------------------------+")
            debug_status = "true" if self.settings["debug_mode"] else "false"
            print(f"{Fore.YELLOW}[debug]: {debug_status}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[os-introduce]: welcome to PyKernelOS, {self.entered_username}!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[os-check]: user: {self.entered_username}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[os-check]: {Fore.YELLOW}host: {self.hostname}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[os-check]: {Fore.GREEN}everything seems to be OK.{Style.RESET_ALL}")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            print(f"{Fore.GREEN}[os-introduce]: welcome to PyKernelOS{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[os-check]: everything seems to be OK.{Style.RESET_ALL}")

    def display_apps(self, apps):
        print(f"+-------------------------------+")
        print(f"|            {Fore.YELLOW}[apps]:{Style.RESET_ALL}            |")
        print(f"+-------------------------------+")
        for i, app in enumerate(apps, start=1):
            print(f"[ {Fore.YELLOW}{i}{Style.RESET_ALL} ]  -  {Fore.CYAN}{app}{Style.RESET_ALL}")
        print("")

    def display_systemstuff(self):
        print(f"+---------------------------------------+")
        print(f"|                                       |")
        print(f"|           {Fore.YELLOW}[system stuff]:{Style.RESET_ALL}             |")
        print(f"|                                       |")
        print(f"| [ {Fore.CYAN}q{Style.RESET_ALL} ] - {Fore.GREEN}set OS to logon{Style.RESET_ALL}               |")
        print(f"| [ {Fore.CYAN}r{Style.RESET_ALL} ] - {Fore.GREEN}reboot{Style.RESET_ALL}                        |")
        print(f"| [ {Fore.CYAN}rf{Style.RESET_ALL} ] - {Fore.GREEN}refresh{Style.RESET_ALL}                      |")
        print(f"| [ {Fore.CYAN}b{Style.RESET_ALL} ] - {Fore.GREEN}go back to bios{Style.RESET_ALL}               |")
        print(f"|                                       |")
        print(f"+---------------------------------------+")

    def display_returning_message(self):
        print(f"{Fore.YELLOW}[kernel]: Returning to main kernel in 2 seconds...{Style.RESET_ALL}")
        time.sleep(2)

# Main
if __name__ == "__main__":
    simple_os = PyKernelOS()
    if len(sys.argv) > 2:
        entered_username = sys.argv[1]
        entered_hostname = sys.argv[2]
        simple_os.set_username(entered_username, entered_hostname)
    simple_os.run()
