#linux environment
import cv2
from os import path
from pyzbar.pyzbar import decode
from os import listdir, path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def read_qr_code():
    # Fixed directory path
    dir = f'{path.expanduser('~/Documents')}'
    files = listdir(dir)
    file_completer = WordCompleter(files)

    # Print available files in the fixed directory
    print("Available files:")
    for file in files:
        print(file)

    try:
        # Prompt user for the image file name with auto-completion
        image_name = prompt('Enter the QR image file name (include extension): ', completer=file_completer)
        
        # Check if the file exists in the fixed directory
        if image_name not in files:
            print('File not found. Please enter a valid file name.')
            return
        
        # Construct the full file path
        image_path = path.join(dir, image_name)
        
        # Load the image
        image = cv2.imread(image_path)
        
        # Decode the QR code
        decoded_objects = decode(image)
        
        if decoded_objects:
            for obj in decoded_objects:
                # Print the type and data of the QR code
                print("Type:", obj.type)
                print("Data:", obj.data.decode("utf-8"))
        else:
            print("No QR code found in the image.")
    
    except KeyboardInterrupt:
        print('\nExiting...')
    except Exception as e:
        print(f"Error: {e}")

# Call the function to read QR code from image
read_qr_code()

