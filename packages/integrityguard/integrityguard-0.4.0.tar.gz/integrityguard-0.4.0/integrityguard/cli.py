import sys
import click
from integrityguard.helpers.loadconfig import load_config
from integrityguard.helpers.showpaths import show_paths
from integrityguard.helpers.copyconfig import copy_config
from integrityguard.hashreport import hash_report
from integrityguard.monitor import monitor

# Load configuration
config = load_config()

# Get root path to scan
path = config['monitor']['target_path']

# Get hash type
hash_type = config['hash']['hash_type'].lower()

@click.command()

# Required options
@click.option('--task', default="monitor", help='Tasks available: monitor, generate_hashes')

# Optional or conditional options
@click.option('--target', default=path, help='Target path to monitor')
@click.option('--config', help='Full path to .conf file')
@click.option('--hash', help='Hash algorithm type (MD5, SHA1, SHA224, SHA256, SHA384, and SHA512).')

# Options to use with copy_config
@click.option('--destination', help='Used for copy_config task. Full destination path of the .conf file.')

# Options to use with generate_hashes
@click.option('--save-to', help='Destination folder of the hashes.json report.')

def main(task,target,config,hash,destination,save_to):

    """Console script for IntegrityGuard."""

    if task == "generate_hashes":
        
        if save_to != None and save_to.endswith('.json') == False:
            print("Error: --save-to must be a full path including the file name. (e.g. hashes.json)")
            exit()

        hash_report(config,target,save_to)

    elif task == "monitor":
        monitor(config,target)

    elif task == "copy_config":
        # Handle possible errors
        if destination == "":
            print("Error: --destination is required when using copy_config task.")
            exit()

        if destination.endswith('.conf') == False:
            print("Error: --destination must be a full path including the file name. (e.g. <any-name>.conf)")
            exit()

        # Copy config file
        copy_config(destination)

    elif task == "show_paths":
        show_paths(config)

    return 0

if __name__ == "__main__":
    sys.exit(main())
