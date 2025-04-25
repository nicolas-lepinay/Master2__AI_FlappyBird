import pygame
import neat
import os
from ai import BestGenomeSaver, eval_genomes, test_best_genome, play_vs_ai
from game import Base, draw_window_training, UserQuitException
from utils import FLOOR, WIN_WIDTH, WIN_HEIGHT

pygame.init()
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

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

    try:
        winner = p.run(eval_genomes, 1000)
        print('\nBest genome:\n{!s}'.format(winner))
    except UserQuitException:
        print("👋 Entraînement interrompu par l'utilisateur.")


def main():
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird AI")
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    # Créer les instances des boutons
    from game import Button, draw_menu
    from utils import train_btn_img, test_btn_img, play_btn_img

    button_scale = 0.3
    train_button = Button(WIN_WIDTH // 2 - train_btn_img.get_width() * button_scale // 2, 200, train_btn_img, button_scale)
    test_button = Button(WIN_WIDTH // 2 - test_btn_img.get_width() * button_scale // 2, 350, test_btn_img, button_scale)
    play_button = Button(WIN_WIDTH // 2 - play_btn_img.get_width() * button_scale // 2, 500, play_btn_img, button_scale)

    menu_active = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if menu_active:
                draw_menu(win, train_button, test_button, play_button)

                if train_button.draw(win):
                    menu_active = False
                    run(config_path)
                    menu_active = True  # Retour au menu

                if test_button.draw(win):
                    menu_active = False
                    test_best_genome(config_path)
                    menu_active = True  # Retour au menu

                if play_button.draw(win):
                    menu_active = False
                    play_vs_ai(config_path)
                    menu_active = True  # Retour au menu
            else:
                # Un mode de jeu est actif
                pass

    pygame.quit()

if __name__ == "__main__":
    main()