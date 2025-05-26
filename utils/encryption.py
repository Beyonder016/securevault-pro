# encryption.py
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from utils.config import TEMP_DIR
import secrets

BLOCK_SIZE = 128


def encrypt_file(filepath, key):
    with open(filepath, 'rb') as f:
        data = f.read()

    padder = padding.PKCS7(BLOCK_SIZE).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()

    enc_path = os.path.join(TEMP_DIR, "encrypted_" + os.path.basename(filepath))
    with open(enc_path, 'wb') as f:
        f.write(iv + ct)

    return enc_path


def decrypt_file(filepath, key):
    with open(filepath, 'rb') as f:
        iv = f.read(16)
        ct = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plain = decryptor.update(ct) + decryptor.finalize()

    unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()
    data = unpadder.update(padded_plain) + unpadder.finalize()

    dec_path = os.path.join(TEMP_DIR, "decrypted_" + os.path.basename(filepath))
    with open(dec_path, 'wb') as f:
        f.write(data)

    return dec_path
