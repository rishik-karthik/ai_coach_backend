from io import BytesIO
from gtts import gTTS


class TextToSpeech:
    def speak(self, text, lang="en"):
        cleaned = (text or "").strip()

        if not cleaned:
            return
        
        buffer = BytesIO()
        #gTTS expects to save a file to your hard drive (e.g., audio.mp3). However, saving files to a hard
        #  drive and reading them back is very slow. 
        # BytesIO() creates a "fake file" that lives purely in your computer's temporary memory (RAM). It acts exactly like a file, but it is infinitely faster.
        gTTS(text=cleaned, lang=lang).write_to_fp(buffer)

        buffer.seek(0) #rewind to start

        return buffer.read()
    