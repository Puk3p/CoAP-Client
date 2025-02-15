import pygame
import os

# Inițializează pygame
pygame.init()

# Dimensiunea ferestrei
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinozaur Animat")

# Culori
BG_COLOR = (50, 50, 50)  # Fundal gri închis
BLACK = (0, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 30

# Încărcare sprite sheet
sprite_sheet_image = pygame.image.load('../../.assets/cat/redDino.png').convert_alpha()

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        """Decupează un cadru din sprite sheet."""
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image

# Creează sprite sheet-ul
sprite_sheet = SpriteSheet(sprite_sheet_image)

# Decupează cadrele animației, evitând cadrul 15
frames = [
    sprite_sheet.get_image(i, 24, 24, 4, BLACK)
    for i in range(24) if i != 15  # Excludem cadrul 15
]

# Poziția inițială a dinozaurului
dino_x = 50
dino_y = SCREEN_HEIGHT - 120  # La baza ecranului

# Viteza dinozaurului
dino_speed = 5

# Indexul cadrului curent
frame_index = 0

# Jocul rulează
run = True
while run:
    clock.tick(FPS)

    # Evenimente
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Fundal
    screen.fill(BG_COLOR)

    # Animația dinozaurului
    screen.blit(frames[frame_index], (dino_x, dino_y))

    # Actualizează cadrul
    frame_index += 1
    if frame_index >= len(frames):
        frame_index = 0

    # Mișcă dinozaurul spre dreapta
    dino_x += dino_speed
    if dino_x > SCREEN_WIDTH:  # Dacă iese din ecran, revine la stânga
        dino_x = -100

    # Actualizare ecran
    pygame.display.update()

# Închide pygame
pygame.quit()
