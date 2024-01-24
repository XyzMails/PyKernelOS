import os
import requests
import zipfile
import shutil

def download_and_extract():
    try:
        # Download the zip file
        url = 'https://github.com/XyzMails/PyKernelOS/archive/main.zip'
        response = requests.get(url)
        with open('PyKernelOS.zip', 'wb') as zip_file:
            zip_file.write(response.content)

        # Extract the contents of the zip file
        with zipfile.ZipFile('PyKernelOS.zip', 'r') as zip_ref:
            zip_ref.extractall('temp')

        # Move the 'utilities' folder if it doesn't exist in the destination
        utilities_source = 'temp/PyKernelOS-main/utilities'
        utilities_destination = './utilities'
        if not os.path.exists(utilities_destination):
            shutil.move(utilities_source, utilities_destination)
        else:
            print("[installer]: 'utilities' folder already exists in the destination.")

        # Move the 'PyKernelOS' folder from the 'releases' directory
        releases_source = 'temp/PyKernelOS-main/releases/PyKernelOS'
        releases_destination = './PyKernelOS'
        shutil.move(releases_source, releases_destination)

        # Clean up
        os.remove('PyKernelOS.zip')
        shutil.rmtree('temp')

        print("[installer]: Download and extraction successful.")
    except Exception as e:
        print("[installer]: Error during download and extraction:", e)

if __name__ == "__main__":
    download_and_extract()
