from os import system as os_system, get_terminal_size as get_ts
from colorama import init as c_init, Fore
from requests import get as req_get
from urllib.request import urlopen
from pyfiglet import figlet_format
from tempfile import gettempdir
from json import load
from sys import argv
class AmeyBox:
    def __init__(self):
        self.DefaultConfig = urlopen("https://raw.githubusercontent.com/Amey-Gurjar/AmeyBox/main/config.json")
        c_init()
        for c_arg in argv:
            if "--config:" in c_arg:
                self.config=c_arg.replace("--config:", "")
                break
            else:
                self.config=self.DefaultConfig
        self.jsonData=self.jsonDataLoader(configFile=self.config)
        self.installApp()
    def jsonDataLoader(self, configFile="config.json"):
        try:
            return load(configFile)["AmeyBox"]
        except: 
            print(f"{Fore.RED}Invalid Config File Format!{Fore.RESET}")
    def mainInterfaceLoder(self):
        os_system("cls")
        print(f"{'='*get_ts().columns}\n")
        print(f"{Fore.GREEN}{figlet_format('Amey Tool Box', font='banner3', width=get_ts().columns)}{Fore.RESET}")
        print(f"{'='*get_ts().columns}\n")
        self.allPackages = self.jsonData['Packages']
        for package in self.allPackages:
            mainPackage = self.allPackages[package]
            print(f"{Fore.GREEN}[{package}] {list(mainPackage.keys())[0]}:{Fore.RESET}")
            for innerPack in mainPackage[list(mainPackage.keys())[0]]:
                for finalPack in mainPackage[list(mainPackage.keys())[0]][innerPack]:
                    print(f"{Fore.WHITE}{finalPack}{Fore.RESET}")
    def packageInstaller(self, pkgNum=0):
        for package in self.allPackages[str(pkgNum)]:
            mainPackage = self.allPackages[str(pkgNum)][package]
            for innerPack in mainPackage:
                print(f"{Fore.GREEN}[{innerPack}] {list(mainPackage[innerPack].keys())[0]}{Fore.RESET}")
        print(f"\nEnter The Package To Install! (Press Q To Quit)")
        packageName = str(input("AmeyBox> ")).lower()
        if (packageName == "q"):
            exit()
        else:
            mainInstallObject = mainPackage[packageName]
            for installOs in mainInstallObject: 
                for installSystem in mainInstallObject[installOs]:
                    print(f"{Fore.GREEN}[{installSystem}] {mainInstallObject[installOs][installSystem]['system']} -> {mainInstallObject[installOs][installSystem]['version']}{Fore.RESET}")    
            print(f"\nEnter The Operating System To Install On! (Press Q To Quit)")
            systemToInstall = str(input("AmeyBox> ")).lower()
            if (systemToInstall == "q"):
                exit()
            else:
                finalInstallObject = mainInstallObject[installOs][systemToInstall]
                tempFileName = f"{gettempdir()}\\{finalInstallObject['fileName']}"
                URL = finalInstallObject["url"]
                with open(tempFileName, "wb") as installPackage:
                    q_res = req_get(URL, stream=True)
                    if q_res.headers.get("content-length") is None:
                        installPackage.write(q_res.content)
                    else:
                        dl = 0
                        total_length = int(q_res.headers.get("content-length"))
                        for data in q_res.iter_content(chunk_size=4096):
                            dl += len(data)
                            installPackage.write(data)
                            done = int(50 * dl / total_length)
                            print(f"{Fore.GREEN}Downloading {finalInstallObject['fileName']}: {Fore.WHITE}[{'='*(0 + done)}]{Fore.RESET}", end="\r")
                print(f"\n{Fore.GREEN}Installing {finalInstallObject['fileName']}...{Fore.RESET}")
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
                
if __name__ == "__main__":
    AmeyBox()