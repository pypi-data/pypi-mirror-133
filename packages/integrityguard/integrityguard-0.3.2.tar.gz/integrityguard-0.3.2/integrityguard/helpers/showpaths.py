import configparser
from appdirs import *
from colorama import init, Fore, Back, Style
import os

def show_paths(config_path=None):

    # Identify OS config default path
    os_dirs = AppDirs("IntegrityGuard", "IntegrityGuard")

    # Define default config file path
    config_file = os.path.join(os_dirs.user_config_dir, "integrityguard.conf")

    # Check if the user provided a config path
    if config_path != None:
        config_file = os.path.abspath(config_path)

    # Print basic instructions for the user
    print(Fore.GREEN + "See important information below:")
    print(Fore.YELLOW + "Default config file path: " + config_file )
    print(Fore.YELLOW + "Default hashes store path: " + os.path.join(os_dirs.user_data_dir, "hashes.json") )

    return True