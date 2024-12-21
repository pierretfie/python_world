import random
import string
import qrcode
from os import path
from colorama import Fore, Style
import os

print(Fore.RED+ '****************scripted by pierre-tfie********************')
def password():
    len=input(Fore.RESET+'ENTER LENGTH OF PASS TO GENERATE:\n')
    
    while True:
        if len[0] not in string.digits:
            print(f'{Style.BRIGHT}{Fore.RED}ERROR!!ENTER A NUMBER:\n')

            len=input(f'{Style.RESET_ALL}{Fore.RESET}ENTER LENGTH OF PASS TO GENERATE:\n')
        else:
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
    print(f'{Style.DIM}{Fore.RED} {output}')
    return output, filename, len


#store  the password in a QR code
def create_qrcode():
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
    print(f'{Style.NORMAL}{Fore.GREEN}your {len} length password has been generated and saved in your {dir}, nice time securing your accounts')
    print(Style.RESET_ALL) 
    
if __name__ == '__main__':
    gen_output = password()
    create_qrcode()
 