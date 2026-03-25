import os, json, time, sys, pygame, pyaudio
from vosk import Model, KaldiRecognizer

pygame.init()
width, height = 480, 320
screen = pygame.display.set_mode((width, height))

face_idle = pygame.image.load("bmo_faces/idlers.png").convert()
face_blink = pygame.image.load("bmo_faces/blinkrs.png").convert()
face_listen = pygame.image.load("bmo_faces/listening.png").convert()


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
WAKE_DURATION = 5.0 # How many seconds B.MO stays listening after his name


print("B.MO OS Initialized...")
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False


    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result['text'].lower()
        
        bmo_aliases = ["be mo", "bee mo", "beam oh", "b moe", "b move", "below", "dino", "the mo", "bmouth", "the know", "bmore", "the now", "the ammo", "be no", "v know", "bmow", "be know", "the email", "email", "beamer", "the my"]
        for alias in bmo_aliases:
            if alias in text:
                text = text.replace(alias, "bmo")
        
        print(f"B.MO heard (cleaned): {text}")
        # WAKE WORD LOGIC
        if "bmo" in text:
            print("!!! WAKE WORD DETECTED !!!")
            is_awake = True
            wake_time = time.time() 
        
        if is_awake:
            print(f"B.MO Hearing: {text}")

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