import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer


if not os.path.exists("model"):
    print("Please download the model from alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit(1)

model = Model("model")
rec = KaldiRecognizer(model, 16000)


p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("B.MO is listening... Speak now!")



while True:
    data = stream.read(4000, exception_on_overflow=False)
# Inside your while loop:
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result['text'].lower()

        # If any alias is in the text, swap it for "BMO"
        bmo_aliases = ["be mo", "bee mo", "beam oh", "b moe", "b move", "below", "dino", "the mo", "bmouth", "the know", "bmore", "the now", "the ammo", "be no", "v know", "bmow", "be know", "the email", "email", "beamer", "the my"]
        for alias in bmo_aliases:
            if alias in text:
                text = text.replace(alias, "bmo")
        
        print(f"B.MO heard: {text}")




def impression(character)

    if character == "cartman"



        