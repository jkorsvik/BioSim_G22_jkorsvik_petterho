# -*- coding: utf-8 -*-

"""
"""
import random
import numpy as np


__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


def sigmoid(fodder, same_species, F):
    np.exp(fodder/(same_species+1)*F)


class Animal:
    def __init__(self):
        raise NotImplementedError

    def migrate(self):
        prob_to_move = self.fitness*self.mu
        if random.random() < prob_to_move:
            neighbour_tiles = []  # dette ligger hos cellen



    def birth(self):
        raise NotImplementedError

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

    def __init__(self):
        raise NotImplementedError

    def feed(self):
        raise NotImplementedError

    @classmethod
    def change_parameter(cls, parameters):
        try:
            cls.parameter
        except ValueError:
            raise NameError('No parameter with given name for Carnivore')


class Carnivore(Animal, ABC):
    def __init__(self):
        raise NotImplementedError

    def feed(self):
        raise NotImplementedError
