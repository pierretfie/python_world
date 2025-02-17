from requests import get
from bs4 import BeautifulSoup
from time import sleep
def meaning():
    word = input('welcome to the wiki dictionary\n'
                 'what would you like me to search the meaning for?\n')
    print(f'searching meaning or information for {word.lower()}')
    try:
        # get will try to connect to url
        response = get(f'https://simple.wikipedia.org/wiki/{word.replace(' ','_')}')
        # if connection fails we catch the error
    except Exception as e:
        print(f'request failed\n {e}')
        sleep(3)
        print('NO INTERNET')
        pass
    # if connection is established we check the status code
    else:
        status = response.status_code
        print('printing results...............\n\n\n\n')
        sleep(1)
        if status == 200:
            pass
        else:
            # when status code is not 200 say 404 or 403
            print(f'failed {status}')
            try:
                print(f'trying https://en.wikipedia.org/wiki/{word.replace(' ','_')}')
                response = get(f'https://en.wikipedia.org/wiki/{word.replace(' ','_')}')
            except Exception as e:
                print(f'request failed again {e}')
            else:
                pass
        soup = BeautifulSoup(response.text,'html.parser')
        # parsing a certain html line that seems to have the data we want
        results = soup.find_all('div',class_="mw-body-content")
        for result in results:
            print(result.text)
meaning()