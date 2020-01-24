# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from biosim.simulation import BioSim
import textwrap

default_population = [
    {
        "loc": (6, 9),
        "pop": [
            {"species": "Herbivore", "age": 5, "weight": 20}
            for _ in range(50)
        ],
    },
    {
        "loc": (2, 9),
        "pop": [
            {"species": "Herbivore", "age": 5, "weight": 20}
            for _ in range(50)
        ],
    },
    {
        "loc": (2, 3),
        "pop": [
            {"species": "Herbivore", "age": 5, "weight": 20}
            for _ in range(50)
        ],
    },
    {
        "loc": (6, 9),
        "pop": [
            {"species": "Carnivore", "age": 5, "weight": 20}
            for _ in range(10)
        ],
    }
]

desert_landscape = """
                 OOOOOOOOOOOOO
                 ODSSSDDDSDSDO
                 ODSDSDDSDSSDO
                 ODDDDDDDDSSDO
                 ODDDMMDSDDDDO
                 ODDMMSMMDSSDO
                 ODDDMDSDSSDDO
                 ODDDMMDMDSDDO
                 ODDSDSSMSDSDO
                 ODSDDMMMDDSDO
                 ODDDDSMDDDSDO
                 ODDSDSSDSDDDO
                 OOOOOOOOOOOOO
                 """
desert_landscape = textwrap.dedent(desert_landscape)

sim = BioSim(island_map=desert_landscape, ini_pop=default_population,
             img_base='desert_landscape', ymax_animals=800,
             cmax_animals={'Herbivore':40,
                           'Carnivore':30})
sim.set_animal_parameters('Herbivore', {'mu': 0.5,
                                        'eta': 0.1})
sim.set_animal_parameters('Carnivore', {'eta': 0.075,
                                        'F': 20,
                                        'mu': 0.5,
                                        'DeltaPhiMax': 0.75})
sim.simulate(1000)
sim.make_movie()
