import pygame
from utils import load_images
from flappybird.bird import Bird
from flappybird.pipes import Pipes
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, WHITE, BLACK
from random import uniform


class Game:
    def __init__(self):
        self.run = True
        self.window = None
        self.resources = None
        self.pipes = []
        self.birds = []
        self.saved_birds = []
        self.clock = None
        self.next_pipe_timer = 0
        self.count = 1
        self.font = None
        self.current_generation = 1
        self.best_score = 0

    def create_pipe(self):
        return Pipes(self.resources["pipe"])

    def create_bird(self):
        return Bird(50, SCREEN_HEIGHT / 2,
                    [self.resources[f"bird-{i}"] for i in range(1, 3)])

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.run = False
            if event.key == pygame.K_g:
                self.count += 10
            if event.key == pygame.K_h:
                self.count -= 10
                if self.count <= 0:
                    self.count = 1

    def draw_bg(self):
        for x in (0, SCREEN_WIDTH / 2):
            self.screen.blit(self.resources['background'], (x, 0))

    def handle_birds(self, dt):
        for i in range(len(self.birds) - 1, -1, -1):
            b = self.birds[i]
            b.update(dt)
            b.think(self.pipes)
            b.draw(self.screen)
            if b.offscreen():
                self.saved_birds.append(self.birds.pop(i))
            else:
                for p in self.pipes:
                    if p.collides(b):
                        self.saved_birds.append(self.birds.pop(i))

    def handle_pipes(self, dt):
        for i, p in enumerate(self.pipes):
            p.update(dt)
            p.draw(self.screen)
        self.pipes = [x for x in self.pipes if x.visible]

    def reset_state(self):
        self.best_score = max(max([b.score for b in self.saved_birds]), self.best_score)
        self.birds = self.generate_birds()
        self.pipes = [self.create_pipe()]
        self.next_pipe_timer = 0

    def normalize_fitness(self):
        for i in range(len(self.saved_birds)):
            self.saved_birds[i].score **= 2

        sum = 0
        for b in self.saved_birds:
            sum += b.score

        for i in range(len(self.saved_birds)):
            self.saved_birds[i].fitness = self.saved_birds[i].score / sum

    def pool_selection(self, birds):
        r = uniform(0, 1)
        index = 0

        while r > 0:
            r -= birds[index].fitness
            index += 1
        index -= 1
        return birds[index].copy_with_mutation()
        fitness = 0
        b = None
        for bird in birds:
            if bird.fitness > fitness:
                fitness = bird.fitness
                b = bird
        if b is not None:
            return b
        return birds[randint(0, len(birds) - 1)]

    def generate_new_birds(self):
        new_birds = []
        for i in range(len(self.saved_birds)):
            b = self.pool_selection(self.saved_birds)
            new_birds.append(b)
        return new_birds

    def next_generation(self):
        self.current_generation += 1
        self.reset_state()
        self.normalize_fitness()
        self.birds = self.generate_new_birds()
        self.saved_birds = []

    def generate_birds(self, population=50):
        return [self.create_bird() for _ in range(population)]

    def add_pipe(self, dt):
        self.next_pipe_timer += dt
        if self.next_pipe_timer > 3:
            self.next_pipe_timer = 0
            self.pipes.append(self.create_pipe())

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.load_resources()
        self.clock = pygame.time.Clock()
        self.birds = self.generate_birds()
        self.pipes.append(self.create_pipe())
        self.count = 10
        while self.run:
            dt = self.clock.tick(FPS) / 1000
            for i in range(self.count):
                self.add_pipe(dt)
                event = pygame.event.poll()
                self.handle_events(event)
                self.screen.fill(WHITE)
                self.draw_bg()
                self.handle_birds(dt)
                self.handle_pipes(dt)
                if len(self.birds) == 0:
                    self.next_generation()
                self.draw_texts()
                pygame.display.flip()
        self.quit()

    def draw_text(self, text, position, text_color, bg_color=WHITE, alpha=50):
        label = self.font.render(text, True, text_color)
        surface = pygame.Surface((label.get_width(), label.get_height()))
        surface.fill(bg_color)
        surface.set_alpha(alpha)
        self.screen.blit(surface, position)
        self.screen.blit(label, position)

    def draw_texts(self):
        self.draw_text(
            f'Current generation: {self.current_generation}', (10, 10), BLACK, alpha=100)
        self.draw_text(
            f'Iteration/frame: {self.count}   (g +10 | h -10)', (10, 40), BLACK, alpha=100)
        self.draw_text(
            f'Current score: {self.birds[0].score}', (10, 70), BLACK, alpha=100)
        self.draw_text(
            f'Best score: {self.best_score}', (10, 100), BLACK, alpha=100)

    def quit(self):
        pygame.quit()

    def load_resources(self):
        self.font = pygame.font.Font('./assets/Roboto-Regular.ttf', 22)
        self.resources = load_images()
