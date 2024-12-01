from PIL import ImageGrab
import os

def screensht():
    add = 0
    dir = '~/Pictures'
    screenshot = ImageGrab.grab()

    # Create the directory if it doesn't exist
    save_dir = os.path.expanduser(dir)
    os.makedirs(save_dir, exist_ok=True)

    while True:
        name = f'screenshot{add}.png'
        file_path = os.path.join(save_dir, name)

        # Check if the file already exists
        if not os.path.exists(file_path):
            screenshot.save(file_path)
            print(f"Screenshot saved as {name}")
            break  # Exit the loop if save is successful
        else:
            add += 1  # Increment the counter if the file exists

if __name__ == '__main__':
    screensht()