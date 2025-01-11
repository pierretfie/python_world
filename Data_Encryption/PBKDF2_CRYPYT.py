from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os


#PBKDF2 is not reversible
def pbkd():
    # Prompt for data to encrypt
    data = input('ENTER Data to encrypt: ')
    
    # Creating a salt
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    data = data.encode('utf-8')  # Ensure data is in bytes
    key = kdf.derive(data)  # Derive the key
    #print(key)
    return key  # Return the derived key

if __name__ == '__main__':
    derived_key = pbkd()
    print("Derived Key:", derived_key.hex())  # Print the derived key in hexadecimal format