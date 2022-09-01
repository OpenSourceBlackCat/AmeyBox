from os import system as os_sys, path, mkdir
from gettext import install
from sys import platform
from json import load
pipList = ["pyfiglet", "requests", "colorama", "rich"]
# for pip in pipList:
#     os_sys(f"pip install {pip} --force-reinstall")
from pyfiglet import figlet_format as figmat
from rich.progress import track as pgr_bar
from urllib.request import urlopen
from requests import get as rq_get
from colorama import Fore, init as cl_init
class AmeyInstaller:
    def __init__(self):
        cl_init()
        self.clear()
        self.allFiles = load(urlopen("https://raw.githubusercontent.com/Amey-Gurjar/AmeyBox/main/installer.config.json"))["AmeyBox"]["installer"]
    def clear(self):
        if (platform=="win32"):
            os_sys("cls")
        else:
            os_sys("clear")
    def installer(self):
        for package_num, package in enumerate(self.allFiles):
            packageURL = self.allFiles[package]
            homeDir = path.expanduser("~")
            if platform == "win32":
                dataDir = path.join(homeDir, "AppData", "Local", "AmeyToolBox")
                if not path.exists(dataDir):
                    mkdir(dataDir)
            else:
                dataDir = path.join(homeDir, "AmeyToolBox")
            packageName = path.join(dataDir, f"{list(self.allFiles.keys())[package_num]}")
            with open(packageName, "wb") as installPackage:
                q_res = rq_get(packageURL, stream=True)
                if q_res.headers.get("content-length") is None:
                    installPackage.write(q_res.content)
                else:
                    total_length = int(q_res.headers.get("content-length"))
                    for data in pgr_bar(sequence=q_res.iter_content(chunk_size=4096), description=f"{Fore.YELLOW}Installing {packageName}{Fore.GREEN}", total=(total_length/4096)):
                        installPackage.write(data)
            print(f"{Fore.GREEN}Installation Complete!{Fore.YELLOW}")
            input(f"{Fore.YELLOW}Press Any Key To Exit!{Fore.RESET}")
            self.clear()
            
if __name__ == "__main__":
    mainInstaller = AmeyInstaller()
    mainInstaller.installer()