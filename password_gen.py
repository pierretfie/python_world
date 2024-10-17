
import random
import string
import qrcode
from os import path
from colorama import Fore, Style


print(Fore.RED+ '****************scripted by pierre-tfie********************')
def password(len):
    while True:
        if len[0] not in string.digits:
            print(Style.BRIGHT + 'ERROR!!ENTER A NUMBER:\n')
            len=input(Fore.RESET+'ENTER LENGTH OF PASS TO GENERATE:\n')
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
    print(f'{Fore.GREEN}password is >>>>>>>>>>>>\n\n\n{output}{Style.RESET_ALL}')
    data = output
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


password(len=input(Fore.RESET+'ENTER LENGTH OF PASS TO GENERATE:\n'))
