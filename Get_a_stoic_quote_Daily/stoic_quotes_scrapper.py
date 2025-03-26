from requests import get
from bs4 import BeautifulSoup
from time import sleep
def stoic_quote():
    while True:
        try:
            # get will try to connect to url
            response = get('https://stoic-quotes.com/')
            # if connection fails we catch the error
        except Exception as e:
            print(f'request failed\n {e}')
            sleep(3)
            print('NO INTERNET')

            return 'NO INTERNET'
        # if connection is established we check the status code
        
        status = response.status_code
        sleep(1)
        if status == 200:
            soup = BeautifulSoup(response.text,'html.parser')
        # parsing a certain html line that seems to have the data we want
            results = soup.find_all('div',class_="css-1nyywr7")
            for result in results:
                return result.text
        
        
        else:
            print(f'returned status{status}')
        
            # when status code is not 200 say 404 or 403
            return f"Error: {status}"  # Stops retrying if we get an HTTP error
        
        
if __name__ == '__main__':
    quote = stoic_quote()
    print(quote)