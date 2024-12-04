import getpass

def user_input():
    auth_user = input('Enter username:')
    autha_pass = getpass.getpass('Enter password: ')
    #you can add confirmation and password reference blocks
    return auth_user, autha_pass
def confirm():
    details = user_input()
    passwd = 'password'
    if details[0] == 'peter':
        if passwd == details[1]:
            print('Authentication successful')
        else:
            print('Authentication failed')
        exit()
    else:
        print('Unknown User')
confirm()



