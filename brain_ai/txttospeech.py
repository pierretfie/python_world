from gtts import gTTS
from IPython.display import Audio
import os

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    # Save to a temporary file
    tts.save("temp_audio.mp3")
    
    # Read the audio file
    with open("temp_audio.mp3", "rb") as audio_file:
        audio_bytes = audio_file.read()
    
    # Clean up the temporary file
    os.remove("temp_audio.mp3")
    
    return audio_bytes

# Test the function
text = "The answer to the universe is 42"
audio_bytes = text_to_speech(text)
Audio(audio_bytes)