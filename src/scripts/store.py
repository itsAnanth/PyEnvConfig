import os
import json
import logging

from src.utils.registry import get_user_path, set_user_path
from src.scripts.shims import generate_shims

logger = logging.getLogger("pvm.store")

PVM_ROOT = os.path.join(os.environ['LOCALAPPDATA'], '.pvm')
VERSIONS_FILE = os.path.join(PVM_ROOT, 'versions.json')
INIT_MARKER = os.path.join(PVM_ROOT, '.initialized')
SHIMS_DIR = os.path.join(PVM_ROOT, 'shims')

class Store:

    def is_initialized() -> bool:
        return os.path.exists(INIT_MARKER)

    @staticmethod
    def init_store():
        
        if not os.path.isdir(PVM_ROOT):
            os.makedirs(PVM_ROOT, exist_ok=True)
            logger.debug(f"Initialized store at {PVM_ROOT}")

        if not os.path.exists(VERSIONS_FILE):
            Store.write_versions([])
            logger.debug(f"Created versions file at {VERSIONS_FILE}")

        if not os.path.isdir(SHIMS_DIR):
            os.makedirs(SHIMS_DIR, exist_ok=True)
            logger.debug(f"Created shims directory at {SHIMS_DIR}")

            # if shims was accidentally deleted and user is using a version, regenerate shims
            versions = Store.get_versions()
            for version in versions:
                if version.get("using", False):
                    if generate_shims(version):
                        logger.debug(f"Regenerated shims for version {version['version']}")

        # Check if already initialized
        if Store.is_initialized():
            logger.debug("PVM store already initialized")
            return

        # add shims to user path if not already present
        user_path = get_user_path()

        if SHIMS_DIR not in user_path:
            new_path = f"{SHIMS_DIR};{user_path}"

            try:
                set_user_path(new_path)
                logger.debug(f"Added shims directory to user PATH: {SHIMS_DIR}")
            except ValueError as e:
                logger.error(f"Failed to update PATH: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error updating PATH: {e}")
                raise
        
        # Mark as initialized
        with open(INIT_MARKER, 'w') as f:
            f.write('')
        logger.debug("PVM initialization complete")
            


    @staticmethod
    def get_pvm_root() -> str:
        return os.path.join(os.environ['LOCALAPPDATA'], '.pvm')
    
    
    @staticmethod
    def get_versions():
        """Read installed versions from JSON file"""
        if not os.path.exists(VERSIONS_FILE):
            return []
        
        with open(VERSIONS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logger.error("Failed to decode versions file, returning empty list")
            return []
    
    @staticmethod
    def write_versions(versions):
        """Write installed versions to JSON file
        
        Args:
            versions: List of dicts with format [{"version": "3.11.0", "dir": "C:\\...", "using": True}]
        """
        with open(VERSIONS_FILE, 'w') as f:
            json.dump(versions, f, indent=2)

    
    @staticmethod
    def remove_version(version: str):
        """Remove a version from the store
        
        Args:
            version: particular version of python to remove
            
        """
        versions = Store.get_versions()
        versions = [v for v in versions if v["version"] != version]
        Store.write_versions(versions)
    
    @staticmethod
    def get_version(func: lambda version: dict):
        """Get the installation directory for a specific version"""
        versions = Store.get_versions()
        for i, v in enumerate(versions):
            if func(v):
                return i, v
        return -1, None
    
    @staticmethod
    def set_version(version_dict: dict):
        """Get the installation directory for a specific version"""
        versions = Store.get_versions()
        index = -1
        for i, v in enumerate(versions):
            if v["version"] == version_dict["version"]:
                index = i
                break
        
        if index == -1:
            versions.append(version_dict)
        else:
            versions[index] = version_dict
        Store.write_versions(versions)
