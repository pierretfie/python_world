from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os, hashlib


def pbkd(data):
    #creating a salt
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    data = 
    key = kdf.derive(b"mypassword")
pbkd(data = input('ENTER Data to encrypt: '))