from os import system as os_system, get_terminal_size as get_ts
from colorama import init as c_init, Fore
from rich.tree import Tree as NodeTree
from rich import print as r_print
from requests import get as req_get
from urllib.request import urlopen
from pyfiglet import figlet_format
from tempfile import gettempdir
from tqdm import tqdm
from json import load
from sys import argv
class AmeyBox:
    def __init__(self):
        self.prompt = f"{Fore.BLUE}AmeyToolBox> {Fore.RESET}"
        self.guide_style = "bold"
        self.SelectColor = Fore.GREEN
        self.NodeColor = Fore.YELLOW
        self.ResetColor = Fore.RESET
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
            print(f"{Fore.RED}Invalid Config File Format!{self.ResetColor}")
    def mainInterfaceLoder(self):
        os_system("cls")
        print(f"{'='*get_ts().columns}\n")
        print(f"{Fore.GREEN}{figlet_format('Amey Tool Box', font='banner3', width=get_ts().columns)}{self.ResetColor}")
        print(f"{'='*get_ts().columns}\n")
        self.allPackages = self.jsonData['Packages']
        for package in self.allPackages:
            mainPackage = self.allPackages[package]
            packageTree = NodeTree(f"{self.SelectColor}[{package}] {list(mainPackage.keys())[0]}:{self.ResetColor}", guide_style=self.guide_style)
            for innerPack in mainPackage[list(mainPackage.keys())[0]]:
                for finalPack in mainPackage[list(mainPackage.keys())[0]][innerPack]:
                    packageTree.add(f"{self.NodeColor}{finalPack}{self.ResetColor}")
            r_print(packageTree)
    def packageInstaller(self, pkgNum=0):
        for package in self.allPackages[str(pkgNum)]:
            mainPackage = self.allPackages[str(pkgNum)][package]
            packageTree = NodeTree(f"{self.NodeColor}{list(self.allPackages[str(pkgNum)].keys())[0]}:{self.ResetColor}", guide_style=self.guide_style)
            for innerPack in mainPackage:
                packageTree.add(f"{self.SelectColor}[{innerPack}] {list(mainPackage[innerPack].keys())[0]}{self.ResetColor}")
        r_print(packageTree)
        print(f"\nEnter The Package To Install! (Press Q To Quit)")
        packageName = str(input(self.prompt)).lower()
        if (packageName == "q"):
            exit()
        else:
            mainInstallObject = mainPackage[packageName]
            for installOs in mainInstallObject:
                for installSystem in mainInstallObject[installOs]:
                    packageTree = NodeTree(f"{self.SelectColor}[{installSystem}] {mainInstallObject[installOs][installSystem]['system']} {self.ResetColor}")
                    packageTree.add(f"{Fore.BLUE}Version: {self.NodeColor}{mainInstallObject[installOs][installSystem]['version']}{self.ResetColor}")
                    r_print(packageTree)
            print(f"\nEnter The Operating System To Install On! (Press Q To Quit)")
            systemToInstall = str(input(self.prompt)).lower()
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
                        total_length = int(q_res.headers.get("content-length"))
                        for data in tqdm(q_res.iter_content(chunk_size=4096), desc=f"Downloading {finalInstallObject['fileName']}{Fore.YELLOW}", total=(total_length/4096), unit="KB"):
                            installPackage.write(data)
                print(f"\n{Fore.GREEN}Installing {finalInstallObject['fileName']}...{self.ResetColor}")
                os_system(f"{tempFileName}")
                self.mainInterfaceLoder()
    def installApp(self):
        while True:
            self.mainInterfaceLoder()
            print(f"\nEnter The Package Type To Install! (Press Q To Quit)")
            installOption = str(input(self.prompt)).lower()
            if (installOption == "q"):
                exit()
            else:
                self.packageInstaller(pkgNum=installOption)
                
if __name__ == "__main__":
    AmeyBox()