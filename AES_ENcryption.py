from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt data
plaintext = b"Hello, World!"
ciphertext = cipher.encrypt(plaintext)

# Decrypt data
decrypted_text = cipher.decrypt(ciphertext)
print(decrypted_text.decode())