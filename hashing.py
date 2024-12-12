import hashlib
from password_gen import password
data = password()
#print(data)
message = data[0]

def hashdata ():

    #create hash object
    hash_object = hashlib.sha256()

    #convert the input data to bytes and update hash object
    hash_object.update(message.encode('utf-8'))

    # get the hexadecimal representation of the hash value
    hashed_data = hash_object.hexdigest()
    print(hashed_data)
if __name__ == '__main__:
    hashdata()
   



