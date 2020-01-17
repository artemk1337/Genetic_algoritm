import pygame
from constants import BIRDS_SPRITE, BACKGROUND_SPRITE, PIPES_SPRITE

def load_image(path: str):
    image = pygame.image.load(path)
    image.convert()
    return image


def load_images():
    return {'background': load_image(BACKGROUND_SPRITE),
            'pipe': load_image(PIPES_SPRITE),
            'bird-1': load_image(BIRDS_SPRITE[0]),
            'bird-2': load_image(BIRDS_SPRITE[1]),
            'bird-3': load_image(BIRDS_SPRITE[2])}
