from PIL import  ImageGrab
import os
def screensht():
    add = 0
    dir = '~/Pictures'
    screenshot = ImageGrab.grab()
   
    name = f'screenshot{add}.png'

    screenshot.save(os.path.join(os.path.expanduser(dir), name)) 
    files = os.listdir(os.path.expanduser(dir))
    while True: 
      
        if name in files:

      
        
            name = f'screenshot{add+1}.png'
         
            screenshot.save(os.path.join(os.path.expanduser(dir), name)) 
        return name
if __name__ == '__main__':
    screensht()