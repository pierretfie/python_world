from gtts import gTTS
import pygame
import os
import time

def text_to_speech(text, lang='en'):
    # Create the audio file
    tts = gTTS(text=text, lang=lang)
    tts.save("temp_audio.mp3")
    
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load and play the audio
    pygame.mixer.music.load("temp_audio.mp3")
    pygame.mixer.music.play()
    
    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    # Clean up
    pygame.mixer.quit()
    os.remove("temp_audio.mp3")

# Test the function
text = "The answer to the universe is 42"
text_to_speech(text)