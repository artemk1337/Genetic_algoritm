import pygame
import pygame.sprite
import constants
from utils import load_image
import bbnet
from bbnet.nn import NeuralNetwork
import random
import numpy as np


def mutate(x):
    if random.uniform(0, 1) < 0.9:
        offset = np.random.normal() * 0.5
        newx = x + offset
        return newx
    else:
        return x


class Bird():
    WIDTH = 34
    HEIGHT = 24

    def __init__(self, x, y, images, brain=None):
        self.x = x
        self.y = y
        self.images = images
        self.index_animation = 0
        self.image = self.images[self.index_animation]
        self.time_animation = 0.0
        self.vel_y = 0
        self.fitness = 0
        self.score = 0
        if not brain:
            self.brain = NeuralNetwork(5, 10, 1)
        elif isinstance(brain, NeuralNetwork):
            self.brain = NeuralNetwork.copy(brain)
            self.brain.mutate(mutate)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def think(self, pipes):
        closest_pipe = None
        rec = 999999  # :)
        for pipe in pipes:
            diff = pipe.x - self.x
            if diff > 0 and diff < rec:
                rec = diff
                closest_pipe = pipe
        if not closest_pipe:
            return
        output = self.brain.guess(
            [self.y, closest_pipe.top, closest_pipe.bottom, closest_pipe.x, self.vel_y])
        if output[0] > 0.5:
            self.jump()

    def copy_with_mutation(self):
        return Bird(self.x, self.y, self.images, brain=self.brain)

    @property
    def mask(self):
        return pygame.mask.from_surface(self.image)

    def update_animatiom(self, dt):
        self.time_animation += dt
        if self.time_animation >= 0.15:
            self.time_animation = 0
            self.index_animation += 1
            if self.index_animation >= len(self.images):
                self.index_animation = 0
            self.image = self.images[self.index_animation]

    def offscreen(self):
        return self.y <= 0 or self.y >= constants.SCREEN_HEIGHT

    def update(self, dt):
        self.score += 1
        self.update_animatiom(dt)
        if self.y < 0:
            self.vel_y = 0
            self.y = 0
        elif not self.y > constants.SCREEN_HEIGHT:
            self.vel_y += 0.5
            self.y += self.vel_y
        else:
            self.dead = True

    def jump(self):
        self.vel_y = -5
