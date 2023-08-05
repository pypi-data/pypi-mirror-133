#!/usr/bin/env python3

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from integrityguard.helpers.loadconfig import load_config

def monitor(config=None,target=None):

    # Load configuration
    config = load_config(config)

    # Get root path to scan
    path = target
    if path == None:
        path = config['monitor']['target_path']

    logging.basicConfig(filename="",
                        level=logging.INFO,
                        format='[%(asctime)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
