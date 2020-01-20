# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

# from typing import Iterable
from src.biosim.landscape import *
import textwrap


def check_length(lines):
    """
    Compares length of all lines in a list of lines to the first

    Parameters
    ----------
    lines : list
        lines

    Returns
    -------
    bool
        False if not equal length, True if length is equal

    """
    if not all(len(lines[0]) == len(line) for line in lines[1:]):
        return False
    return True


class Island:
    map_params = {'O': Ocean,
                  'M': Mountain,
                  'D': Desert,
                  'S': Savanna,
                  'J': Jungle}

    def __init__(self, island_map_string, ini_pop):
        """
        Initiates the Island class: holds method for updating the map
        Class attribute map_params holds information of which letter relates
        to which class of landscape.py

        Parameters
        ----------
        island_map_string
        ini_pop

        Attributes
        --------
        self.map : dict
            calls method make_map, map creation from a multilinestring
        """
        self.len_map_x = None
        self.len_map_y = None

        self.map = self.make_map(island_map_string)
        self.add_population(ini_pop)
        self._year = 0

    @property
    def num_animals(self):
        """
        Total number of animals on island.

        Returns
        -------
        num_animals : int
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
        num_animals_per_species : dictionary
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
    def clean_multi_line_string(island_map_string): # Change name to clean and check
        """
        Strips and splits a multilinestring and checks for equal length
        of lines and specific letters at the edges: in this case 'O'.
        Raises ValueError if criteria are not met.

        Parameters
        ----------
        island_map_string : multilinestring

        Returns
        -------
        lines : list
            Lines of strings (cleaned)
        """
        island_map_string = island_map_string.strip()
        lines = island_map_string.split('\n')

        if not check_length(lines):
            raise ValueError('Each line of the multi line string, '
                             'shall be equal in length')

        for index in range(len(lines[0])):
            if lines[0][index] is not 'O' or lines[-1][index] is not 'O':
                raise ValueError('This is not an island. Islands are '
                                 'surrounded by water')
        for index in range(len(lines)):
            if lines[index][0] is not 'O' or lines[index][-1] is not 'O':
                raise ValueError('This is not an island. Islands are '
                                 'surrounded by water')

        return lines

    def make_map(self, island_map_string):
        """
        Creates a dictionary data frame that stores instances of cells
        by key: a tuple of (y, x)-coordinates

        Also saves the length and with of the island

        Parameters
        ----------
        island_map_string : multilinestring

        Returns
        -------
        map : dictionary
            key : tuple
                value : instance of subclass of BaseCell

        """
        island_map = {}
        lines = self.clean_multi_line_string(island_map_string)

        # Possible to fix using type hinting (alt+enter)
        self.len_map_x = len(lines[0])
        self.len_map_y = len(lines)

        for y_cord, line in enumerate(lines):
            for x_cord, letter in enumerate(line):
                if letter in self.map_params.keys():
                    island_map[(y_cord, x_cord)] = self.map_params[letter]()
                else:
                    raise ValueError(f'String must consist of uppercase'
                                     f'letters like these:\n'
                                     f'{self.map_params}')

        return island_map

    def probability_calc(self, pos, animal):
        """
        Finds the preposition for all neighbouring cells
        within dx +- 1 and dy +-1. This means we have the positions
        North, West, South and East of the current position.

        Then calculates the probability for the type of animal.
        Parameters
        ----------
        pos : tuple
            Position of current cell
        animal : object
            Class or subclass of BaseAnimal

        Returns
        -------
        prob_list : list of tuples
            (Coordinate(y, x), and probabilities)
        """
        species = animal.__name__
        y_cord, x_cord = pos
        loc_1 = (y_cord - 1, x_cord)
        loc_2 = (y_cord + 1, x_cord)
        loc_3 = (y_cord, x_cord - 1)
        loc_4 = (y_cord, x_cord + 1)
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
        """ Add herbivore to cell in new location """
        self.map[new_loc].add_migrated_herb(herbivore)

    def add_carn_to_new_cell(self, new_loc, carnivore):
        """ Add herbivore to cell in new location """
        self.map[new_loc].add_migrated_carn(carnivore)

    def migrate(self):
        """
        Goes through the map attribute of Island and calculates
        probabilities for herbivores and carnivores, with position and
        name of class.

        calls migrate method in instance of subclass of BaseCell
        Methods
        -------
        BaseCell.migrate()
        probability_calc(pos, animal)


        Notes
        ------
         Adds herbivores and carnivores that has migrated to new cells
        """
        for pos, cell in self.map.items():
            if cell.passable and cell.num_animals > 0:
                prob_herb = self.probability_calc(pos, Herbivore)
                prob_carn = self.probability_calc(pos, Carnivore)
                moved_herb, moved_carn = cell.migrate(prob_herb, prob_carn)
                for loc, herb in moved_herb:
                    self.add_herb_to_new_cell(loc, herb)
                for loc, carn in moved_carn:
                    self.add_carn_to_new_cell(loc, carn)

    def ready_for_new_year(self):
        """
        Resets each cell in Island.map
        Methods
        -------
        BaseCell.grow
        BaseCell.reset_calculate_propensity
        BaseAnimal.reset_has_moved
        """
        for cell in self.map.values():
            cell.grow()
            cell.reset_calculate_propensity()
            for herbivore in cell.herbivores:
                herbivore.reset_has_moved()
            for carnivore in cell.carnivores:
                carnivore.reset_has_moved()

    def add_population(self, population):
        """
        Feeds a dictionary of population to cell by position.

        Parameters
        ----------
        population: list
            loc: tuple
            pop: dict

        Methods
        -------
        BaseCell.add_animals()

        """
        # map_location is a dictionary with loc
        for map_location in population:
            loc = map_location['loc']
            if loc not in self.map.keys():
                raise ValueError('Provided location does not exist')
            if not self.map[loc].passable:
                raise ValueError('Provided location is not passable')

            pop = map_location['pop']
            self.map[loc].add_animals(pop)

    def feed(self):
        """Calls feed_all in all cells of Island.map"""
        for cell in self.map.values():
            cell.feed_all()

    def procreate(self):
        """Calls procreate in all cells of Island.map"""
        for cell in self.map.values():
            cell.procreate()

    def age_animals(self):
        """Calls age_pop in all cells of Island.map"""
        for cell in self.map.values():
            cell.age_pop()

    def lose_weight(self):
        """Calls lose_weight in all cells of Island.map"""
        for cell in self.map.values():
            cell.lose_weight()

    def die(self):
        """Calls die in all cells of Island.map"""
        for cell in self.map.values():
            cell.die()

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @year.setter
    def year(self, new_value):
        self._year = new_value

    def simulate_one_year(self):
        """
        Simulates a whole year by the following sequence
        Returns
        -------

        """
        self.ready_for_new_year()
        self.feed()
        self.procreate()
        self.migrate()
        self.age_animals()
        self.lose_weight()
        self.die()
        self.year += 1


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