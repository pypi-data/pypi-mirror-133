from appdirs import *
import os
import shutil

def copy_config(config_path=None):

    # Identify OS config default path
    dirs = AppDirs("IntegrityGuard", "IntegrityGuard")

    # Check if directory exists
    if os.path.isdir(dirs.user_config_dir) == False:
        os.makedirs(dirs.user_config_dir, exist_ok=True)

    # Define default config file path
    config_file = os.path.join(dirs.user_config_dir, "integrityguard.conf")

    # Check if the user provided a config path
    if config_path != None:
        config_file = os.path.abspath(config_path)

    # Check if the config file exist
    if os.path.isfile(config_file) == False:
        raise ValueError("The configuration file *" + config_file + "* doesn't exist.")
    else:
        source_config_path = os.path.dirname(os.path.abspath(__file__))
        source_config_path = os.path.join( source_config_path , "../integrityguard.conf")
        shutil.copyfile( source_config_path , config_file)

    return True