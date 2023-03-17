import pygame
import sys
from time import perf_counter

import prediction

# Creates the window
pygame.init()
screen = pygame.display.set_mode((280, 280+50))
pygame.display.set_caption('Image Processing')

clock = pygame.time.Clock()

# Loads the font
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 15)

# Creates the image grid
pixels = []
top_margin = 50

columns = screen.get_width()
rows = screen.get_height() - top_margin

brush_size = 10
guess_interval = 3 # seconds
guesses = ""

def generate_list():
    global pixels
    pixels = []

    for x in range(columns):
        pixels.append([])
        for y in range(rows):
            pixels[x].append(0)

generate_list()

def render():
    '''Handles drawing the game'''

    global guesses, _last, dt

    screen.fill((255, 255, 255))

    # Top margin
    pygame.draw.rect(screen, (126, 126, 126), (0, 0, screen.get_width(), top_margin))

    # Renders the pixels
    for x in range(columns):
        for y in range(rows):
            if pixels[x][y] == 1:
                pygame.draw.rect(screen, (0, 0, 0), (x, y + top_margin, 1, 1))

    # Handles the guess text
    if dt >= guess_interval:
        _last = current
        predictions = prediction.predict(pixels)
        guesses = ", ".join(predictions)
    
    text = font.render(f'Guesses: {guesses}', False, (0, 0, 0))
    screen.blit(text, (0, 0))
        
    pygame.display.update()
    clock.tick(120)

def input():
    '''Handles user input'''
    pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed(3)

    keys = pygame.key.get_pressed()

    # Handles drawing
    if pos[1] >= top_margin:
        if pressed[0]:
            for x in range(brush_size):
                for y in range(brush_size):
                    try:
                        pixels[pos[0] + x][pos[1] - top_margin + y] = 1
                    except IndexError as e:
                        ...

    # Clears array to draw again
    if keys[pygame.K_SPACE]:
        generate_list()


dt = 0
_last = perf_counter()
while True:
    current = perf_counter()
    dt = current - _last

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    input()
    render()