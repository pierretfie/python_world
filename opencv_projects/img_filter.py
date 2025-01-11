import cv2
import numpy as np

# Apply different filters to an image
def apply_filters(image):
    # 1. Blur Filter
    blurred = cv2.GaussianBlur(image, (15, 15), 0)

    # 2. Sharpen Filter
    kernel_sharpen = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
    sharpened = cv2.filter2D(image, -1, kernel_sharpen)

    # 3. Sepia Filter
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                              [0.349, 0.686, 0.168],
                              [0.393, 0.769, 0.189]])
    sepia = cv2.transform(image, sepia_filter)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)

    return blurred, sharpened, sepia

# Load the input image
image = cv2.imread('sample.jpg')

# Apply the filters
blurred, sharpened, sepia = apply_filters(image)

# Display the original and filtered images
cv2.imshow('Original Image', image)
cv2.imshow('Blurred Image', blurred)
cv2.imshow('Sharpened Image', sharpened)
cv2.imshow('Sepia Image', sepia)

# Wait for a key press and close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()