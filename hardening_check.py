import os

def firewall_check():
    # Educational simulation (cross-platform safe)
    return "Firewall status check requires OS-specific permissions."

def ssh_check():
    if os.name == "posix":
        return "Check if SSH service is running using: systemctl status ssh"
    return "SSH check not supported on this OS."

def password_policy_check():
    return "Ensure passwords are at least 12 characters with mixed symbols."
