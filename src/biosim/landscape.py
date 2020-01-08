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

    def add_animal(self, species, animal):
        # Could be better if it takes more than one animal, one or more
        raise NotImplementedError

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

    @classmethod
    def set_parameters(cls, parameters):
        for key, value in parameters.items():
            if key in cls.__dict__.keys():
                setattr(cls, key, value)
            else:
                raise NameError('One the keys in your dict_attr is not an attribute.')


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
        self.map = self.make_map(multiple_line_string)

    def make_map(self, multiple_line_string):
        raise NotImplementedError


if __name__ == '__main__':
    cell = Cell()
    cell.set_parameters({'f_max': 100, 'alpha': 1})
