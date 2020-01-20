# -*- coding: utf-8 -*-

"""
"""

import numpy as np
import math
from numba import jit
import random

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


@jit
def fitness_calculation(
        phi_age, age, a_half,
        phi_weight, weight, w_half
                        ):
    """
    Calculates fitness by sigmoid multiplication

    Parameters
    ----------
    phi_age : float
    age : int
    a_half : float
    phi_weight : float
    weight : float
    w_half  : float

    Returns
    -------
    float
        Value between 0 and 1 representing fitness

    """
    pos_q_age = phi_age * (age - a_half)
    neg_q_weight = - (phi_weight * (weight - w_half))

    return 1/(1 + math.exp(pos_q_age)) * 1/(1 + math.exp(neg_q_weight))


class BaseAnimal:
    """
    Baseclass for all animals

    Methods
    -------
    set_parameters: class method
    __init__
    __repr__
    age_one_year
    reset_has_moved
    will_migrate
    birth
    death
    feed
    lose_weight
    """
    w_birth = 8.0
    sigma_birth = 1.5
    beta = 0.9
    eta = 0.05
    a_half = 40
    phi_age = 0.2
    w_half = 10
    phi_weight = 0.1
    mu = 0.25
    lambda_ = 1.0
    gamma = 0.2
    zeta = 3.5
    xi = 1.2
    omega = 0.4
    F = 10.0

    @classmethod
    def set_parameters(cls, w_birth=None, sigma_birth=None, beta=None,
                       eta=None, a_half=None, phi_age=None, w_half=None,
                       phi_weight=None, mu=None, lambda_=None, gamma=None,
                       zeta=None, xi=None, omega=None, F=None,
                       DeltaPhiMax=None):
        """
        Method for changing one or all parameters with a dictionary for
        subclass of BaseAnimal class
        Does not change any parameters before it is sure that all
        parameters are valid.

        Parameters
        ----------
        w_birth : float
            Average birth weight
        sigma_birth : float
            STD of birth weight
        beta : float
            Fodder to weight conversion
        eta : float
            Weight loss scalar
        a_half : float
            Half age of Animals
        phi_age : float
            Scalar of age for fitness
        w_half : float
            Half weight of Animals
        phi_weight : float
            Scalar of weight for fitness
        mu : float
            Scalar for moving is multiplied with fitness
        lambda_ : float
            Scalar for propensity calculation
        gamma : float
            Scalar for birth
        zeta : float
             Scalar if birth will happen
        xi : float
            Scalar for weight loss after birth
        omega : float
            Scalar for death
        F : float
            Appetite of Animal
        DeltaPhiMax : float
            Parameter used by Carnivore when calculating if they can kill
            an Animal

        Returns
        -------

        """
        # By checking all parameters first, set parameters does not change
        # any parameters before it is sure that all parameters are valid

        # If I can, I should make this smaler.

        bool_w_birth = False
        bool_sigma_birth = False
        bool_beta = False
        bool_eta = False
        bool_a_half = False
        bool_phi_age = False
        bool_w_half = False
        bool_phi_weight = False
        bool_mu = False
        bool_lambda_ = False
        bool_gamma = False
        bool_zeta = False
        bool_xi = False
        bool_omega = False
        bool_F = False
        bool_DeltaPhiMax = False

        if w_birth:
            if w_birth >= 0:
                bool_w_birth = True
            else:
                raise ValueError('w_birth takes positive int or float '
                                 'arguments only')
        if sigma_birth:
            if sigma_birth >= 0:
                bool_sigma_birth = True
            else:
                raise ValueError('sigma_birth takes positive int or float '
                                 'arguments only')
        if beta:
            if beta >= 0:
                bool_beta = True
            else:
                raise ValueError('beta takes positive int or float '
                                 'arguments only')
        if eta:
            if 1 >= eta >= 0:
                bool_eta = True
            else:
                raise ValueError('eta takes int or float '
                                 'arguments 0 <= eta <= 1 only')
        if a_half:
            if a_half >= 0:
                bool_a_half = True
            else:
                raise ValueError('a_half takes positive int or float '
                                 'arguments only')
        if phi_age:
            if phi_age >= 0:
                bool_phi_age = True
            else:
                raise ValueError('phi_age takes positive int or float '
                                 'arguments only')
        if w_half:
            if w_half >= 0:
                bool_w_half = True
            else:
                raise ValueError('w_half takes positive int or float '
                                 'arguments only')
        if phi_weight:
            if phi_weight >= 0:
                bool_phi_weight = True
            else:
                raise ValueError('phi_weight takes positive int or float '
                                 'arguments only')
        if mu:
            if mu >= 0:
                bool_mu = True
            else:
                raise ValueError('mu takes positive int or float '
                                 'arguments only')
        if lambda_:
            if lambda_ >= 0:
                bool_lambda_ = True
            else:
                raise ValueError('lambda_ takes positive int or float '
                                 'arguments only')
        if gamma:
            if gamma >= 0:
                bool_gamma = True
            else:
                raise ValueError('gamma takes positive int or float '
                                 'arguments only')
        if zeta:
            if zeta >= 0:
                bool_zeta = True
            else:
                raise ValueError('zeta takes positive int or float '
                                 'arguments only')
        if xi:
            if xi >= 0:
                bool_xi = True
            else:
                raise ValueError('xi takes positive int or float '
                                 'arguments only')
        if omega:
            if omega >= 0:
                bool_omega = True
            else:
                raise ValueError('omega takes positive int or float '
                                 'arguments only')
        if F:
            if F >= 0:
                bool_F = True
            else:
                raise ValueError('F takes positive int or float '
                                 'arguments only')
        if DeltaPhiMax:
            if DeltaPhiMax > 0:
                bool_DeltaPhiMax = True
            else:
                raise ValueError('DeltaPhiMax takes  strictly positive int or '
                                 'float arguments only')

        if bool_w_birth is True:
            cls.w_birth = w_birth
        if bool_sigma_birth is True:
            cls.sigma_birth = sigma_birth
        if bool_beta is True:
            cls.beta = beta
        if bool_eta is True:
            cls.eta = eta
        if bool_a_half is True:
            cls.a_half = a_half
        if bool_phi_age is True:
            cls.phi_age = phi_age
        if bool_w_half is True:
            cls.w_half = w_half
        if bool_phi_weight is True:
            cls.phi_weight = phi_weight
        if bool_mu is True:
            cls.mu = mu
        if bool_lambda_ is True:
            cls.lambda_ = lambda_
        if bool_gamma is True:
            cls.gamma = gamma
        if bool_zeta is True:
            cls.zeta = zeta
        if bool_xi is True:
            cls.xi = xi
        if bool_omega is True:
            cls.omega = omega
        if bool_F is True:
            cls.F = F
        if bool_DeltaPhiMax is True:
            cls.DeltaPhiMax = DeltaPhiMax

    def __init__(self, age=0, weight=None):
        """
        Initialises instance, calculates weight with a gaussian
        distribution if weight is not specified.

        Parameters
        ----------
        age : int
        weight : float

        Attributes
        --------
        self._age : int
        self._weight : float
        self._compute_fitness : bool
        self._fitness : float
            Between 0 and 1
        self._has_moved : bool
        """
        self._age = age
        self._weight = weight
        self._compute_fitness = True
        self._fitness = None
        self._has_moved = False
        if weight is None:
            normal = random.gauss(self.w_birth, self.sigma_birth)
            self.weight = normal
            if normal < 0:
                self.weight = 0  # newborns with <= 0 will die end of year

    def __repr__(self):
        """How the instance presents itself if called"""
        string = f"Animal Type: {type(self).__name__}\n" \
                 f"Age: {self.age}\n" \
                 f"Weight: {self.weight}\n" \
                 f"Fitness: {self.fitness}\n"
        return string

    @property
    def fitness(self):
        """
        Calculates fitness if weight or age is changed, else return old value

        Returns
        -------
        self._fitness : float


        """
        if self._compute_fitness is True:
            if self.weight <= 0:
                return 0

            self._compute_fitness = False
            self._fitness = fitness_calculation(
                self.phi_age, self.age, self.a_half,
                self.phi_weight, self.weight, self.w_half)

            return self._fitness

        return self._fitness

    def age_one_year(self):
        """Adds an increment of 1 to age"""
        self.age += 1

    @property
    def age(self):
        """Getter for age"""
        return self._age

    @age.setter
    def age(self, new_age):
        """Sets age to new value and compute fitness to true"""
        self._compute_fitness = True
        self._age = new_age

    @property
    def weight(self):
        """Getter for weight"""
        return self._weight

    @weight.setter
    def weight(self, new_weight):
        """Sets weight to new value and compute fitness to true"""
        self._compute_fitness = True
        self._weight = new_weight

    @property
    def has_moved(self):
        """
        Gives back bool value and sets the moved statement to True

        Returns
        -------
        moved : bool

        """
        moved = self._has_moved
        self._has_moved = True
        return moved

    def reset_has_moved(self):
        """Set has moved to False"""
        self._has_moved = False

    def will_migrate(self):
        """
        Animals that has not moved yet will calculate if they will move

        Returns
        -------
        bool
            True if the animal wil move
        """
        if not self.has_moved:
            prob_to_move = self.fitness * self.mu
            return bool(random.random() < prob_to_move)
        return False

    def birth(self, num_same_species):
        """
        Whether or not an animal will give birth, weight loss updated, returns
        offspring

        Parameters
        ----------
        num_same_species : int
            Number of same animals of age >= 1 in the same cell

        Returns
        -------
        offspring : object
            Instance of a new animal of same type as "mother"
            with default age 0 and default weight None.

        """
        mates = num_same_species - 1
        prob_to_birth = np.minimum(1, (self.gamma * self.fitness * mates))
        if self.weight < self.zeta*(self.w_birth + self.phi_weight):
            return 0

        if random.random() < prob_to_birth:
            offspring = type(self)()
            weight_loss = self.xi * offspring.weight

            if self.weight >= weight_loss:
                self.weight -= weight_loss
                return offspring

        return 0

    def death(self):
        """
        Calculates if animal dies by probability.
        If fitness = 0, the animal will die regardless

        Returns
        -------
        bool
            True if animal dies

        """
        prob_to_die = self.omega*(1-self.fitness)
        dies = random.random() < prob_to_die
        return bool(dies) or self.fitness <= 0

    def feed(self, available_food):  # Overwritten by carnivores
        """

        Parameters
        ----------
        available_food : float

        Returns
        -------
        float
            Remaining fodder in the cell

        """
        if self.F <= available_food:
            self.weight += self.beta * self.F
            return available_food - self.F

        if 0 < available_food:
            self.weight += self.beta * available_food

        return 0

    def lose_weight(self):
        """Yearly passive weight loss"""
        self.weight -= self.eta*self.weight


class Herbivore(BaseAnimal):
    w_birth = 8.0
    sigma_birth = 1.5
    beta = 0.9
    eta = 0.05
    a_half = 40
    phi_age = 0.2
    w_half = 10
    phi_weight = 0.1
    mu = 0.25
    lambda_ = 1.0
    gamma = 0.2
    zeta = 3.5
    xi = 1.2
    omega = 0.4
    F = 10.0

    def __init__(self, age=0, weight=None):
        """
        Subclass of BaseAnimal, has it's own set of class parameters.

        Parameters
        ----------
        age : int
        weight : float

        """
        super().__init__(age, weight)


class Carnivore(BaseAnimal):
    w_birth = 6.0
    sigma_birth = 1.0
    beta = 0.75
    eta = 0.125
    a_half = 60.0
    phi_age = 0.4
    w_half = 4.0
    phi_weight = 0.4
    mu = 0.4
    lambda_ = 1.0
    gamma = 0.8
    zeta = 3.5
    xi = 1.1
    omega = 0.9
    F = 50.0
    DeltaPhiMax = 10.0

    def __init__(self, age=0, weight=None):
        """
        Subclass of BaseAnimal, has it's own set of class parameters.
        Overwrites feed (eats other animals)

        Parameters
        ----------
        age: int
        weight: float

        Methods
        -------
        kill_or_not
        eat
        feed

        """
        super().__init__(age, weight)

    def kill_or_not(self, herbivore):
        """Calculates if carnivore will kill herbivore"""
        probability_to_kill = ((self.fitness - herbivore.fitness) /
                               self.DeltaPhiMax)
        return bool(random.random() < probability_to_kill)

    def eat(self, meat, eaten):
        """Consumes herbivore, updates weight, will not eat more than F"""
        if meat + eaten < self.F:
            self.weight += self.beta * meat
        else:
            self.weight += self.beta*(self.F - eaten)

    def feed(self, list_herbivores_least_fit):
        """
        Iterates list of herbivores then tries to kill them.

        Cannot eat animals with greater fitness than themselves.
        Stops feeding when F(appetite) is met.

        Creates deletion list with Herbivores, then removes them
        and returns updated list of herbivores.

        Parameters
        ----------
        list_herbivores_least_fit : list
            Herbivores in ascending order by fitness

        Returns
        -------
        list_herbivores_least_fit : list
            The same list as input, killed herbivores removed

        """
        eaten = 0
        deletion_list = []
        for herbivore in list_herbivores_least_fit:
            if eaten >= self.F:
                break

            if self.fitness <= herbivore.fitness:
                continue

            if self.DeltaPhiMax < self.fitness - herbivore.fitness:
                self.eat(herbivore.weight, eaten)
                eaten += herbivore.weight
                deletion_list.append(herbivore)

            else:
                if self.kill_or_not(herbivore):
                    self.eat(herbivore.weight, eaten)
                    eaten += herbivore.weight
                    deletion_list.append(herbivore)

        for herbivore in deletion_list:
            list_herbivores_least_fit.remove(herbivore)
        return list_herbivores_least_fit


if __name__ == '__main__':
    pass
