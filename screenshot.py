from PIL import  ImageGrab
import os
def screensht():
    add = 0
    dir = '~/Pictures'
    screenshot = ImageGrab.grab()
    try:
        name = f'screenshot{add}.png'

        screenshot.save(os.path.join(os.path.expanduser(dir), name))  
    except FileExistsError:
      
        
         name = f'screenshot{add+1}.png'
         screenshot.save(os.path.join(os.path.expanduser(dir), name)) 
    return name
if __name__ == '__main__'
screensht()