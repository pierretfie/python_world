#windows
import pyttsx3
from time import sleep


def check_voice():

    engine = pyttsx3.init(driverName='sapi5')
    voice = engine.getProperty('voices')
    engine.setProperty('voice',  voice[1].id)
    engine.setProperty('rate', 170)
    engine.say('hello')
    engine.runAndWait()
if __name__ == '__main__':
    check_voice()
