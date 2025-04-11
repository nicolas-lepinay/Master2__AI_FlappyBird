import neat
import pickle
import pygame
from flappy_bird_ai.game import Bird, Pipe, Base
from flappy_bird_ai.utils import FLOOR, WIN_WIDTH, WIN

class BestGenomeSaver(neat.reporting.BaseReporter):
    def __init__(self, filename="best.pickle"):
        super().__init__()
        self.best_fitness_so_far = float("-inf")
        self.filename = filename

    def post_evaluate(self, config, population, species, best_genome):
        if best_genome.fitness > self.best_fitness_so_far:
            self.best_fitness_so_far = best_genome.fitness
            print(f"\n🏆 NEW BEST FITNESS : {self.best_fitness_so_far:.2f}. Saving best genome to {self.filename}...\n")
            with open(self.filename, "wb") as f:
                pickle.dump(best_genome, f)

def eval_genomes(genomes, config):
    global WIN, gen
    gen += 1

    nets = []
    birds = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()
    run = True
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            for bird in birds:
                if pipe.collide(bird, WIN):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        from .game import draw_window # Import localement
        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)

    return # Implicit return

def test_best_genome(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    with open("best.pickle", "rb") as f:
        best_genome = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(best_genome, config)

    bird = Bird(230, 350)
    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1

        output = net.activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
        if output[0] > 0.5:
            bird.jump()

        bird.move()
        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird, WIN):
                run = False
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= FLOOR or bird.y < -50:
            run = False

        from game import draw_window # Import localement
        draw_window(WIN, [bird], pipes, base, score, 0, pipe_ind)

    print("Test terminé. Score final :", score)

def play_vs_ai(config_path):
    """
    Permet à un joueur humain de jouer contre l'IA entraînée.
    """
    # Charger la configuration NEAT
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # Charger le meilleur génome de l'IA
    try:
        with open("best.pickle", "rb") as f:
            best_genome = pickle.load(f)
    except FileNotFoundError:
        print("Erreur : Le fichier best.pickle n'a pas été trouvé. Veuillez d'abord entraîner l'IA.")
        return

    # Créer le réseau neural de l'IA
    ai_net = neat.nn.FeedForwardNetwork.create(best_genome, config)

    # Initialiser les oiseaux, le joueur en premier
    player = Bird(150, 350, is_player = True)
    ai_bird = Bird(230, 350)

    base = Base(FLOOR)
    pipes = [Pipe(700)]

    score_player = 0
    score_ai = 0

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.jump()

        # Logique de l'IA pour sauter
        pipe_ind = 0
        if len(pipes) > 1 and ai_bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1
        output = ai_net.activate((ai_bird.y, abs(ai_bird.y - pipes[pipe_ind].height), abs(ai_bird.y - pipes[pipe_ind].bottom)))
        if output[0] > 0.5:
            ai_bird.jump()

        # Déplacer les oiseaux, le sol et les tuyaux
        player.move()
        ai_bird.move()
        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()

            # Vérifier les collisions
            if pipe.collide(player, WIN):
                print("Le joueur a perdu ! Score :", score_player)
                run = False
            if pipe.collide(ai_bird, WIN):
                print("L'IA a perdu ! Score :", score_ai)
                run = False

            if not pipe.passed and pipe.x < player.x and not pipe.passed_player:
                pipe.passed_player = True
                add_pipe = True
                score_player += 1
            if not pipe.passed and pipe.x < ai_bird.x and not pipe.passed_ai:
                pipe.passed_ai = True
                # Vous pouvez choisir de donner un score différent à l'IA si vous le souhaitez
                score_ai += 1
            elif pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
                pipe.passed = False # Réinitialiser pour les nouveaux tuyaux

        if add_pipe:
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        # Vérifier si les oiseaux touchent le sol ou sortent de l'écran
        if player.y + player.img.get_height() >= FLOOR or player.y < -50:
            print("Le joueur a touché le sol ou est sorti de l'écran ! Score :", score_player)
            run = False
        if ai_bird.y + ai_bird.img.get_height() >= FLOOR or ai_bird.y < -50:
            print("L'IA a touché le sol ou est sortie de l'écran ! Score :", score_ai)
            run = False

        from game import draw_window_vs_ai # Import localement
        draw_window_vs_ai(WIN, player, ai_bird, pipes, base, score_player, score_ai)

    pygame.quit()
    quit()


