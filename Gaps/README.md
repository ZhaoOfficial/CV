# GAPS

Genetic Algorithm based solver for jigsaw puzzles with piece size auto-detection.

A modification version of https://github.com/nemanja-m/gaps.

# Creating puzzles from images

To create puzzle from image use `create_puzzle` script.

i.e.

```bash
$ cd bin/
$ python create_puzzle.py images/pillars.jpg --size=48 --destination=puzzle.jpg
```

will create puzzle with `420` pieces from `images/pillars.jpg` where each piece is 48x48 pixels.


Run `create_puzzle --help` for detailed help.

__NOTE__ *Created puzzle dimensions may be smaller then original image depending on given puzzle piece size. Maximum possible rectangle is cropped from original image.*

:star: **Here we find that `.png` pictures preserve much better image quality than `.jpg`, so always generate `.png` pitures.**

# Solving puzzles

In order to solve puzzles, use `gaps` script.

i.e.

```bash
$ cd bin/
$ python solve.py --image=puzzle.jpg --generations=20 --population=600
```

This will start genetic algorithm with initial population of 600 and 20 generations.

Following options are provided:

Option          | Description
--------------- | -----------
`--source`      | Path to puzzle
`--size`        | Puzzle piece size in pixels
`--generations` | Number of generations for genetic algorithm
`--method`      | Method for calculating error. Options: "Mahalanobis" and "L2". 
`--population`  | Number of individuals in population
`--verbose`     | Show best solution after each generation
`--save`        | Save puzzle solution as image

Run `gaps --help` for detailed help.

## Size detection

If you don't explicitly provide `--size` argument to `gaps`, piece size will be detected automatically.

However, you can always provide `gaps` with `--size` argument explicitly:

```bash
$ gaps --image=puzzle.jpg --generations=20 --population=600 --size=48
```

__NOTE__ *Size detection feature works for the most images but there are some edge cases where size detection fails and detects incorrect piece size. In that case you can explicitly set piece size.*

## Termination condition

The termination condition of a Genetic Algorithm is important in determining when a GA run will end.
It has been observed that initially, the GA progresses very fast with better solutions coming in every few iterations,
but this tends to saturate in the later stages where the improvements are very small.

`gaps` will terminate:

* when there has been no improvement in the population for `X` iterations, or
* when it reaches an absolute number of generations
