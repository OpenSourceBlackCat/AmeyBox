from colorama import init, Fore
from json import load
from sys import argv
class AmeyBox:
    def __init__(self):
        for c_arg in argv:
            if "--config:" in c_arg:
                self.config=c_arg.replace("--config:", "")
                break
            else:
                self.config="config.json"
        print(f"{Fore.RED} {self.jsonDataLoader(configFile=self.config)}")
    def jsonDataLoader(self, configFile="config.json"):
        if configFile.endswith(".json"):
            with open(configFile, "r") as configJson:
                return load(configJson)
        else: 
            print(f"{Fore.RED}Invalid Config File Format!{Fore.RESET}")