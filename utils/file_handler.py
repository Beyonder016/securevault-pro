# utils/file_handler.py
import os
import shutil
import uuid
from datetime import datetime

TEMP_DIR = "temp_files"

def ensure_temp_dir():
    os.makedirs(TEMP_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file) -> str:
    ensure_temp_dir()
    file_id = uuid.uuid4().hex
    file_path = os.path.join(TEMP_DIR, f"{file_id}_{uploaded_file.name}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path

def clean_temp_dir(older_than_minutes=10):
    now = datetime.now().timestamp()
    for f in os.listdir(TEMP_DIR):
        fpath = os.path.join(TEMP_DIR, f)
        if os.path.isfile(fpath):
            if now - os.path.getmtime(fpath) > 60 * older_than_minutes:
                os.remove(fpath)

def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
