from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt_file(file_path: str, password: str):
    salt = os.urandom(16)
    key = generate_key(password, salt)
    iv = os.urandom(12)
    
    with open(file_path, "rb") as f:
        plaintext = f.read()
    
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    with open(file_path + ".enc", "wb") as f:
        f.write(salt + iv + encryptor.tag + ciphertext)
    print("File encrypted successfully!")