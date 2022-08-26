from colorama import init as c_init, Fore
from json import load, loads
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
        self.allPackages = self.jsonData['Packages']
        for package in self.allPackages:
            print(f"{Fore.RESET}{package}:\n{Fore.RESET}")
            for pack in range(len(self.allPackages[package])):
                print(f"{Fore.GREEN}[{list(self.allPackages[package].keys())[pack]}]: {self.allPackages[package][str(pack+1)]['name']}{Fore.RESET}")
            print("\n")
    def installApp(self):
        while True:
            self.mainInterfaceLoder()