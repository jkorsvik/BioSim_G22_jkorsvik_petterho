# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from src.biosim.simulation import BioSim
from src.biosim.animals import Carnivore, Herbivore, BaseAnimal

default_population = [
    {
        "loc": (3, 3),
        "pop": [
            {"species": "Herbivore", "age": 5, "weight": 20}
            for _ in range(2000)
        ],
    },
]
sim = BioSim(island_map='OOOOOOO\n'
                        'ODDDDDO\n'
                        'ODDDDDO\n'
                        'ODDDDDO\n'
                        'ODDDDDO\n'
                        'ODDDDDO\n'
                        'OOOOOOO', ini_pop=default_population,
             img_base='migrate_checker', ymax_animals=3000)
sim.set_animal_parameters('Herbivore', {'mu': 1e10, 'omega': 1e-10, 'eta': 1e-10})
print(Herbivore.mu, Herbivore.omega, Herbivore.eta, Herbivore.w_birth, Herbivore.sigma_birth)
sim.make_movie()