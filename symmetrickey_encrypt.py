from cryptography.fernet import Fernet

key = Fernet.generate_key()  # Single shared key
cipher = Fernet(key)

# Encrypt and decrypt
ciphertext = cipher.encrypt(b"Hello World")
plaintext = cipher.decrypt(ciphertext)