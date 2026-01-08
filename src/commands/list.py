import logging
from src.scripts.get_versions import get_python_github_versions
from src.scripts.store import Store
from argparse import _SubParsersAction, ArgumentParser


logger = logging.getLogger("pvm.list")


def handle_list(args):
    # Show installed versions
    installed = Store.get_versions()
    installed = sorted(installed, key=lambda v: tuple(map(int, v['version'].split('.'))))
    
    if args.installed or not (args.available or args.all or args.latest):
        if installed:
            print("Installed versions:")
            for v in installed:
                print(f"{v['version']} ({v['dir']}) {'[using]' if v.get('using') else ''}")
        else:
            print("No versions installed")
        
        if not args.available and not args.all and not args.latest:
            return
    
    if args.available or args.all or args.latest:
        logger.info("Fetching available Python versions from python.org...")
        versions = get_python_github_versions()
        print("\nAvailable versions:")
        
        if args.latest:
            versions = versions[len(versions) - 1]
        
        installed_versions = {v['version'] for v in installed}
        
        for v in versions:
            marker = "[installed]" if v['version'] in installed_versions else ""
            print(f"{v['version']} {marker}")

def list_command(sub_parser: _SubParsersAction):

    parser = sub_parser.add_parser(
        'list',
        help='List installed or available Python versions'
    )

    parser.add_argument(
        '-i', '--installed',
        action='store_true',
        help='Show only installed versions (default if no flags)'
    )

    parser.add_argument(
        '--available',
        action='store_true',
        help='Show available versions from python.org'
    )

    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Show both installed and available versions'
    )

    parser.add_argument(
        '--latest',
        action='store_true',
        help='Filter available versions to show only the latest from each major release'
    )

    parser.set_defaults(func=handle_list)

    