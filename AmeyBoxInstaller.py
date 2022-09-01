from os import system as os_sys
from sys import platform
from json import load
pipList = ["pyfiglet", "requests", "colorama", "rich"]
for pip in pipList:
    os_sys(f"pip install {pip} --force-reinstall")
from pyfiglet import figlet_format as figmat
from rich.progress import track as pgr_bar
from urllib.request import urlopen
class AmeyInstaller:
    def __init__(self):
        os_sys("clear")
        self.allFiles = urlopen(load(""))