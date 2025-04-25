import pygame
import os

pygame.font.init()

WIN_WIDTH = 570
WIN_HEIGHT = 800
FLOOR = 730

STAT_FONT = pygame.font.SysFont("comicsans", 30)
END_FONT = pygame.font.SysFont("comicsans", 50)
DRAW_LINES = True

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird (AI)")

bg_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")).convert_alpha(), (600, 900))

train_btn_img = pygame.image.load(os.path.join("assets", "train_button.png")).convert_alpha()
test_btn_img = pygame.image.load(os.path.join("assets", "test_button.png")).convert_alpha()
play_btn_img = pygame.image.load(os.path.join("assets", "play_button.png")).convert_alpha()
quit_btn_img = pygame.image.load(os.path.join("assets", "quit_button.png")).convert_alpha()

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)