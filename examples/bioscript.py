import textwrap
import matplotlib.pyplot as plt

from src.biosim.simulation import BioSim
from pprint import pprint

"""
Compatibility check for BioSim simulations.

This script shall function with biosim packages written for
the INF200 project January 2019.
"""

__author__ = "Hans Ekkehard Plesser, NMBU"
__email__ = "hans.ekkehard.plesser@nmbu.no"


if __name__ == "__main__":

    ini_herbs = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]

    sim = BioSim(ini_pop=ini_herbs, seed=123456)

    """
    sim.set_animal_parameters("Herbivore", {"zeta": 3.2, "xi": 1.8})
    sim.set_animal_parameters(
        "Carnivore",
        {
            "a_half": 70,
            "phi_age": 0.5,
            "omega": 0.3,
            "F": 65,
            "DeltaPhiMax": 9.0,
        },
    )
    sim.set_landscape_parameters("J", {"f_max": 700})
    """
    sim.simulate(50)
    #simulate(num_years=100, vis_years=1, img_years=2000)

    sim.add_population(population=ini_carns)
    #sim.simulate(num_years=100, vis_years=1, img_years=2000)
    sim.simulate(150)
