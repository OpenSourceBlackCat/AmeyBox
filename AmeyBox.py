from colorama import init as c_init, Fore
from requests import get as req_get
from os import system as os_system
from tempfile import gettempdir
from json import load
from sys import argv
class AmeyBox:
    def __init__(self):
        c_init()
        for c_arg in argv:
            if "--config:" in c_arg:
                self.config=c_arg.replace("--config:", "")
                break
            else:
                self.config="config.json"
        self.jsonData=self.jsonDataLoader(configFile=self.config)
        self.installApp()
    def jsonDataLoader(self, configFile="config.json"):
        if configFile.endswith(".json"):
            with open(configFile, "r") as configJson:
                return load(configJson)["AmeyBox"]
        else: 
            print(f"{Fore.RED}Invalid Config File Format!{Fore.RESET}")
    def mainInterfaceLoder(self):
        os_system("cls")
        self.allPackages = self.jsonData['Packages']
        for package in self.allPackages:
            mainPackage = self.allPackages[package]
            print(f"{Fore.GREEN}[{package}] {list(mainPackage.keys())[0]}:{Fore.RESET}")
            for innerPack in mainPackage[list(mainPackage.keys())[0]]:
                print(mainPackage[list(mainPackage.keys())[0]][innerPack]['name'])
    def packageInstaller(self, pkgNum=0):
        for package in self.allPackages[str(pkgNum)]:
            mainPackage = self.allPackages[str(pkgNum)][package]
            for innerPack in mainPackage:
                print(f"{Fore.GREEN}[{innerPack}] {mainPackage[innerPack]['name']}{Fore.RESET} -> {Fore.BLUE}v{mainPackage[innerPack]['version']}{Fore.RESET}")
        print(f"\nEnter The Package To Install! (Press Q To Quit)")
        packageName = str(input("AmeyBox> ")).lower()
        if (packageName == "q"):
            exit()
        else:
            mainInstallObject = mainPackage[packageName]
            tempFileName = f"{gettempdir()}\\{mainInstallObject['fileName']}"
            URL = mainInstallObject["url"]
            with open(tempFileName, "wb") as installPackage:
                installPackage.write(req_get(URL).content)
            os_system(f"{tempFileName}")
        self.mainInterfaceLoder()
    def installApp(self):
        while True:
            self.mainInterfaceLoder()
            print(f"\nEnter The Package Type To Install! (Press Q To Quit)")
            installOption = str(input("AmeyBox> ")).lower()
            if (installOption == "q"):
                exit()
            else:
                self.packageInstaller(pkgNum=installOption)
                