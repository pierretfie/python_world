#windows
import pyttsx3
from time import sleep
engine = pyttsx3.init(driverName='sapi5')  # For Window
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)
engine.setProperty('rate', 170)
engine.say("Hello, this is a test. Initializing sequence,please wait")
sleep(2)
engine.say('initialization complete')
engine.runAndWait()
sleep(3)

