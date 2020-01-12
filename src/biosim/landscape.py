# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from src.biosim.animals import Herbivore, Carnivore
import numpy as np



class Cell:
    passable = True
    f_max = 0
    alpha = 0


    @classmethod
    def set_parameters(cls, parameters):
        for key, value in parameters.items():
            if key in cls.__dict__.keys():
                if value < 0:
                    raise ValueError('Parameters must be positive.')
                else:
                    setattr(cls, key, value)

            else:
                raise NameError('One the keys in your parameters is not an '
                                'attribute.')

    def __init__(self):
        self.herbivores = []
        self.carnivores = []
        self._calculate_propensity = True
        self._propensity = None
        self.fodder = 0

    def grow(self):
        pass

    def add_animals(self, animal_list):
        # Takes list of dicts with are the animal
        for animal in animal_list:
            if animal['species'] == 'Herbivore':
                self.herbivores.append(Herbivore(
                    age=animal['age'], weight=animal['weight']))
            if animal['species'] == 'Carnivore':
                self.carnivores.append(Carnivore(
                    age=animal['age'], weight=animal['weight']))

    def add_migrated_herb(self, herbivore):
        self.herbivores.append(herbivore)

    def add_migrated_carn(self, carnivore):
        self.carnivores.append(carnivore)

    def remove_migrated_herb(self, herbivore):
        self.herbivores.remove(herbivore)

    def remove_migrated_carn(self, carnivore):
        self.carnivores.remove(carnivore)

    def procreate(self):
        number_of_adult_herbivores = self.num_herbivores
        if number_of_adult_herbivores > 1:
            for herbivore in self.herbivores:
                offspring = herbivore.birth(number_of_adult_herbivores)
                if not offspring:
                    continue
                self.herbivores.append(offspring)

        number_of_adult_carnivores = self.num_carnivores
        if number_of_adult_carnivores > 1:
            for carnivore in self.carnivores:
                offspring = carnivore.birth(number_of_adult_carnivores)
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
    def propensity(self):
        if not self._calculate_propensity:
            return self._propensity

        if not self.passable:
            self._propensity = {'Carnivore': 0,
                                'Herbivore': 0}
        else:

            gamma = Herbivore.gamma
            appetite = Herbivore.gamma
            propensity_herb = np.exp((gamma*(self.fodder
                                             / (self.num_herbivores + 1)
                                             * appetite)), dtype=np.float64)
            gamma_1 = Carnivore.gamma
            appetite_1 = Carnivore.F
            meat = 0
            for herbivore in self.herbivores:
                meat += herbivore.weight
            propensity_carn = np.exp(gamma_1*(meat
                                              / (self.num_carnivores + 1)
                                              * appetite_1), dtype=np.float64)
            self._propensity = {'Carnivore': propensity_carn,
                                'Herbivore': propensity_herb}

        self._calculate_propensity = False

        return self._propensity

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


class Ocean(Cell):
    passable = False

    def __init__(self):
        super().__init__()


class Mountain(Cell):
    passable = False

    def __init__(self):
        super().__init__()


class Desert(Cell):
    passable = True

    def __init__(self):
        super().__init__()


class Savanna(Cell):
    passable = True
    f_max = 300.0
    alpha = 0.3

    def __init__(self):
        super().__init__()
        self.fodder = self.f_max

    def grow(self):
        self.fodder += self.alpha*(self.f_max - self.fodder)


class Jungle(Cell):
    passable = True
    f_max = 800.0

    def __init__(self):
        super().__init__()
        self.fodder = self.f_max

    def grow(self):
        self.fodder = self.f_max


if __name__ == '__main__':
    pass
