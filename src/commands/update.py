import os
import sys
import urllib.request
import json
import logging
import subprocess
from argparse import _SubParsersAction, ArgumentParser

from src.utils.version import get_pvm_version

logger = logging.getLogger("pvm.update")

def get_latest_release(repo_owner, repo_name, asset_name):
    """Fetch the latest release download URL from GitHub API."""
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            
        # Find the asset with the matching name
        for asset in data.get('assets', []):
            if asset['name'] == asset_name:
                return asset['browser_download_url'], data['tag_name']
        
        raise ValueError(f"Asset '{asset_name}' not found in latest release")
    
    except Exception as e:
        logger.error(f"Failed to fetch latest release info: {e}")
        raise

def handle_update(args):

    if get_pvm_version() == get_latest_release("itsAnanth", "pvm", "pvm.exe")[1]:
        print("pvm is already up to date.")
        return
    
    # Run the install script in a new PowerShell window
    ps_command = 'irm https://raw.githubusercontent.com/itsAnanth/pvm/refs/heads/main/powershell/install.ps1 | iex'
    
    try:
        subprocess.Popen(
            ['powershell', '-NoExit', '-ExecutionPolicy', 'ByPass', '-Command', ps_command],
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
        
        logger.info("Update process started in a new terminal window.")
        logger.info("Please check the terminal window for update progress.")
        
    except Exception as e:
        logger.error(f"Failed to start update: {e}")
        logger.error("Update failed")
        return

def update_command(sub_parser: _SubParsersAction):

    parser = sub_parser.add_parser(
        'update',
        help='Update pvm to latest version'
    )

    parser.set_defaults(func=handle_update)

    