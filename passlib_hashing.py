from passlib.hash import bcrypt

# Hash a password
hashed = bcrypt.hash("my_password")

# Verify the password
print(bcrypt.verify("my_password", hashed))  # True
print(bcrypt.verify("wrong_password", hashed))  # False