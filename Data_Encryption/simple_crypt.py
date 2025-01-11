from simplecrypt import encrypt, decrypt

password = "my_secret_key"
ciphertext = encrypt(password, "Confidential data")
plaintext = decrypt(password, ciphertext)

print(plaintext.decode())