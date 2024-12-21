from cryptography.fernet import Fernet


def aescrypt():
    # Generate a key
    key = Fernet.generate_key()
    cipher = Fernet(key)

    # Encrypt data
    plaintext = input("Enter data to encrypt: ")
    #conversion to bytes
    plaintext_bytes = plaintext.encode('utf-8')
    ciphertext = cipher.encrypt(plaintext_bytes)
    print(ciphertext)
    return ciphertext, key
def aesdecrypt():
    key = data[1]
    cipher = Fernet(key)
    ciphertext = data[0]
    # Decrypt data
    decrypted_text = cipher.decrypt(ciphertext)
    print(decrypted_text.decode())
if __name__ == '__main__':
    data = aescrypt()

    aesdecrypt()