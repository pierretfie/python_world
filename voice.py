#windows
import pyttsx3
from time import sleep
engine = pyttsx3.init(driverName='sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice',  voice[1].id)
engine.setProperty('rate', 170)
engine.say('hello')
engine.runAndWait()
