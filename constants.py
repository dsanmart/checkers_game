import pygame
import os

width = 800
height = 800
rows = 8
cols = 8
square_size = width//cols

# rgb colors used
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
grey = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load(os.path.join('pics/crown.png')), (44, 25))
