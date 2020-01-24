# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from biosim.simulation import BioSim
import textwrap

default_population = [
    {
        "loc": (6, 6),
        "pop": [
            {"species": "Herbivore", "age": 5, "weight": 20}
            for _ in range(300)
        ],
    },
    {
        "loc": (6, 6),
        "pop": [
            {"species": "Carnivore", "age": 5, "weight": 20}
            for _ in range(10)
        ],
    }
]

half_island_map = """
                 OOOOOOOOOOOOO
                 OOOOOJJJOOOOO
                 OOOOOJJJOOOOO
                 OOOOOODOOOOOO
                 OOOOOODOOOOOO
                 OOOOOSSSOOOOO
                 OOOOSSSSSOOOO
                 OOOSSSJSSSSOO
                 OOSSSJOJSSSOO
                 OOSSSSJSSSOOO
                 OOOOSSSSSOOOO
                 OOOOOOSOOOOOO
                 OOOOOOOOOOOOO
                 """
half_island_map = textwrap.dedent(half_island_map)

sim = BioSim(island_map=half_island_map, ini_pop=default_population,
             img_base='half_island', ymax_animals=3000)
sim.simulate(1000)
sim.make_movie()