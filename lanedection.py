import cv2
import numpy as np

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    return cv2.bitwise_and(img, mask)

def draw_lines(img, lines):
    if lines is None:
        return
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 5)

def detect_lanes(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply Canny edge detection
    edges = cv2.Canny(blur, 50, 150)
    
    # Define region of interest (ROI)
    height, width = edges.shape
    roi_vertices = np.array([[(0, height), (width // 2, height // 2), (width, height)]], dtype=np.int32)
    roi = region_of_interest(edges, roi_vertices)
    
    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(roi, rho=1, theta=np.pi/180, threshold=50, minLineLength=40, maxLineGap=150)
    
    # Draw lines on a blank image
    line_image = np.zeros_like(image)
    draw_lines(line_image, lines)
    
    # Combine original image with line image
    result = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    return result

# Load a sample video or image
cap = cv2.VideoCapture('road_video.mp4')  # Replace with 'road.jpg' for an image
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    lanes = detect_lanes(frame)
    
    # Display the result
    cv2.imshow('Lane Detection', lanes)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()