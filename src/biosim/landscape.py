# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


class Cell:
    def __init__(self):
        self.herbivores = []
        self.carnivores = []
        self.fodder = 0

    def add_animal(self, species, animal):
        # Could be better if it takes more than one animal, one or more
        raise NotImplementedError

    # Maybe to be used
    def update_and_sort_animals_by_fitness(self):
        raise NotImplementedError

    def feed_herbivores(self):
        for herbivore in self.herbivores:
            self.fodder = herbivore.feed(self.fodder)

    @property
    def num_carnivores(self):
        return len(self.carnivores)

    @property
    def num_herbivores(self):
        return len(self.herbivores)

    @property
    def meat_for_carnivores(self):
        return sum(self.herbivores)

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
        self.map = self.make_map(multiple_line_string)

    def make_map(self, multiple_line_string):
        raise NotImplementedError


if __name__ == '__main__':
    savanna = Savanna()
    savanna.set_parameters({'f_max': 100, 'alpha': 1})
