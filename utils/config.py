# config.py
import os

# Temporary storage for encrypted/decrypted files
TEMP_DIR = "temp_files"

# App metadata
APP_NAME = "SecureVault"
APP_ICON = "🔐"
THEME = "dark"

# Ensure directory exists
os.makedirs(TEMP_DIR, exist_ok=True)
