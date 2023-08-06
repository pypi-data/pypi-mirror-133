from appdirs import *
import os
import shutil

def copy_config(target_path=None):

    # Identify OS config default path
    dirs = AppDirs("IntegrityGuard", "IntegrityGuard")

    # Check if directory exists
    if os.path.isdir(dirs.user_config_dir) == False:
        os.makedirs(dirs.user_config_dir, exist_ok=True)

    # Define default config file path
    if target_path == None:
        target_path = os.path.join(dirs.user_config_dir, "integrityguard.conf")

    # Check if the config file exist
    if os.path.isfile(target_path) == True:
        print("The configuration file *" + target_path + "* already exist. Skipped.")
    else:
        source_config_path = os.path.dirname(os.path.abspath(__file__))
        source_config_path = os.path.join( source_config_path , "../integrityguard.conf")
        shutil.copyfile( source_config_path , target_path)
        print("Success: configuration file copied to " + target_path)

    return True