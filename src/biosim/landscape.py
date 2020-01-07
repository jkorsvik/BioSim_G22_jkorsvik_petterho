# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


class Cell:
    f_max = 0
    alpha = 0

    def __init__(self):
        self.herbivores = []
        self.carnivores = []
        self.fodder = 0

    def eat(self):
        raise NotImplementedError

    @property
    def num_carnivore(self):
        return len(self.carnivores)

    @property
    def num_herbivore(self):
        return len(self.herbivores)

    @property
    def meat_for_carnivores(self):
        return sum(self.herbivores)

    @property
    def num_animals(self):
        return self.num_carnivore + self.num_herbivore


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

    @classmethod
    def change_parameters(cls, parameters):
        pass


class Jungle(Cell):
    f_max = 800.0

    def __init__(self):
        super().__init__()
        self.fodder = self.f_max

    def grow(self):
        self.fodder = self.f_max

    @classmethod
    def change_parameters(cls, parameters):
        pass


class Map:
    map_params = {'O': Ocean, 'M': Mountain, 'D': Desert, 'S': Savanna,
                  'J': Jungle}

    def __init__(self, multiple_line_string):
        self.map = self.make_map(multiple_line_string)

    def make_map(self, multiple_line_string):
        raise NotImplementedError


if __name__ == '__main__':
    pass