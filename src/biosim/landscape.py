# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

from src.biosim.animals import Herbivore, Carnivore
import numpy as np
import itertools


def choose_new_location(prob_list):
    """
    Draws one out of a list with weights.

    Parameters
    ----------
    prob_list : list
        tuple(loc, probabilities)

    Returns
    -------
    locations[index] : tuple
        new_location - (y, x)
    """
    probabilities = [x[1] for x in prob_list]
    cumulative_sum = np.cumsum(probabilities)
    locations = [x[0] for x in prob_list]
    index = 0
    random_number = np.random.random()
    while random_number > cumulative_sum[index]:
        index += 1
    return locations[index]


class BaseCell:
    passable = True
    f_max = 0
    alpha = 0

    @classmethod
    def set_parameters(cls, passable=None, f_max=None, alpha=None):
        """
        Method for changing one or all parameters with a dictionary for class
        of BaseCell class
        By checking all parameters first, set parameters does not change
        any parameters before it is sure that all parameters are valid

        Parameters
        ----------
        passable - float
        f_max - float
        alpha - float

        Returns
        -------

        """

        bool_passable = False
        bool_f_max = False
        bool_alpha = False

        if passable:
            if type(passable) is bool:
                bool_passable = True
            else:
                raise ValueError('passable takes bool arguments only')
        if f_max:
            if f_max >= 0:
                bool_f_max = True
            else:
                raise ValueError('f_max takes int or float arguments only')
        if alpha:
            if alpha >= 0:
                bool_alpha = True
            else:
                raise ValueError('alpha takes int or float arguments only')

        if bool_passable is True:
            cls.passable = passable
        if bool_f_max is True:
            cls.f_max = f_max
        if bool_alpha is True:
            cls.alpha = alpha

    def __init__(self):
        """
        Initialize Cell

        Attributes
        ------
        self.herbivores : list
        self.carnivores : list
        self._calculate_propensity : bool
        self._propensity : None(filler)
        self.fodder : float
        """
        self.herbivores = []
        self.carnivores = []
        self._calculate_propensity = True
        self._propensity = None
        self.fodder = 0

    def grow(self):
        """IS OVERWRITTEN BY SUBCLASSES"""
        pass

    def add_animals(self, animal_list):
        """
        Adds a new population from a list of dictionaries to the Cell
        In the dictionaries the species, age and weight of each animal
        resides.

        Parameters
        ----------
        animal_list: list
            dict

        Returns
        -------

        """
        # Takes list of dicts with are the animal
        for animal in animal_list:
            if animal['species'] == 'Herbivore':
                self.herbivores.append(Herbivore(
                    age=animal['age'], weight=animal['weight']))
            if animal['species'] == 'Carnivore':
                self.carnivores.append(Carnivore(
                    age=animal['age'], weight=animal['weight']))

    def add_migrated_herb(self, herbivore):
        """Add herbivore to list of herbivores"""
        self.herbivores.append(herbivore)

    def add_migrated_carn(self, carnivore):
        """Add carnivore to list of carnivores"""
        self.carnivores.append(carnivore)

    def remove_migrated_herb(self, herbivore):
        """Remove herbivore from list of herbivores"""
        self.herbivores.remove(herbivore)

    def remove_migrated_carn(self, carnivore):
        """Remove carnivore from list of carnivores"""
        self.carnivores.remove(carnivore)

    def chain_lists(self):
        """Chains list of cell.herbivores with cell.carnivores lists"""
        return itertools.chain(self.herbivores, self.carnivores)

    def migrate(self, prob_herb, prob_carn):
        """
        Goes through herbivores, migrates, appends to moved_herb.
        Goes through carnivores, migrates, appends to moved_carn.
        Deletes the animal that has moved from the list of class.


        Parameters
        ----------
        prob_herb: list of tuples
            Location (y, x) and Probability

        prob_carn: list of tuples
            Location (y, x) and Probability

        Returns
        -------
        moved_herb: list of tuples
            New position (y, x) and animal instance

        moved_carn: list of tuples
            New position (y, x) and animal instance

        """
        moved_herb = []
        moved_carn = []
        for herb in self.herbivores:
            if herb.will_migrate():
                loc = choose_new_location(prob_herb)
                moved_herb.append((loc, herb))
        for carn in self.carnivores:
            if carn.will_migrate():
                loc = choose_new_location(prob_carn)
                moved_carn.append((loc, carn))

        for loc, herb in moved_herb:
            self.remove_migrated_herb(herb)
        for loc, carn in moved_carn:
            self.remove_migrated_carn(carn)

        return moved_herb, moved_carn

    def procreate(self):
        """
        Goes through herbivores and carnivores if there is more than one
        animal the same list.

        Calls birth method, and if offspring returned appends the offspring
        to the cells appropriate list.

        Methods
        -------
        BaseAnimal.birth(num_of_same_species)


        Returns
        -------

        """
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
        """Makes animals in cell lose_weight"""
        for herbivore in self.herbivores:
            herbivore.lose_weight()
        for carnivore in self.carnivores:
            carnivore.lose_weight()

    @staticmethod
    def sort_by_fitness(animal_list):
        """Sort list of animals by fitness"""
        sorted_list = sorted(animal_list, key=lambda var: var.fitness)
        return sorted_list

    def feed_all(self):
        """Makes all animals eat"""
        self.feed_herbivores()
        self.feed_carnivores()

    def feed_herbivores(self):
        """
        Herbivores is sorted by fitness thereafter goes through the updated
        list in reverse. This makes the most fit animals first to feed.

        Updated the cells amount of food(fooder) after each animal has fed.

        Methods
        -------
        BaseAnimal.feed()

        """
        self.herbivores = self.sort_by_fitness(self.herbivores)
        for herbivore in reversed(self.herbivores):
            self.fodder = herbivore.feed(self.fodder)

    def feed_carnivores(self):
        """
        Sorts herbivores by fitness
        Sorts carnivores by fitness

        The fittest carnivore feeds first with sorted list of herbivores
        as input.

        Sets the returned list as the new list for herbivores.

        Methods
        ------
        Carnivore.feed(least_fit_herbivores)
            Returns list
                Animals that are still living

        Returns
        -------

        """
        self.herbivores = self.sort_by_fitness(self.herbivores)
        self.carnivores = self.sort_by_fitness(self.carnivores)
        for carnivore in reversed(self.carnivores):
            self.herbivores = carnivore.feed(self.herbivores)

    def age_pop(self):
        """Adds a increment of 1 to the animals age attribute"""
        #### Spør om dette
        for herbivore in self.herbivores:
            herbivore.age += 1
        for carnivore in self.carnivores:
            carnivore.age += 1

    def die(self):
        """
        Iterates through animals, adds them to a death list.

        Iterates through death list and removes them from the cell's
        appropriate list by object instance.

        Methods
        -------
        BaseAnimal.death()
            Returns bool

        Returns
        -------

        """

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
        """
        Property of each cell, calculates each year once because of
        self._calculate_propensity

        if cell is not passable propensities will be zero

        Propensity is calculated by:
        .. math::
            \epsilon_k = \frac{f_k}{(n_k + 1)F'}

            \pi_k = e^{\gamma\epsilon_j}

            \pi_j = \frac{\pi_j}{\sum\epsilon_C(i)}



        sets self.calculate_propensity to False when propensity is calculated

        Returns
        -------
        self._propensity: dict
            key: str containing class.__name__
            value: propensity

        """
        if not self._calculate_propensity:
            return self._propensity

        if not self.passable:
            self._propensity = {'Carnivore': 0,
                                'Herbivore': 0}
        else:

            lambda_ = Herbivore.lambda_
            appetite = Herbivore.F
            dividend = ((self.num_herbivores + 1) * appetite)
            exponent_herb = (lambda_ * (self.fodder
                                        / dividend))

            propensity_herb = np.exp(exponent_herb)

            lambda_ = Carnivore.lambda_
            appetite_ = Carnivore.F

            dividend = ((self.num_carnivores + 1) * appetite_)
            exponent_carn = (lambda_ * (self.meat_for_carnivores
                                        / dividend))

            propensity_carn = np.exp(exponent_carn)

            self._propensity = {'Carnivore': propensity_carn,
                                'Herbivore': propensity_herb}

            self._calculate_propensity = False

        return self._propensity

    def reset_calculate_propensity(self):
        """Sets _calculate_propensity to True"""
        self._calculate_propensity = True

    @property
    def num_carnivores(self):
        """Property: number of carnivores derived from len of list"""
        return len(self.carnivores)

    @property
    def num_herbivores(self):
        """Property: number of herbivores derived from len of list"""
        return len(self.herbivores)

    @property
    def meat_for_carnivores(self):
        """Property: Sum the weight of all herbivores in cell"""
        meat = 0
        for herbivore in self.herbivores:
            meat += herbivore.weight
        return meat

    @property
    def num_animals(self):
        """Property: sum of all num_carnivores and num_herbivores"""
        return self.num_carnivores + self.num_herbivores


class Ocean(BaseCell):
    """Subclass of cell"""
    passable = False

    def __init__(self):
        super().__init__()


class Mountain(BaseCell):
    """Subclass of cell"""
    passable = False

    def __init__(self):
        super().__init__()


class Desert(BaseCell):
    """
    Subclass of cell, is passable but contains no food
    """
    passable = True
    f_max = 0

    def __init__(self):
        super().__init__()


class Savanna(BaseCell):
    """
    Subclass of cell

    Attributes
    ------
    self.f_max:  max amount of fodder(food) in the cell
    self.alpha: value used for grow method

    Methods
    ------
    grow: updates amount of fodder in cell
    """
    passable = True
    f_max = 300.0
    alpha = 0.3

    def __init__(self):
        super().__init__()
        self.fodder = self.f_max

    def grow(self):
        self.fodder += self.alpha * (self.f_max - self.fodder)


class Jungle(BaseCell):
    """
    Subclass of cell

    Attributes
    ------
    self.f_max: max amount of fodder(food) in the cell

    Methods
    ------
    grow: updates amount of fodder in cell
    """
    passable = True
    f_max = 800.0

    def __init__(self):
        super().__init__()
        self.fodder = self.f_max

    def grow(self):
        self.fodder = self.f_max


if __name__ == '__main__':
    pass
