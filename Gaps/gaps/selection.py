'''Selects fittest individuals from given population.'''

from typing import List, Tuple

import numpy as np

from gaps.individual import Individual


def roulette_selection(population: List[Individual], elites: int = 4) -> List[Tuple[Individual, Individual]]:
    '''Roulette wheel selection.

    Each individual is selected to reproduce, with probability directly
    proportional to its fitness score.

    :params population: Collection of the individuals for selecting.
    :params elite: Number of elite individuals passed to next generation.

    Usage::

        >>> from gaps.selection import roulette_selection
        >>> selected_parents = roulette_selection(population, 10)

    '''
    fitness_values = np.array([individual.fitness for individual in population])
    probability_intervals = np.cumsum(fitness_values)

    def select_individual() -> float:
        '''Selects random individual from population based on fitess value'''
        select_1 = np.random.uniform(0, probability_intervals[-1])
        select_2 = np.random.uniform(0, probability_intervals[-1])
        index_1, index_2 = np.searchsorted(probability_intervals, [select_1, select_2])
        
        return population[index_1], population[index_2]

    selected = []
    for _ in range(len(population) - elites):
        first, second = select_individual()
        selected.append((first, second))

    return selected
