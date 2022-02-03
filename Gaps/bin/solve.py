# Solves given jigsaw puzzle
# This module loads puzzle and initializes genetic algorithm
# with given number of generations and population.
# At the end, solution image is displayed.

import argparse
import os
import sys
from time import time
sys.path.append(os.pardir)

import cv2
import matplotlib.pyplot as plt

from gaps.genetic_algorithm import GeneticAlgorithm
from gaps.size_detector import SizeDetector
from gaps.plot import Plot

GENERATIONS = 20
POPULATION = 200


def show_image(img, title):
    if not args.verbose:
        Plot(img, title)
    plt.show()


def parse_arguments():
    '''Parses input arguments required to solve puzzle'''
    parser = argparse.ArgumentParser(description='A Genetic based solver for jigsaw puzzles')
    parser.add_argument('--source', type=str, default='out.jpg', help='Input image.')
    parser.add_argument('--generations', type=int, default=GENERATIONS, help='Num of generations.')
    parser.add_argument('--population', type=int, default=POPULATION, help='Size of population.')
    parser.add_argument('--size', type=int, help='Single piece size in pixels.')
    parser.add_argument('--method', type=str, default='L2', help='Method for calculating error, "Mahalanobis" and "L2".')
    parser.add_argument('--verbose', action='store_true', help='Show best individual after each generation.')
    parser.add_argument('--save', action='store_true', help='Save puzzle result as image.')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    image = cv2.imread(args.source)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if args.size is not None:
        piece_size = args.size
    else:
        detector = SizeDetector(image)
        piece_size = detector.detect_piece_size()

    print('\n=== Population:    {}'.format(args.population))
    print('=== Generations:   {}'.format(args.generations))
    print('=== Piece size:    {} px'.format(piece_size))
    print('=== Error methods: {}'.format(args.method))

    # Let the games begin! And may the odds be in your favor!
    start = time()
    algorithm = GeneticAlgorithm(image, piece_size, args.population, args.generations, args.method)
    solution = algorithm.start_evolution(args.verbose)
    end = time()

    print('\n=== Done in {0:.3f} s'.format(end - start))

    solution_image = solution.to_image()
    solution_image_name = os.path.splitext(args.source)[0] + '_solution.jpg'

    if args.save:
        solution_image = cv2.cvtColor(solution_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(solution_image_name, solution_image)
        print('=== Result saved as "{}"'.format(solution_image_name))

    print('=== Close figure to exit')
    show_image(solution_image, 'Solution')
