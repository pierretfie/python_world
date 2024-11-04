from gtts import gTTS
import os
from playsound import playsound

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    # Save to a temporary file
    tts.save("temp_audio.mp3")
    
    # Play the audio file
    playsound("temp_audio.mp3")
    
    # Clean up the temporary file
    os.remove("temp_audio.mp3")

# Test the function
text = "The answer to the universe is 42"
text_to_speech(text)