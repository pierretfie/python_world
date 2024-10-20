import pyttsx3
import random
import string
import qrcode
from os import path
from colorama import Fore, Style

print(Fore.RED+ '****************scripted by pierre-tfie********************')
def password():
    engine = pyttsx3.init(driverName='sapi5')
    voice = engine.getProperty('voices')
    engine.setProperty('voice',  voice[1].id)
    engine.setProperty('rate', 150)
    engine.say("hello, I'm Brain, you have requested a new password. What should be the password length?")
    engine.runAndWait()
    len=input(Fore.RESET+'ENTER LENGTH OF PASS TO GENERATE:\n')
    
    while True:
        if len[0] not in string.digits:
            print(f'{Style.BRIGHT}{Fore.RED}ERROR!!ENTER A NUMBER:\n')

            engine.say('invalid input, reenter password length')
            engine.runAndWait()
            len=input(f'{Style.RESET_ALL}{Fore.RESET}ENTER LENGTH OF PASS TO GENERATE:\n')
        else:
            engine.say('add the password usage')
            engine.runAndWait()
            break
   
    filename = input('password use:\n')
    
    l = string.ascii_lowercase
    u = string.ascii_uppercase
    c = string.punctuation
    d = string.digits
    combination = l + u + c + d
    output = ''
    
    for i in range(int(len)):
        output += random.choice(combination)
    return output, filename, len


#store  the password in a QR code
def create_qrcode():
        
    engine = pyttsx3.init(driverName='sapi5')
    voice = engine.getProperty('voices')
    engine.setProperty('voice',  voice[1].id)
    engine.setProperty('rate', 150)
    data = gen_output[0]
    filename =  gen_output[1]
    len = gen_output[2]
    filename = filename+'.png'
    qr = qrcode.QRCode(
    version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=5,
    border=8,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='aqua' )
    dir = path.expanduser('~/Documents')
    img.save(path.join(dir, filename))
    engine.say(f'your {len} length password has been generated and saved in your Documents, nice time securing your accounts')
    engine.runAndWait()
    
if __name__ == '__main__':
    gen_output = password()
    create_qrcode()
 