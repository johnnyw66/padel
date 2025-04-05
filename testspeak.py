from gtts import gTTS
import pygame
import io
import tempfile

def notifyme_announce(text):
    # Create a gTTS object and get the speech as an in-memory stream
    tts = gTTS(text)
    speech_stream = io.BytesIO()
    tts.write_to_fp(speech_stream)

    # Save the in-memory stream to a temporary file
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_audio_file.write(speech_stream.getvalue())
    temp_audio_file.close()

    # Load and play the audio from the temporary file
    pygame.mixer.music.load(temp_audio_file.name)
    pygame.mixer.music.play()

    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


pygame.init()
notifyme_announce("You have 1 Padel opportunity!")
pygame.quit()

