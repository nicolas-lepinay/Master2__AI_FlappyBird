# neat_training/bestgenomesaver.py
import neat
import pickle

class BestGenomeSaver(neat.reporting.BaseReporter):
    def __init__(self, filename="best.pickle"):
        super().__init__()
        self.best_fitness_so_far = float("-inf")
        self.filename = filename

    def post_evaluate(self, config, population, species, best_genome):
        if best_genome.fitness > self.best_fitness_so_far:
            self.best_fitness_so_far = best_genome.fitness
            print(f"==> NEW BEST FITNESS: {self.best_fitness_so_far:.2f}. Saving best genome to {self.filename}...")
            with open(self.filename, "wb") as f:
                pickle.dump(best_genome, f)
