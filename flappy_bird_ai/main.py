import pygame
import neat
import os
from ai import BestGenomeSaver, eval_genomes, test_best_genome, play_vs_ai
from game import Base, draw_window
from utils import FLOOR, WIN_WIDTH, WIN_HEIGHT

pygame.init()
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

TRAINING = False

def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    saver = BestGenomeSaver()
    p.add_reporter(saver)

    winner = p.run(eval_genomes, 1000)
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    draw_window(WIN, [], [], Base(FLOOR), 0, 0, 0)

    mode = input("Choisissez le mode (train/test/play): ").lower()

    if mode == "train":
        run(config_path)
    elif mode == "test":
        test_best_genome(config_path)
    elif mode == "play":
        play_vs_ai(config_path)
    else:
        print("Mode invalide. Veuillez choisir 'train', 'test' ou 'play'.")
