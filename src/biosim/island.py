# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from .landscape import *


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
    """
    Initiates the Island class: holds method for updating the map
    Class attribute map_params holds information of which letter relates
    to which class of landscape.py

    Parameters
    ----------
    island_map_string : multilinestring
        Multiple lines of string with characters representing cell type
    ini_pop : dict
        Key: location - Value: list of dict of species, age, and weight


    Attributes
    ----------
    map : dict
        calls method make_map, map creation from a multilinestring
    herbivore_tot_data : list
        Total number of herbivores indexed by year
    carnivore_tot_data : list
        Total number of carnivore indexed by year
    stats : dict
        multiple nested dicts, stores all data on dead/ born animals.
    """
    map_params = {'O': Ocean,
                  'M': Mountain,
                  'D': Desert,
                  'S': Savanna,
                  'J': Jungle}

    def __init__(self, island_map_string, ini_pop, store_stats=False):
        """
        Initializes instance of Island

        Parameters
        ----------
        island_map_string : str
            Multilinestring of map
        ini_pop : dict
            key : location - Value : list of dict
        store_stats : bool
        """
        self.len_map_x = None
        self.len_map_y = None

        self.map = self.make_map(island_map_string)
        self.add_population(ini_pop)
        self._year = 0

        self.herbivore_tot_data = []
        self.carnivore_tot_data = []
        self.update_data_list()

        self._store_stats = store_stats
        if store_stats:
            self.stats = {}
            self.create_and_update_stats_structure()

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

    def create_and_update_stats_structure(self):
        """Creates data structure for stats"""
        all_herbs = self.num_animals_per_species['Herbivore']
        all_carns = self.num_animals_per_species['Carnivore']

        for pos in self.map.keys():
            self.stats[self.year] = {'Herbivore': {'death': {pos: []},
                                                   'birth': {pos: []},
                                                   'alive': all_herbs},
                                     'Carnivore': {'death': {pos: []},
                                                   'birth': {pos: []},
                                                   'alive': all_carns}
                                     }

    def update_data_list(self):
        """Updates list for use in visualization"""
        animals_per_species = self.num_animals_per_species
        herbivores = animals_per_species['Herbivore']
        carnivores = animals_per_species['Carnivore']
        self.herbivore_tot_data.append(herbivores)
        self.carnivore_tot_data.append(carnivores)

    @staticmethod
    def clean_multi_line_string(island_map_string):
        """
        Strips and splits a multilinestring and checks for equal length
        of lines and specific letters at the edges: in this case 'O'.
        Raises ValueError if criteria are not met.

        Parameters
        ----------
        island_map_string : multilinestring
            Lines is row, letter is column
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
        island_map_string : str
            string of multiple lines

        Returns
        -------
        map : dict
            key : tuple, value : instance of subclass of BaseCell

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

        If the animal has nowhere to move, it returns None
        Parameters
        ----------
        pos : tuple
            Position of current cell
        animal : str
            Name of the animal

        Returns
        -------
        prob_list : list of tuples
            (Coordinate(y, x), and probabilities)
        """
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
                                    option.propensity[animal])
                                   )

        prop_sum = np.sum(sum(dict(propensity_list).values()))
        if prop_sum == 0:
            return None
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
                prob_herb = self.probability_calc(pos, 'Herbivore')
                prob_carn = self.probability_calc(pos, 'Carnivore')
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
        """Calls procreate in all cells of Island.map, adds born to stats"""
        for pos, cell in self.map.items():
            herb_birth, carn_birth = cell.procreate()
            if self._store_stats:
                self.stats[self.year]['Herbivore']['birth'][pos] = herb_birth
                self.stats[self.year]['Carnivore']['birth'][pos] = carn_birth

    def age_animals(self):
        """Calls age_pop in all cells of Island.map"""
        for cell in self.map.values():
            cell.age_pop()

    def lose_weight(self):
        """Calls lose_weight in all cells of Island.map"""
        for cell in self.map.values():
            cell.lose_weight()

    def die(self):
        """Calls die in all cells of Island.map, adds dead to stats"""
        for pos, cell in self.map.items():
            herb_death, carn_death = cell.die()
            if self._store_stats:
                self.stats[self.year]['Herbivore']['death'][pos] = herb_death
                self.stats[self.year]['Carnivore']['death'][pos] = carn_death

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @year.setter
    def year(self, new_value):
        """Sets year to new value"""
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
        self.update_data_list()
        if self._store_stats:
            self.create_and_update_stats_structure()


if __name__ == '__main__':
    pass
