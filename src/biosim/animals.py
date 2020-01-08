# -*- coding: utf-8 -*-

"""
"""

import numpy as np


__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


def sigmoid(value):
    return 1/(1 + np.exp(value))


def propensity(fodder, same_species, F):
    return np.exp(fodder / (same_species + 1) * F)


def probability_for_moving(list_for_moving):
    sum_propensity = 0
    for fodder, same_species, F in list_for_moving:
        sum_propensity += propensity(fodder, same_species, F)
    probability = propensity(fodder, same_species, F) / sum_propensity
    return probability


class Animal:
    w_birth = 6.0
    sigma_birth = 1.0
    beta = 0.75
    eta = 0.125
    a_half = 60.0
    phi_age = 0.4
    w_half = 4.0
    phi_weight = 0
    mu = 0.4
    lambda_ = 1.0
    gamma = 0.8
    omega = 0.9

    def __init__(self, age=0, weight=None):
        self._age = age
        self._weight = weight
        self._compute_fitness = True
        self._fitness = None
        if weight is None:
            self.weight = np.random.normal(self.w_birth, self.sigma_birth)
        self.fitness = self.calculate_fitness()



    def migrate(self, list_for_moving):
        prob_to_move = self.fitness*self.mu
        if np.random.random() < prob_to_move:
            list_for_moving = []
            cumulative_sum = np.cumsum(probability_for_moving(list_for_moving))
            r = np.random.random()
            index = 0
            while r >= cumulative_sum[n]:
                index += 1
            return index

    def birth(self):

        prob_to_birth = np.min(1, self.gamma*self.fitness)
        if self.num_animals() >= 2:
            if np.random.binomial(1, 1 - prob_to_birth):


    def death(self):
        prob_to_die = self.omega*(1-self.fitness)
        return np.random.binomial(1, 1 - prob_to_die) or self.fitness <= 0

    def feed(self):  # This will be overwritten by the subclasses
        pass

    @property
    def fitness(self):
        if self.weight <= 0:
            return 0

        positive_q_age = self.phi_age * (self.age - self.a_half)
        negative_q_weight = - (self.phi_weight * (self.weight - self.w_half))

        return sigmoid(positive_q_age) * sigmoid(negative_q_weight)

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_age):
        self._compute_fitness = True
        self._age =
    # sjekk om det dette er en mulig lokasjon på kartet

    @classmethod
    def change_parameter(cls, parameters):
        try:
              #  cls.parameter
        except ValueError:
            raise NameError('No parameter with given name for Carnivore')


class Herbivore(Animal):
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
        super().__init__(self, age, weight)

    def feed(self):
        raise NotImplementedError


class Carnivore(Animal):
    w_birth = 6.0
    sigma_birth = 1.0
    beta = 0.75
    eta = 0.125
    a_half = 60.0
    phi_age = 0.4
    w_half = 4.0
    phi_weight = 0
    mu = 0.4
    lambda_ = 1.0
    gamma = 0.8
    zeta = 3.5
    xi = 1.1
    omega = 0.9
    F = 50.0
    DeltaPhiMax = 10.0

    def __init__(self, age=0, weight=None):
        super().__init__(self, age, weight)


    def feed(self):
        raise NotImplementedError
