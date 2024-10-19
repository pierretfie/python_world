import hashlib
data = 'message to encrypt'

#create hash object
hash_object = hashlib.sha256()

#convert the input data to bytes and update hash object
hash_object.update(data.encode('utf-8'))

# get the hexadecimal representation of the hash value
hashed_data = hash_object.hexdigest()
print(hashed_data)