import sys
import click
from integrityguard.helpers.loadconfig import load_config
from integrityguard.helpers.showpaths import show_paths
from integrityguard.hashreport import hash_report
from integrityguard.monitor import monitor

# Load configuration
config = load_config()

# Get root path to scan
path = config['monitor']['target_path']

# Get hash type
hash_type = config['hash']['hash_type'].lower()

@click.command()
@click.option('--task', default="monitor", help='Tasks available: monitor, generate_hashes')
@click.option('--target', default=path, help='Target path to monitor')
@click.option('--hash', default=hash_type, help='Hash algorithm type (MD5, SHA1, SHA224, SHA256, SHA384, and SHA512).')

def main(task,target,hash):

    """Console script for IntegrityGuard."""

    if task == "generate_hashes":
        hash_report()
    elif task == "monitor":
        monitor()
    elif task == "show_paths":
        show_paths()
    return 0

if __name__ == "__main__":
    sys.exit(main())
