import cv2
import numpy as np

def encrypt_image(image, key):
    # Convert the image to a NumPy array
    encrypted_image = np.bitwise_xor(image, key)
    return encrypted_image

def decrypt_image(encrypted_image, key):
    # Decrypt by XORing again with the same key
    decrypted_image = np.bitwise_xor(encrypted_image, key)
    return decrypted_image

# Load the image
image = cv2.imread('image.jpg')  # Replace with your image path
key = 123  # Secret key for encryption (integer)

# Encrypt the image
encrypted_image = encrypt_image(image, key)

# Save and display the encrypted image
cv2.imwrite('encrypted_image.jpg', encrypted_image)
cv2.imshow("Encrypted Image", encrypted_image)

# Decrypt the image
decrypted_image = decrypt_image(encrypted_image, key)

# Save and display the decrypted image
cv2.imwrite('decrypted_image.jpg', decrypted_image)
cv2.imshow("Decrypted Image", decrypted_image)

# Wait and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()