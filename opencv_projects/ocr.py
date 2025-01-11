import cv2
import pytesseract

# Path to Tesseract-OCR executable (change this to match your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the image
image = cv2.imread('text_image.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Preprocess the image for better OCR results
gray = cv2.GaussianBlur(gray, (5, 5), 0)
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Perform OCR
text = pytesseract.image_to_string(gray)

# Display the extracted text
print("Extracted Text:")
print(text)

# Optionally, display the processed image
cv2.imshow("Processed Image", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()