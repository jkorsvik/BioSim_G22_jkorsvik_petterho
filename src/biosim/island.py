# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from src.biosim.landscape import *
import textwrap


def check_length(lines):
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

        for index in range(len(lines[0])):
            if lines[0][index] is not 'O' or lines[-1][index] is not 'O':
                raise ValueError('')
        for index in range(len(lines)):
            if lines[index][0] is not 'O' or lines[index][-1] is not 'O':
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
        island_map = {}
        lines = self.clean_multi_line_string(island_map_string)
        for y_cord, line in enumerate(lines):
            for x_cord, letter in enumerate(line):
                if letter in self.map_params.keys():
                    island_map[(y_cord, x_cord)] = self.map_params[letter]()
                else:
                    raise ValueError(f'String must consist of uppercase'
                                     f'letters like these:\n'
                                     f'{self.map_params}')

        return island_map

    def propensity_of_neighbour_cells(self, pos):
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
            propensity_list.append((loc, option.propensity))
        return propensity_list

    def add_animal_to_new_cell(self, new_loc, animal):
        self.map[new_loc].add_migrated_animal(animal)

    def migrate(self):
        migration_by_cells = []

        for pos, cell in self.map.items():
            if cell.passable and cell.num_animals > 0:

                propensity_list = self.propensity_of_neighbour_cells(pos)
                migration_by_cells.append((cell.migrate(propensity_list)))

        for list_cell in migration_by_cells:
            for pos, animal in list_cell:
                self.add_animal_to_new_cell(pos, animal)


    def ready_for_new_year(self):
        for cell in self.map.values():
            cell.grow()
            cell.reset_calculate_propensity()
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