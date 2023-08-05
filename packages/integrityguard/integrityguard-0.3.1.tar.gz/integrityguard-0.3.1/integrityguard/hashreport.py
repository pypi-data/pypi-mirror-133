#!/usr/bin/env python3

import os
import json
import pathlib
from integrityguard.helpers.loadconfig import load_config
from integrityguard.data.hash import hash_file
from appdirs import *

# Load configuration
config = load_config()

# Get root path to scan
path = config['monitor']['target_path']

# Get hash type
hash_type = config['hash']['hash_type'].lower()

def hash_report():

    # Check if the directory is empty
    if len( os.listdir(path) ) == 0:
        raise ValueError("The directory is empty.")

    # Identify OS config default path
    os_dirs = AppDirs("IntegrityGuard", "IntegrityGuard")

    # Initiate hashes variable
    hashes = []

    # Scan path directory recursively
    for subdir, dirs, files in os.walk(path):
        for file in files:

            file_fullpath = os.path.join(subdir, file)
            try:
                getHash = hash_file(file_fullpath, hash_type)
                hashes.append({ "path": os.path.abspath(file_fullpath), "hash": getHash })
                print(file_fullpath + " > " + getHash)
            except ValueError as e:
                print("Something went wrong hashing the files. " + e)

    # Store hashes
    hash_file_path = os.path.join(os_dirs.user_data_dir, "hashes.json")
    f = open(hash_file_path, "w")
    f.write(json.dumps(hashes))
    f.close()

    print("Hashes stored at " + hash_file_path)