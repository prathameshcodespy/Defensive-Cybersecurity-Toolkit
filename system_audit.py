import platform
import sys

def get_os_info():
    return platform.system(), platform.release()

def get_python_version():
    return sys.version

def audit_summary(open_ports):
    return f"Total open ports detected: {len(open_ports)}"
