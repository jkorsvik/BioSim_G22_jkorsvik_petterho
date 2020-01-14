# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from src.biosim.landscape import *
import textwrap
from src.biosim.animals import *


def check_length(*args):
    if not all(len(args[0]) == len(_arg) for _arg in args[1:]):
        return False
    return True


def choose_new_location(prob_list):
    """
    Draws one out of a list with weights.

    Parameters
    ----------
    prob_list - list of tuple(loc, probabilities)

    Returns
    -------
    new_location - tuple of (y, x)
    """
    probabilities = [x[1] for x in prob_list]
    cumulative_sum = np.cumsum(probabilities)
    locations = [x[0] for x in prob_list]
    index = 0
    while not np.random.binomial(1, cumulative_sum[index]):
        index += 1
    return locations[index]


class Island:
    map_params = {'O': Ocean,
                  'M': Mountain,
                  'D': Desert,
                  'S': Savanna,
                  'J': Jungle}

    def __init__(self, island_map_string, ini_pop):
        self.map = self.make_map(island_map_string)
        self.add_population(ini_pop)

    @property
    def num_animals(self):
        """
        Total number of animals on island.

        Returns
        -------
        num_animals - int
        """
        num_animals = 0
        for num_type in self.num_animals_per_species.values():
            num_animals += num_type
        return num_animals

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.

        Returns
        -------
        num_animals_per_species - dictionary
        """
        num_animals_per_species = {}
        num_herbivores = 0
        num_carnivores = 0

        for cell in self.map.values():
            num_herbivores += cell.num_herbivores
            num_carnivores += cell.num_carnivores

        num_animals_per_species['Herbivore'] = num_herbivores
        num_animals_per_species['Carnivore'] = num_carnivores

        return num_animals_per_species

    @staticmethod
    def clean_multi_line_string(island_map_string):
        """
        Strips and splits a multilinestring and checks for equal length
        of lines and specific letters at the edges: in this case 'O'.
        Raises ValueError if criteria are not met.

        Parameters
        ----------
        island_map_string - multilinestring

        Returns
        -------
        lines - a list of lines of strings (cleaned)
        """
        island_map_string = island_map_string.strip()
        lines = island_map_string.split('\n')

        if not check_length(lines):
            raise ValueError('Each line of the multi line string, '
                             'shall be equal in length')

        for x in range(len(lines[0])):
            if lines[0][x] is not 'O' or lines[-1][x] is not 'O':
                raise ValueError('')
        for y in range(len(lines)):
            if lines[y][0] is not 'O' or lines[y][-1] is not 'O':
                raise ValueError('')

        return lines

    def make_map(self, island_map_string):
        """
        Creates a dictionary data frame that stores instances of cells
        by key: a tuple of (y, x)-coordinates

        Parameters
        ----------
        island_map_string

        Returns
        -------
        map - dictionary

        """
        map = {}
        lines = self.clean_multi_line_string(island_map_string)
        for y, line in enumerate(lines):
            for x, letter in enumerate(line):
                if letter in self.map_params.keys():
                    map[(y, x)] = self.map_params[letter]()
                else:
                    raise ValueError(f'String must consist of uppercase'
                                     f'letters like these:\n'
                                     f'{self.map_params}')
        return map

    def probability_calc(self, pos, animal):
        species = animal.__class__.__name__
        y, x = pos
        loc_1 = (y - 1, x)
        loc_2 = (y + 1, x)
        loc_3 = (y, x - 1)
        loc_4 = (y, x + 1)
        option_1 = self.map[loc_1]
        option_2 = self.map[loc_2]
        option_3 = self.map[loc_3]
        option_4 = self.map[loc_4]

        list_ = [(loc_1, option_1), (loc_2, option_2),
                 (loc_3, option_3), (loc_4, option_4)]
        propensity_list = []

        for loc, option in list_:
            propensity_list.append((loc,
                                    option.propensity[species])
                                   )

        prop_sum = np.sum(sum(dict(propensity_list).values()))
        prob_list = []
        for loc, prop in propensity_list:
            prob_list.append((loc, (prop / prop_sum)))

        return prob_list

    def add_herb_to_new_cell(self, new_loc, herbivore):
        self.map[new_loc].add_migrated_herb(herbivore)

    def add_carn_to_new_cell(self, new_loc, carnivore):
        self.map[new_loc].add_migrated_carn(carnivore)

    def migrate(self):
        for pos, cell in self.map.items():
            deletion_list = []
            if cell.passable and cell.num_animals > 0:
                if cell.num_herbivores > 0:
                    for herbivore in cell.herbivores:
                        if not herbivore.has_moved:
                            if not herbivore.will_migrate():
                                continue
                            prob_list = self.probability_calc(pos, herbivore)
                            try:
                                new_loc = choose_new_location(prob_list)
                            except ValueError:
                                new_loc = pos
                            deletion_list.append(herbivore)
                            self.add_herb_to_new_cell(new_loc, herbivore)
                    for herbivore in deletion_list:
                        cell.remove_migrated_herb(herbivore)

                deletion_list = []
                if cell.num_carnivores > 0:
                    for carnivore in cell.carnivores:
                        if not carnivore.has_moved:
                            if not carnivore.will_migrate():
                                continue
                            prob_list = self.probability_calc(pos, carnivore)
                            try:
                                new_loc = choose_new_location(prob_list)
                            except ValueError:
                                new_loc = pos
                            deletion_list.append(carnivore)
                            self.add_carn_to_new_cell(new_loc, carnivore)
                    for carnivore in deletion_list:
                        cell.remove_migrated_carn(carnivore)

    def ready_for_new_year(self):
        for cell in self.map.values():
            cell.grow()
            for herbivore in cell.herbivores:
                herbivore.reset_has_moved()
            for carnivore in cell.carnivores:
                carnivore.reset_has_moved()

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population

        Parameters
        ----------
        self
        """
        # map_location is a dictionary with loc
        for map_location in population:
            loc = map_location['loc']
            pop = map_location['pop']
            self.map[loc].add_animals(pop)

    def feed(self):
        for cell in self.map.values():
            cell.feed_all()

    def procreate(self):
        for cell in self.map.values():
            cell.procreate()

    def age_animals(self):
        for cell in self.map.values():
            cell.age_pop()

    def lose_weight(self):
        for cell in self.map.values():
            cell.lose_weight()

    def die(self):
        for cell in self.map.values():
            cell.die()

    def simulate_one_year(self):
        self.ready_for_new_year()
        self.feed()
        self.procreate()
        self.migrate()
        self.age_animals()
        self.lose_weight()
        self.die()

if __name__ == '__main__':
    geogr = """\
            OOOOOOOOOOOOOOOOOOOOO
            OOOOOOOOSMMMMJJJJJJJO
            OSSSSSJJJJMMJJJJJJJOO
            OSSSSSSSSSMMJJJJJJOOO
            OSSSSSJJJJJJJJJJJJOOO
            OSSSSSJJJDDJJJSJJJOOO
            OSSJJJJJDDDJJJSSSSOOO
            OOSSSSJJJDDJJJSOOOOOO
            OSSSJJJJJDDJJJJJJJOOO
            OSSSSJJJJDDJJJJOOOOOO
            OOSSSSJJJJJJJJOOOOOOO
            OOOSSSSJJJJJJJOOOOOOO
            OOOOOOOOOOOOOOOOOOOOO
            """
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (2, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 40}
                for _ in range(200)
            ],
        }
    ]

    ini_carn = [
        {
            "loc": (4, 6),
            "pop": [
                {"species": "Carnivore", "age": 2, "weight": 40}
                for _ in range(4)
            ],
        }
    ]

    sim = Island(geogr, ini_herbs)
    for x in range(200):
        sim.simulate_one_year()
        if x == 50:
            sim.add_population(ini_carn)
        print(x)
        print(sim.num_animals)
        print(sim.num_animals_per_species)
        """
        for position in sim.island_map:
            try:
                print(sim.island_map[position].herbivores[-1], position)
                print(sim.island_map[position].carnivores[-1], position)
                print(position)
            except IndexError:
                pass"""