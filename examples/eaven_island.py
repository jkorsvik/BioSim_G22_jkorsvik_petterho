# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from biosim.simulation import BioSim

default_population = [
    {
        "loc": (1, 1),
        "pop": [
            {"species": "Herbivore", "age": 5, "weight": 20}
            for _ in range(150)
        ],
    },
    {
        "loc": (1, 1),
        "pop": [
            {"species": "Carnivore", "age": 5, "weight": 20}
            for _ in range(40)
        ],
    }
]
sim = BioSim(island_map='OOOO\nOJJO\nOJJO\nOOOO', ini_pop=default_population,
             img_base='square_island', ymax_animals=1000)
sim.simulate(100)
sim.make_movie()
