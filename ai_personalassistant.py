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

#task handler
def get_weather(city):
    api_key = "your_weather_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        speak(f"The weather in {city} is {weather} with a temperature of {temp}°C.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")


#reminder
import datetime

def set_reminder(task, time):
    speak(f"Reminder set for {task} at {time}.")
    # Optionally, you can integrate this with a scheduler like `schedule` or `apscheduler`.


#command processing 
def process_command(command):
    if "weather" in command:
        speak("Which city?")
        city = listen()
        if city:
            get_weather(city)
    elif "reminder" in command:
        speak("What should I remind you about?")
        task = listen()
        if task:
            speak("At what time?")
            time = listen()
            if time:
                set_reminder(task, time)
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {now}.")
    elif "search" in command:
        speak("What do you want to search for?")
        query = listen()
        if query:
            speak(f"Searching for {query}.")
            os.system(f"start https://www.google.com/search?q={query}")
    else:
        response = ai_response(command)
        speak(response)