# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from biosim.simulation import BioSim
import textwrap

default_population = [
    {
        "loc": (1, 2),
        "pop": [
            {"species": "Herbivore", "age": 5, "weight": 20}
            for _ in range(300)
        ],
    },
    {
        "loc": (1, 2),
        "pop": [
            {"species": "Carnivore", "age": 5, "weight": 20}
            for _ in range(4)
        ],
    }
]
checker_map = """
                 OOOOOOOOOO
                 OOJOJOJOJO
                 OJOJOJOJOO
                 OOJOJOJOJO
                 OJOJOJOJOO
                 OOJOJOJOJO
                 OJOJOJOJOO
                 OOJOJOJOJO
                 OJOJOJOJOO
                 OOOOOOOOOO
                 """
checker_map = textwrap.dedent(checker_map)

checker_map2 = """
                 OOOOOOOOOO
                 ODJDJDJDJO
                 OJDJDJDJDO
                 ODJDJDJDJO
                 OJDJDJDJDO
                 ODJDJDJDJO
                 OJDJDJDJDO
                 ODJDJDJDJO
                 OJDJDJDJDO
                 OOOOOOOOOO
                 """
checker_map2 = textwrap.dedent(checker_map2)

sim = BioSim(island_map=checker_map, ini_pop=default_population,
             img_base='checker_map_ocean', ymax_animals=500, cmax_animals={
        'Herbivore': 100, 'Carnivore':80
    })
sim.simulate(100)
sim.make_movie()