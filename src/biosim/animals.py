# -*- coding: utf-8 -*-

"""
"""
import random

import numpy as np


__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"





def sigmoid(value):
    return 1/(1 + np.exp(value))


class Animal:
    def __init__(self, age=0, weight=None):
        self.gamma = None
        self.mu = None
        self.weight = weight
        if weight is None:
            self.weight = np.random.normal(self.w_birth, self.sigma_birth)
        self.age = age
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        positive_q_age = self.phi_age * (self.age - self.a_half)
        negative_q_weight = - self.phi_weight * (self.weight - self.w_half)
        return sigmoid(positive_q_age) * sigmoid(negative_q_weight)


    @staticmethod
    def propensity(fodder, same_species, F):
        return np.exp(fodder / (same_species + 1) * F)


    def migrate(self):
        prob_to_move = self.fitness*self.mu
        if random.random() < prob_to_move:
            neighbour_tiles = []  # dette ligger hos cellen (landscape)



    def birth(self):
        prob_to_birth = np.min(1, self.gamma*self.fitness)
        if map.map[self.position].num_animals() >= 2:
            if np.random.random() < prob_to_birth:




    def death(self):
        raise NotImplementedError

    def feed(self):  # This will be overwritten by the subclasses
        pass

    @property
    def position(self):
        return self.position

    @position.setter
    def location(self, loc):
        pass
    # sjekk om det dette er en mulig lokasjon på kartet


class Herbivore(Animal, ABC):
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
        self.
        super().__init__(self, age, weight)

    def feed(self):
        raise NotImplementedError

    @classmethod
    def change_parameter(cls, parameters):
        try:
            cls.parameter
        except ValueError:
            raise NameError('No parameter with given name for Carnivore')


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
