# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from src.biosim.landscape import *
import textwrap
from src.biosim.animals import *


class BioSim:
    map_params = {'O': Ocean,
                  'M': Mountain,
                  'D': Desert,
                  'S': Savanna,
                  'J': Jungle}

    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing
            animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal
            densities
        :param img_base: String with beginning of file name for figures,
            including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self._year = 0

        self.island_map = self.make_map(island_map)
        self.add_population(ini_pop)

    def make_map(self, island_map_string):
        island_map = {}
        lines = island_map_string.split('\n')
        for y, line in enumerate(lines):
            for x, letter in enumerate(line):
                island_map[(y, x)] = self.map_params[letter.upper()]()
        return island_map

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        globals()[species].set_parameters(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        globals()[landscape].set_parameters(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
            (default: vis_years)

        Image files will be numbered consecutively.
        """

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        # map_location is a dictionary with loc
        for map_location in population:
            loc = map_location['loc']
            pop = map_location['pop']
            self.island_map[loc].add_animals(pop)

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        num_animals = 0
        for num_type in self.num_animals_per_species.values():
            num_animals += num_type
        return num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        num_animals_per_species = {}
        num_herbivores = 0
        num_carnivores = 0

        for cell in self.island_map.values():
            num_herbivores += cell.num_herbivores
            num_carnivores += cell.num_carnivores

        num_animals_per_species['Herbivores'] = num_herbivores
        num_animals_per_species['Carnivores'] = num_carnivores

        return num_animals_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell
        on island."""
        raise NotImplementedError

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        raise NotImplementedError

    # The way i think it would be smart to do the work behind the simulation.
    # These are not obligatory, but the way i think it would be smart to do
    # the task.
    # - Petter

    def feed(self):
        for cell in self.island_map.values():
            cell.feed_all()

    def procreate(self):
        for cell in self.island_map.values():
            cell.procreate()

    def migrate(self):
        for cell in self.island_map.values():
            cell.migrate()

    def age_animals(self):
        for cell in self.island_map.values():
            cell.age()

    def lose_weight(self):
        for cell in self.island_map.values():
            cell.lose_weight()

    def die(self):
        for cell in self.island_map.values():
            cell.die()

    def simulate_one_year(self):
        self.feed()
        self.procreate()
        self.migrate()
        self.age_animals()
        self.lose_weight()
        self.die()

if __name__ == '__main__':
    geogr = """\
            OOO
            OJO
            OOO"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(50)
            ],
        }
    ]

    sim = BioSim(geogr, ini_herbs, 1)
    sim.simulate_one_year()
