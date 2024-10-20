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


    
    
if __name__ == '__main__':
    gen_output = password()
def create_qrcode():
    
create_qrcode()