import pyttsx3

engine = pyttsx3.init(driverName='espeak')

# List all available voices
voices = engine.getProperty('voices')

# Set a voice that you know should work
engine.setProperty('voice', voices.id)  # Try the first available voice

engine.say("Hello, this is a test.")
engine.runAndWait()
