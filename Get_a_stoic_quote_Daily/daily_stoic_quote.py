from subprocess import run
#depends on a separate script 
from stoic_quotes_scrapper import stoic_quote
from plyer import notification
import os
import platform

def post_quote():
    notification.notify(
        title = 'Daily Stoic Quote',
        message = stoic_quote(),
        timeout = (300) #time in seconds
    )
    if platform.system() == 'Linux':
        try:
#change notification path based on your available notifications 
            os.system('paplay /usr/share/sounds/freedesktop/stereo/service-login.oga')
        except Exception as e:
            pass
    elif platform.system() == 'Windows':
        try:
            # Windows fallback using winsound (built-in)
            import winsound
            winsound.MessageBeep()
        except Exception as e:
            pass


if __name__ == '__main__':
    post_quote()