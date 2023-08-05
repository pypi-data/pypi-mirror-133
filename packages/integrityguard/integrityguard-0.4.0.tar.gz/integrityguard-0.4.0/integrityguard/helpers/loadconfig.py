import configparser
from appdirs import *
import os
from integrityguard.helpers.copyconfig import copy_config

def load_config(config_path=None,copy=False):

    # Identify OS config default path
    dirs = AppDirs("IntegrityGuard", "IntegrityGuard")

    # Define default config file path
    config_file = os.path.join(dirs.user_config_dir, "integrityguard.conf")

    # Check if the user provided a config path
    if config_path != None:
        config_file = os.path.abspath(config_path)

    # Check if the config file exist
    if os.path.exists(config_file) == False:
        print("File *"+ config_file + "* not found.")
        if copy:
            copy_config(config_file)

    config = configparser.ConfigParser()
    config.read(config_file)

    return config