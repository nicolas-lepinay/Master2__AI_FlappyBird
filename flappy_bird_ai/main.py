import pygame
import neat
import os
from flappy_bird_ai.ai import BestGenomeSaver, eval_genomes, test_best_genome

pygame.init()
WIN = pygame.display.set_mode((570, 800))

gen = 0

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
    saver = BestGenomeSaver(filename="best.pickle")
    p.add_reporter(saver)

    winner = p.run(eval_genomes, 1000)
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    if TRAINING:
        run(config_path)
    else:
        test_best_genome(config_path)