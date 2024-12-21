from cryptography.fernet import Fernet


def aescrypt():
    # Generate a key
    key = Fernet.generate_key()
    cipher = Fernet(key)

    # Encrypt data
    plaintext = input(b"Enter data to encrypt: ")
    ciphertext = cipher.encrypt(plaintext)
    print(ciphertext)
    return ciphertext, cipher

def aesdecrypt():
    cipher = aescrypt[0]
    ciphertext = aescrypt[1]
    # Decrypt data
    decrypted_text = cipher.decrypt(ciphertext)
    print(decrypted_text.decode())
if __name__ == '__main__':
    aesdecrypt()