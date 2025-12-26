from src.scripts.arch import is_windows, detect_arch


arch = detect_arch()
print(f"Current architecture: {arch if arch != '' else 'win32'}")
print(f"Is windows?: {is_windows()}")