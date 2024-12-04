import getpass

def login():
    auth_user = getpass.getuser('Enter username:')
    autha_pass = getpass.getpass('Enter password: ')

if __name__ == '__main__':
    login()
