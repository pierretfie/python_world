import cv2
import re
import validators

# List of suspicious keywords
SUSPICIOUS_KEYWORDS = ["login", "secure", "bank", "verify", "account", "update"]

# Function to analyze URL
def is_suspicious_url(url):
    # Check for suspicious keywords
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url.lower():
            return True

    # Check for shortened URL patterns
    shortened_url_patterns = ["bit.ly", "tinyurl", "goo.gl", "t.co"]
    if any(pattern in url.lower() for pattern in shortened_url_patterns):
        return True

    return False

# Function to process QR code
def analyze_qr_code(image_path):
    # Load the QR code image
    image = cv2.imread(image_path)

    # Initialize QR code detector
    detector = cv2.QRCodeDetector()

    # Detect and decode QR code
    data, bbox, _ = detector.detectAndDecode(image)

    if data:
        print(f"QR Code Content: {data}")
        
        # Validate if the content is a URL
        if validators.url(data):
            print("Detected Content is a URL.")
            if is_suspicious_url(data):
                print("Warning: The URL appears to be suspicious!")
            else:
                print("The URL seems safe.")
        else:
            print("The QR code content is not a URL.")
    else:
        print("No QR Code detected.")

# Main Function
if __name__ == "__main__":
    # Path to QR code image
    image_path = "qr_code_example.png"  
    analyze_qr_code(image_path)