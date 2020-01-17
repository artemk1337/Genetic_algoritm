import pygame
import pygame.sprite
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from utils import load_image
from random import randint
from flappybird.bird import Bird
from random import randint


class Pipes():
    WIDTH = 80
    GAP = 110
    VELOCITY = 10

    def __init__(self, pipe_img):

        self.x = SCREEN_WIDTH
        self.top = 0
        self.bottom = 0
        self.passed = False

        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img

        self.height = randint(100, 400)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + Pipes.GAP

    def update(self, dt):
        self.x -= Pipes.VELOCITY

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    @property
    def visible(self):
        return self.x > -Pipes.WIDTH

    @property
    def rect(self):
        """Get the Rect which contains this PipePair."""
        return pygame.Rect(self.x, 0, Pipes.WIDTH, Pipes.PIECE_HEIGHT)

    @property
    def top_mask(self):
        return pygame.mask.from_surface(self.PIPE_TOP)

    @property
    def bottom_mask(self):
        return pygame.mask.from_surface(self.PIPE_BOTTOM)


    def update(self, delta_frames=1):
        # ANIMATION_SPEED * frames_to_msec(delta_frames)
        self.x -= delta_frames*100

    def collides(self, bird: Bird):
        bird_mask = bird.mask
        top_pipes = self.top_mask

        top_offset = (int(self.x - bird.x), int(self.top - round(bird.y)))
        bottom_offset = (int(self.x - bird.x), int(self.bottom - round(bird.y)))

        b_point = bird.mask.overlap(self.bottom_mask, bottom_offset)
        t_point = bird.mask.overlap(self.top_mask,top_offset)
        return b_point or t_point
        # return pygame.sprite.collide_mask(self, bird)
