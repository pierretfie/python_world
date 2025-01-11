from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate keys
key = RSA.generate(2048)
public_key = key.publickey()

# Encrypt message
cipher = PKCS1_OAEP.new(public_key)
ciphertext = cipher.encrypt(b"Secure Message")

# Decrypt message
decipher = PKCS1_OAEP.new(key)
plaintext = decipher.decrypt(ciphertext)
print(plaintext.decode())