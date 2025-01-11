import cv2
from pyzbar.pyzbar import decode

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture video frame
    ret, frame = cap.read()
    if not ret:
        break

    # Decode QR codes in the frame
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        # Extract the QR code data
        data = obj.data.decode('utf-8')
        print(f"QR Code Data: {data}")

        # Draw a rectangle around the QR code
        points = obj.polygon
        if len(points) == 4:
            pts = [(point.x, point.y) for point in points]
            for i in range(len(pts)):
                cv2.line(frame, pts[i], pts[(i + 1) % 4], (0, 255, 0), 3)

        # Display the decoded data on the frame
        cv2.putText(frame, data, (pts[0][0], pts[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (0, 255, 0), 2)

    # Display the video feed
    cv2.imshow('QR Code Scanner', frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()