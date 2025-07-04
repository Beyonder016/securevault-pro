# utils/hashing.py
import hashlib

def sha256_hash(file_path: str) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def compare_hash(original: str, test: str) -> bool:
    return original == test
