import os

def display_bios_menu():
    print("[bios]: BIOS loaded")
    print("[bios]: Choose your bootable media:")

def list_bootable_media():
    bootables_folder = "bios/bootables"
    try:
        bootable_files = [file for file in os.listdir(bootables_folder) if file.endswith(".boot")]
        return bootable_files
    except FileNotFoundError:
        print(f"[bios]: Directory '{bootables_folder}' not found.")
        return []

def load_bootable_media(bootable_file):
    try:
        os.system(f'python "bios/bootables/{bootable_file}"')  # Adjust the path here
    except Exception as e:
        print(f"[bios]: Error loading bootable media: {e}")

if __name__ == "__main__":
    while True:
        display_bios_menu()
        bootable_files = list_bootable_media()

        if not bootable_files:
            print("[bios]: No bootable media found.")
            break

        for i, bootable_file in enumerate(bootable_files, start=1):
            print(f"[ {i} ] - {bootable_file}")

        choice = input("[bios]: Enter the number of your choice (q to quit): ").lower()

        if choice == 'q':
            print("[bios]: Exiting BIOS. Goodbye!")
            break
        elif choice.isdigit():
            bootable_index = int(choice)
            if 1 <= bootable_index <= len(bootable_files):
                selected_bootable = bootable_files[bootable_index - 1]
                load_bootable_media(selected_bootable)
                break
            else:
                print("[bios]: Invalid choice. Please enter a valid number.")
        else:
            print("[bios]: Invalid input. Please enter a valid choice.")
