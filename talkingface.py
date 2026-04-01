import pygame
import time
import sys


pygame.init()
width, height = 480, 320
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BMO Blinking Test")


try:
    face_normal = pygame.image.load("bmo_faces/idlers.png").convert()
    face_blink = pygame.image.load("bmo_faces/blinkrs.png").convert()
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

last_blink_time = time.time()
blink_duration = 0.15 
blink_interval = 4.0  


running = True
while running:
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    current_time = time.time()

   
    if current_time - last_blink_time > blink_interval:
        screen.blit(face_blink, (0, 0))
  
        if current_time - last_blink_time > (blink_interval + blink_duration):
            last_blink_time = current_time
    else:
        screen.blit(face_normal, (0, 0))

  
    pygame.display.flip()
    

    time.sleep(0.01) 

pygame.quit()
sys.exit()