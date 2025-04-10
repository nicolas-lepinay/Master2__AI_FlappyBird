# flappy_bird/constants.py
import os
import pygame

# Dimensions et positions
WIN_WIDTH = 570
WIN_HEIGHT = 800
FLOOR = 730

# Option de débogage
DRAW_LINES = False

# Variables pour les polices et images (initialement vides)
STAT_FONT = None
END_FONT = None
pipe_img = None
bg_img = None
bird_images = []  # liste vide initialement
base_img = None

# La fenêtre Pygame (sera assignée depuis main.py)
WIN = None


def load_assets():
    """
    Charge les polices et images après l'initialisation du display.
    Au lieu de réaffecter la variable bird_images, on met à jour la liste en place.
    """
    global STAT_FONT, END_FONT, pipe_img, bg_img, base_img
    pygame.font.init()
    STAT_FONT = pygame.font.SysFont("comicsans", 30)
    END_FONT = pygame.font.SysFont("comicsans", 50)

    # Charger les images
    pipe_img_raw = pygame.image.load(os.path.join("assets", "pipe.png")).convert_alpha()
    pipe_img = pygame.transform.scale2x(pipe_img_raw)

    bg_img_raw = pygame.image.load(os.path.join("assets", "bg.png")).convert_alpha()
    bg_img = pygame.transform.scale(bg_img_raw, (600, 900))

    # Charger les images de l'oiseau
    bird_images_raw = [
        pygame.image.load(os.path.join("assets", f"bird{x}.png")).convert_alpha()
        for x in range(1, 4)
    ]
    images = [pygame.transform.scale2x(img) for img in bird_images_raw]
    # Mettre à jour la liste existante en place (pour que les modules l'utilisant voient le contenu mis à jour)
    bird_images.clear()
    bird_images.extend(images)

    base_img_raw = pygame.image.load(os.path.join("assets", "base.png")).convert_alpha()
    base_img = pygame.transform.scale2x(base_img_raw)

    # Réassigner les variables globales (pour les autres modules qui les importent via "import flappy_bird.constants as const", par exemple)
    globals()['pipe_img'] = pipe_img
    globals()['bg_img'] = bg_img
    globals()['base_img'] = base_img
