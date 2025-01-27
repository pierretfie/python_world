import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None

# Example usage
speak("Hello! How can I assist you?")
command = listen()

import openai

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

def ai_response(query):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=query,
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()

# Example usage
query = "What is the capital of France?"
response = ai_response(query)
speak(response)