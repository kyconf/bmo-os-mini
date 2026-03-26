import pygame
import sys
from datetime import datetime
import time
import busrequest

def print_text(text, duration):
    pygame.init()
    width, height = 480, 320
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("BMO Face")


    BMO_GREEN = (163, 255, 210)  # #a3ffd2
    TEXT_GREEN = (83, 138, 111)  # #538a6f


    font_path = "bmo_font.ttf"
    try:
        pixel_font = pygame.font.Font(font_path, 40) 
    except IOError:
        print(f"Could not find {font_path}, using default.")
        pixel_font = pygame.font.SysFont("Arial", 24)



    if isinstance(text, list):
        lines = text  
    else:
        lines = [text] 

    start = time.time()

    running = True
    while running:
        
        if time.time() - start >= duration:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BMO_GREEN)   

        

        for i, p in enumerate(lines):        
            text_surf = pixel_font.render(p, True, TEXT_GREEN)
            line_height = 40
            x_pos = width // 2
            y_pos = (height // 2) + (i * line_height) - (len(lines) * line_height // 2)
            text_rect = text_surf.get_rect(center=(x_pos, y_pos))
            screen.blit(text_surf, text_rect)
    
        
        pygame.display.flip()       

    pygame.quit()
    sys.exit()
    

def print_time():
    # you can change this depending on the size of your screen (i used a 3.5 TFT)
    pygame.init()
    width, height = 480, 320
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("BMO Face")


    BMO_GREEN = (163, 255, 210)  # #a3ffd2
    TEXT_GREEN = (83, 138, 111)  # #538a6f

  
    font_path = "bmo_font.ttf"
    try:

        pixel_font = pygame.font.Font(font_path, 80) 
    except IOError:
        print(f"Could not find {font_path}, using default.")
        pixel_font = pygame.font.SysFont("Arial", 24)

    running = True

    
    start = time.time()
    duration = 5
    while running:
        if time.time() - start >= duration:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = datetime.now()
        separator = ":" if now.second % 2 == 0 else " "
            
        # digital clock logic
        time_string = now.strftime(f"%I{separator}%M %p")
        text_surface = pixel_font.render(time_string, True, TEXT_GREEN)


        text_rect = text_surface.get_rect(center=(width // 2, height // 2))

        screen.fill(BMO_GREEN)       
        screen.blit(text_surface, text_rect)
        
        pygame.display.flip()       

    pygame.quit()
    sys.exit()

if __name__ in "__main__":
    print_text("hello", 5)