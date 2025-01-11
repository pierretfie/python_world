def decrypt_file(file_path: str, password: str):
    with open(file_path, "rb") as f:
        data = f.read()
    
    salt, iv, tag, ciphertext = data[:16], data[16:28], data[28:44], data[44:]
    key = generate_key(password, salt)
    
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    with open(file_path.replace(".enc", ""), "wb") as f:
        f.write(plaintext)
    print("File decrypted successfully!")