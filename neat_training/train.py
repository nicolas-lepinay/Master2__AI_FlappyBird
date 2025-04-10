# neat_training/train.py
import pygame
import neat
import flappy_bird.constants as const  # importer le module complet
from flappy_bird.game import Bird, Pipe, Base, draw_window
from flappy_bird.constants import WIN_WIDTH, FLOOR

gen = 0

def eval_genomes(genomes, config):
    global gen
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
    run_sim = True
    while run_sim and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_sim = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1
        for i, bird in enumerate(birds):
            ge[i].fitness += 0.1
            bird.move()
            output = nets[i].activate((bird.y,
                                         abs(bird.y - pipes[pipe_ind].height),
                                         abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            for i, bird in enumerate(birds):
                if pipe.collide(bird, const.WIN):
                    ge[i].fitness -= 1
                    nets.pop(i)
                    ge.pop(i)
                    birds.pop(i)
                    break
            if pipe.x + pipes[0].PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and birds and pipe.x < birds[0].x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)
        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(i)
                ge.pop(i)
                birds.pop(i)

        draw_window(const.WIN, birds, pipes, base, score, gen, pipe_ind)

def run(config_path):
    import os
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))

    from neat_training.bestgenomesaver import BestGenomeSaver
    saver = BestGenomeSaver(filename="best.pickle")
    p.add_reporter(saver)
    winner = p.run(eval_genomes, 50)
    print('\nBest genome:\n{!s}'.format(winner))
