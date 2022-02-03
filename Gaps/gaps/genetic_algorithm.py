from operator import attrgetter
from typing import List
from time import time

from gaps import image_helpers
from gaps.selection import roulette_selection
from gaps.crossover import Crossover
from gaps.individual import Individual
from gaps.image_analysis import ImageAnalysis
from gaps.plot import Plot
from gaps.progress_bar import print_progress

import numpy as np


class GeneticAlgorithm(object):
    '''Genetic algorithm for puzzle solving'''
    TERMINATION_THRESHOLD = 3

    def __init__(
        self, image: np.ndarray, piece_size: int, population_size: int, generations: int, method: str, elite_size: int = 2
    ):
        self._image = image
        self._piece_size = piece_size
        self._generations = generations
        self._elite_size = elite_size
        self.method = method
        pieces, rows, columns = image_helpers.flatten_image(image, piece_size, indexed=True)
        self._population = [Individual(pieces, rows, columns) for _ in range(population_size)]
        self._pieces = pieces

    def start_evolution(self, verbose: bool):
        print('=== Pieces:        {}\n'.format(len(self._pieces)))

        t_start = time()
        ImageAnalysis.analyze_image(self._pieces, self.method)
        print('=== Analysis time: {}s'.format(time() - t_start))

        fittest = None
        best_fitness_score = np.NINF
        termination_counter = 0

        if verbose:
            plot = Plot(self._image)

        for generation in range(self._generations):
            print_progress(generation, self._generations - 1, prefix='=== Solving puzzle: ')

            new_population = []

            # Elitism
            elite = self._get_elite_individuals()
            new_population.extend(elite)

            selected_parents = roulette_selection(self._population, elites=self._elite_size)

            for first_parent, second_parent in selected_parents:
                crossover = Crossover(first_parent, second_parent)
                crossover.run()
                child = crossover.child()
                new_population.append(child)

            fittest = self._best_individual()

            if fittest.fitness <= best_fitness_score:
                termination_counter += 1
            else:
                best_fitness_score = fittest.fitness

            if termination_counter == self.TERMINATION_THRESHOLD:
                print('\n\n=== GA terminated')
                print('=== There was no improvement for {} generations'.format(self.TERMINATION_THRESHOLD))
                return fittest

            self._population = new_population

            if verbose:
                plot.show_fittest(fittest.to_image(), 'Generation: {} / {}'.format(generation + 1, self._generations))

        return fittest

    def _get_elite_individuals(self) -> List[Individual]:
        '''Returns first 'elite_count' fittest individuals from population'''
        # choose the last self._elite_size of the population
        return sorted(self._population, key = attrgetter('fitness'))[-self._elite_size:]

    def _best_individual(self) -> Individual:
        '''Returns the fittest individual from population'''
        return max(self._population, key = attrgetter('fitness'))
