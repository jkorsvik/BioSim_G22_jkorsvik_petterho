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
            if animal['species'] == 'Carnivore':
                self.carnivores.append(ani.Carnivore(
                    age=animal['age'], weight=animal['weight']))

    def procreate(self):
        if self.num_herbivores > 1:
            for herbivore in self.herbivores:
                offspring = herbivore.birth(self.num_herbivores)
                if not offspring:
                    continue
                self.herbivores.append(offspring)

        if self.num_carnivores > 1:
            for carnivore in self.carnivores:
                offspring = carnivore.birth(self.num_carnivores)
                if not offspring:
                    continue
                self.carnivores.append(offspring)

    def lose_weight(self):
        for herbivore in self.herbivores:
            herbivore.lose_weight()
        for carnivore in self.carnivores:
            carnivore.lose_weight()

    @staticmethod
    def sort_by_fitness(animal_list):
        sorted_list = sorted(animal_list, key=lambda var: var.fitness)
        return sorted_list

    def feed_all(self):
        self.feed_herbivores()
        self.feed_carnivores()

    def feed_herbivores(self):
        self.herbivores = self.sort_by_fitness(self.herbivores)
        for herbivore in reversed(self.herbivores):
            self.fodder = herbivore.feed(self.fodder)

    def feed_carnivores(self):
        self.herbivores = self.sort_by_fitness(self.herbivores)
        self.carnivores = self.sort_by_fitness(self.carnivores)
        for carnivore in reversed(self.carnivores):
            self.herbivores = carnivore.feed(self.herbivores)

    def age_pop(self):
        for herbivore in self.herbivores:
            herbivore.age += 1
        for carnivore in self.carnivores:
            carnivore.age += 1

    def die(self):
        death_list = []
        for herbivore in self.herbivores:
            if herbivore.death():
                death_list.append(herbivore)

        for dead in death_list:
            self.herbivores.remove(dead)

        death_list = []
        for carnivore in self.carnivores:
            if carnivore.death():
                death_list.append(carnivore)

        for dead in death_list:
            self.carnivores.remove(dead)


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
