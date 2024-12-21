import pyttsx3
import random
import string
import qrcode
from os import path
from colorama import Fore, Style
import os

print(Fore.RED + '****************scripted by pierre-tfie********************')

def init_engine():
    if os.name == 'nt':
        engine = pyttsx3.init(driverName='sapi5')
        voice = engine.getProperty('voices')
        engine.setProperty('voice', voice[1].id)
        engine.setProperty('rate', 150)
        return engine
    return None

def password(engine):
    if engine:
        engine.say("hello, I'm Brain, you have requested a new password. What should be the password length?")
        engine.runAndWait()
    pass_length = input(Fore.RESET + 'ENTER LENGTH OF PASS TO GENERATE:\n')
    
    while not pass_length.isdigit():
        print(f'{Style.BRIGHT}{Fore.RED}ERROR!! ENTER A NUMBER:\n')
        if engine:
            engine.say('invalid input, reenter password length')
            engine.runAndWait()
        pass_length = input(f'{Style.RESET_ALL}{Fore.RESET}ENTER LENGTH OF PASS TO GENERATE:\n')
    
    if engine:
        engine.say('add the password usage')
        engine.runAndWait()
   
    filename = input('password use:\n')
    
    l = string.ascii_lowercase
    u = string.ascii_uppercase
    c = string.punctuation
    d = string.digits
    combination = l + u + c + d
    output = ''
    
    for i in range(int(pass_length)):
        output += random.choice(combination)
    return output, filename, pass_length

def create_qrcode(gen_output, engine):
    data, filename, pass_length = gen_output
    filename += '.png'
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=8,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='aqua')
    dir = path.expanduser('~/Documents')
    img.save(path.join(dir, filename))
    if engine:
        engine.say(f'your {pass_length} length password has been generated and saved in your Documents, nice time securing your accounts')
        engine.runAndWait()

if __name__ == '__main__':
    engine = init_engine()
    gen_output = password(engine)
    create_qrcode(gen_output, engine)
 