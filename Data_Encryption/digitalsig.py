from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Generate RSA keys
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Sign the data
data = b"Authentic Message"
signature = private_key.sign(
    data, 
    padding.PKCS1v15(), 
    hashes.SHA256()
)

# Verify the signature
public_key.verify(signature, data, padding.PKCS1v15(), hashes.SHA256())