from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os, hashlib

salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)

key = kdf.derive(b"mypassword")