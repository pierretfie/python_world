#for updating tokens on already cloned github repositories 

from subprocess import run

def update_token():
    credential_cache = ['git', 'credential-cache', 'exit']
    new_token = input('Enter new token: ')
    username = input('Enter github username: ')
    repository = input('Enter target repository name: ')
    update_token_url = ['git', 'remote', 'set-url', 'origin', f'https://{new_token}@github.com/{username}/{repository}.git'] 
    try:
        run(credential_cache)
        run(update_token_url)
    except Exception as e:
        print(f'an error:{e} occurred while updating new access token')
    else:
        print('Private git remote Access token update successfully')

if __name__ == '__main__':
    update_token()