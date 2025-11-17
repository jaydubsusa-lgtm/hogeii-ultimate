#!/usr/bin/env python3
"""
Configuration module for Hogeii Ultimate
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"

# Ensure directories exist
LOG_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# Sentinel configuration
SENTINEL_CONFIG = {
    "monitor_interval": 5,  # seconds
    "log_file": LOG_DIR / "sentinel.log",
    "alert_threshold": 10,
    "enable_email_alerts": False,
}

# UGO Auto configuration
UGO_CONFIG = {
    "default_file_perms": "644",
    "default_dir_perms": "755",
    "secure_file_perms": "600",
    "executable_perms": "755",
    "insecure_patterns": ["777", "666", "776", "767"],
}

# Hogeii Core configuration
CORE_CONFIG = {
    "verbose": True,
    "auto_fix": False,
    "backup_before_fix": True,
}
