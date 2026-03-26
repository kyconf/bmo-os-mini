import os, json, time, sys, pygame, pyaudio, subprocess
import random
import busrequest
import snips_trainer
import displaytext
import video
from vosk import Model, KaldiRecognizer

pygame.init()
width, height = 480, 320
screen = pygame.display.set_mode((width, height))

face_idle = pygame.image.load("bmo_faces/idlers.png").convert()
face_blink = pygame.image.load("bmo_faces/blinkrs.png").convert()
face_listen = pygame.image.load("bmo_faces/thinkingrs.png").convert()


if not os.path.exists("model"):
    print("Download model first!")
    exit(1)

model = Model("model")
rec = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


is_awake = False
last_blink_time = time.time()
wake_time = 0 
WAKE_DURATION = 5.0 



print("B.MO OS Initialized...")
running = True


import gzip
import pickle
import rhasspynlu

def fast_load_brain(pickle_path="bmo_brain.pbz2"):
    try:
        with gzip.open(pickle_path, "rb") as f:
            print("BMO: Loading pre-trained brain... (Fast Boot)")
            return pickle.load(f)
    except FileNotFoundError:
        print("❌ ERROR: bmo_brain.pbz2 not found! Run 'python3.10 snips_trainer.py' first.")
        exit(1)

bmo_graph = fast_load_brain()


def parse_voice(text):
    recognitions = rhasspynlu.recognize(text, bmo_graph)
    if recognitions:
        result = recognitions[0]
        intent_name = result.intent.name
        
    
        if intent_name.startswith("__label__"):
            intent_name = intent_name.replace("__label__", "")
            
        slots = {s.entity: s.value for s in result.entities}
        return intent_name, result.intent.confidence, slots
    return None, 0, {}

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result['text'].lower()
        
        bmo_aliases = ["be mo", "bee mo", "beam oh", "b moe", "b move", "below", "dino", "the mo", "bmouth", "the know", "bmore", "the now", "the ammo", "be no", "v know", "bmow", "be know", "the email", "email", "beamer", "the my", "demo"]
        for alias in bmo_aliases:
            if alias in text:
                text = text.replace(alias, "bmo")

        if "coat" in text:
            text = text.replace("coat", "quote")
        

        
        print(f"B.MO heard (cleaned): {text}")

        # WAKE WORD LOGIC


        if "bmo" in text:
            print("WAKE WORD DETECTED")
            is_awake = True
            wake_time = time.time() 


            text = text.replace("bmo", "").strip()

        if is_awake:
            print(f"B.MO Hearing: {text}")

    # Intent 
        if is_awake and text: 
            intent, probability, slots = parse_voice(text)
            print(f"   Detected Intent: {intent}")
            print(f"   Confidence:      {probability:.2f} ({probability * 100:.1f}%)")
            
            if intent and probability > 0.6:
                print(f"Brain match! Intent: {intent}")
                is_thinking = True
                
                if intent == "greetuser":
                    video.play_video("hellobmo")
                
                elif intent == "gettime":
                    displaytext.print_time()

                elif intent == "telljoke":
                    handle_tell_joke(slots)
                elif intent == "bmobeep":
                    randombeep = ["beep1", "beep2"]
                    choice = random.choice(randombeep)
                    video.play_video(choice)
                elif intent == "isrobot":
                    video.play_video("ipad2")
                elif intent == "isbirthday":
                    video.play_video("birsday")
                elif intent == "getquote":
                    video.play_video("GiantLeap")
                elif intent == "playsong":
                    video.play_video("Daisy")
                elif intent == "getbus":
                    busrequest.get_bus()

                is_thinking = False
                is_awake = False 
            else:
                video.play_video("gameover")
                print("Brain didn't understand that command.")


        if is_awake and (time.time() - wake_time > WAKE_DURATION):
            print("B.MO is going back to sleep...")
            is_awake = False



    current_time = time.time()

    if is_awake:
    
        screen.blit(face_listen, (0, 0))
    else:

        if current_time - last_blink_time > 4.0: 
            screen.blit(face_blink, (0, 0))
            if current_time - last_blink_time > 4.15: # Blink duration
                last_blink_time = current_time
        else:
            screen.blit(face_idle, (0, 0))

    pygame.display.flip()

stream.stop_stream()
stream.close()
mic.terminate()
pygame.quit()