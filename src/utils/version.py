def get_pvm_version():
    try:
        from src._version import VERSION
    except ImportError:
        VERSION = "dev"
    return VERSION