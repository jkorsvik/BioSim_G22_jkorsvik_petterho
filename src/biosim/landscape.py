# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"
import src.biosim.animals as ani
import textwrap
from pprint import pprint


class Cell:
    def __init__(self):
        self.herbivores = []
        self.carnivores = []
        self.fodder = 0

    def add_animals(self, animal_list):
        # Takes list of dicts with are the animal
        for animal in animal_list:
            if animal['species'] == 'Herbivore':
                self.herbivores.append(ani.Herbivore(
                    age=animal['age'], weight=animal['weight']))
            if animal['species'] == 'Herbivore':
                self.carnivores.append(ani.Carnivore(
                    age=animal['age'], weight=animal['weight']))

    # Maybe to be used
    def update_and_sort_animals_by_fitness(self):
        raise NotImplementedError

    def feed_herbivores(self):
        for herbivore in self.herbivores:
            self.fodder = herbivore.feed(self.fodder)

    def feed_carnivores(self):
        raise NotImplementedError

    @property
    def num_carnivores(self):
        return len(self.carnivores)

    @property
    def num_herbivores(self):
        return len(self.herbivores)

    @property
    def meat_for_carnivores(self):
        meat = 0
        for herbivore in self.herbivores:
            meat += herbivore.weight
        return meat

    @property
    def num_animals(self):
        return self.num_carnivores + self.num_herbivores

    @classmethod
    def set_parameters(cls, parameters):
        for key, value in parameters.items():
            if key in cls.__dict__.keys():
                setattr(cls, key, value)
            else:
                raise NameError('One the keys in your parameters is not an '
                                'attribute.')


class Ocean(Cell):
    def __init__(self):
        super().__init__()


class Mountain(Cell):
    def __init__(self):
        super().__init__()


class Desert(Cell):
    def __init__(self):
        super().__init__()


class Savanna(Cell):
    f_max = 300.0
    alpha = 0.3

    def __init__(self):
        super().__init__()
        self.fodder = self.f_max

    def grow(self):
        self.fodder += self.alpha*(self.f_max - self.fodder)


class Jungle(Cell):
    f_max = 800.0

    def __init__(self):
        super().__init__()
        self.fodder = self.f_max

    def grow(self):
        self.fodder = self.f_max


class Map:
    map_params = {'O': Ocean, 'M': Mountain, 'D': Desert, 'S': Savanna,
                  'J': Jungle}

    def __init__(self, multiple_line_string):
        lines = self.clean_multi_line_string(multiple_line_string)
        print(lines)
        self.map = self.make_map(lines)

    @staticmethod
    def clean_multi_line_string(multi_line_string):
        lines = multi_line_string.split('\n')
        return lines

    def make_map(self, multiple_line_string):
        island_map = {}

        for y, line in enumerate(multiple_line_string):
            for x, letter in enumerate(line):
                island_map[(y, x)] = self.map_params[letter.upper()]()
        return island_map


if __name__ == '__main__':
    savanna = Savanna()
    savanna.set_parameters({'f_max': 100, 'alpha': 1})

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
               OOOOOOOOOOOOOOOOOOOOO"""

    geogr = textwrap.dedent(geogr)

    island = Map(geogr)
    pprint(island.map)
