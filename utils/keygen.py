# utils/keygen.py
import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def generate_salt(length=16):
    return os.urandom(length)

def derive_key(password: str, salt: bytes, length=32, iterations=100_000) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encode_salt(salt: bytes) -> str:
    return urlsafe_b64encode(salt).decode()

def decode_salt(salt_str: str) -> bytes:
    return urlsafe_b64decode(salt_str.encode())
