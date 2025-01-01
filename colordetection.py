import cv2
import numpy as np

def detect_color(frame, lower_bound, upper_bound):
    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color range
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    # Apply the mask to the original frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    return mask, result

# Define the color range (e.g., for red)
lower_red = np.array([0, 120, 70])   # Lower bound of red in HSV
upper_red = np.array([10, 255, 255])  # Upper bound of red in HSV

# Initialize webcam or use an image
cap = cv2.VideoCapture(0)  # Use `cv2.imread('image.jpg')` for images

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect the specified color
    mask, result = detect_color(frame, lower_red, upper_red)

    # Display the results
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Detected Color", result)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()