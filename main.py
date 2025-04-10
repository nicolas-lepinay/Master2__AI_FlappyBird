# main.py
import os
import pygame
import flappy_bird.constants as const
from flappy_bird.constants import WIN_WIDTH, WIN_HEIGHT, load_assets
from neat_training.train import run

def main():
    pygame.init()
    # Crée la fenêtre et assigne-la à la variable globale WIN
    const.WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    # Charger les assets (doit être appelé après la création de la fenêtre)
    load_assets()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

if __name__ == "__main__":
    main()
