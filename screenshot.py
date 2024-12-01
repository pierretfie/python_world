from PIL import  ImageGrab
import os
def screensht():
    add = 0
    dir = '~/Pictures'
    screenshot = ImageGrab.grab()
   
    name = f'screenshot{add}.png'

    screenshot.save(os.path.join(os.path.expanduser(dir), name))  
    if name in os.listdir(os.path.expanduser(dir)):
      
        
         name = f'screenshot{add+1}.png'
         screenshot.save(os.path.join(os.path.expanduser(dir), name)) 
    return name
if __name__ == '__main__':
    screensht()