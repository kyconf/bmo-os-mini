import pygame
import sys

# 1. SETUP THE WINDOW
pygame.init()
width, height = 480, 320
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BMO Face")

# 2. COLORS (Hex converted to RGB)
BMO_GREEN = (163, 255, 210)  # #a3ffd2
TEXT_GREEN = (83, 138, 111)  # #538a6f

# 3. SETUP THE FONT
font_path = "bmo_font.ttf"
try:
    # Pygame uses its own font loader
    pixel_font = pygame.font.Font(font_path, 32) 
except IOError:
    print(f"Could not find {font_path}, using default.")
    pixel_font = pygame.font.SysFont("Arial", 24)

# 4. PRE-RENDER THE TEXT
# (Text, Antialias, Color)
text_surface = pixel_font.render("BMO IS ONLINE", True, TEXT_GREEN)

# Get the rectangle of the text to center it easily
text_rect = text_surface.get_rect(center=(width // 2, height // 2))

# 5. MAIN LOOP
running = True
while running:
    # Check for exit events (so the window closes properly)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 6. DRAWING
    screen.fill(BMO_GREEN)        # Fill background
    screen.blit(text_surface, text_rect) # Draw text in the center
    
    pygame.display.flip()        # Update the physical display

pygame.quit()
sys.exit()