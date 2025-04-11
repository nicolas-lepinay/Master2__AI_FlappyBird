import pygame
from flappy_bird_ai.utils import WIN_WIDTH, WIN_HEIGHT, FLOOR, blitRotateCenter
import random

# 🐤
class Bird:
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.IMGS = [pygame.transform.scale2x(pygame.image.load("assets/bird" + str(x) + ".png").convert_alpha()) for x in range(1, 4)]
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        displacement = self.vel * (self.tick_count) + 0.5 * (3) * (self.tick_count) ** 2

        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Tilt the bird
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

# 🧱
class Pipe:
    GAP = 200
    VEL = 12.5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(pygame.transform.scale2x(pygame.image.load("assets/pipe.png").convert_alpha()), False, True)
        self.PIPE_BOTTOM = pygame.transform.scale2x(pygame.image.load("assets/pipe.png").convert_alpha())

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(130, 370)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        # If not null --> collision
        if t_point or b_point:
            return True
        return False

# ⛰️
class Base:
    VEL = 5

    def __init__(self, y):
        self.IMG = pygame.transform.scale2x(pygame.image.load("assets/base.png").convert_alpha())
        self.WIDTH = self.IMG.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

# 🖼️
def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    from .utils import bg_img, STAT_FONT, DRAW_LINES # Import localement pour éviter les dépendances circulaires
    if gen == 0:
        gen = 1
    win.blit(bg_img, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        bird.draw(win)

    score_label = STAT_FONT.render("Score : " + str(score),1,(255,255,255))
    gen_label = STAT_FONT.render("Gens : " + str(gen-1),1,(255,255,255))
    alive_label = STAT_FONT.render("Alive : " + str(len(birds)),1,(255,255,255))

    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
    win.blit(gen_label, (10, 10))
    win.blit(alive_label, (10, 50))

    pygame.display.update()