#a model for answering greetings(rule-based model)
from subprocess import run
import random
import nltk
from nltk.tokenize import word_tokenize

#first we need a dataset for possible greetings(we can make it formal)
def greet_response (user_input):
    #we will use a dictionary to map the user's input to a response
    greetings = ["hello", "hi", "hey", "greetings", "what's up", "hola"]
    responses = [
    "Hello! How can I help you?",
    "Hi there! What do you need?",
    "Hey! What's on your mind?",
    "Greetings! How can I assist you today?",
    "What's up? How can I help?"
    ]
    #use tokenization makes it easier to repond 
    # to different greetings with a single word know to the model eg 'hi'
    user_input = user_input.lower()
    #we are breaking down the user iput
    try:

        tokens = word_tokenize(user_input)
    except Exception as e:
        nltk.download('punkt')
        nltk.download('punkt_tab')
    else:
        pass

    #filter response
    for token in tokens:
        if token in greetings:
            #return a response which is at the same position as the greeting
            return random.choice(responses)
    return  "Sorry, I didn't understand that."

user_input = input('You:')
response = greet_response(user_input)
print('Bot:', response)
try:
    run(['espeak',response])
except Exception as e:
    import pyttsx3
    engine = pyttsx3.init(driverName='sapi5')
    voice = engine.getProperty('voices')
    engine.setProperty('voice',voice[0].id )
    engine.setProperty('rate', 190)
    engine.say(response)
    engine.runAndWait()

#increase the dataset
#build a model that would handle greetings(use pretrained  model)



