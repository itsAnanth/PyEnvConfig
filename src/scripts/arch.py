import os
import platform
import struct

def detect_arch():
    cpu = platform.machine().lower()
    is_64 = struct.calcsize("P") * 8 == 64

    if cpu in ("amd64", "x86_64") and is_64:
        return "amd64"
    if cpu in ("arm64", "aarch64"):
        return "arm64"
    return ""  # win32

def is_windows():
    return os.name == "nt"