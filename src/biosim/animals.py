# -*- coding: utf-8 -*-

"""
"""

import numpy as np


__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


def sigmoid(value):
    return 1/(1 + np.exp(value))


""""
def probability_for_moving(list_for_moving):
    sum_propensity = 0
    for fodder, same_species, F in list_for_moving:
        sum_propensity += propensity(fodder, same_species, F)
    probability = propensity(fodder, same_species, F) / sum_propensity
    return probability
    """


class Animal:
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

    def __init__(self, age=0, weight=None):
        self._age = age
        self._weight = weight
        self._compute_fitness = True
        self._fitness = None
        self._has_moved = False
        if weight is None:
            normal = np.random.normal(self.w_birth, self.sigma_birth)
            self.weight = normal
            if normal < 0:
                self.weight = 0  # newborns with <= 0 will die end of year

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self):
        string = f"Animal Type: {type(self).__name__}\n" \
                 f"Age: {self.age}\n" \
                 f"Weight: {self.weight}\n" \
                 f"Fitness: {self.fitness}\n"
        return string

    def reset_has_moved(self):
        self._has_moved = False
    """
    def migrate(self, list_for_moving):
        # Liste som skal inn er Fodder og dyr av samme type, med lokasjon
        prob_to_move = self.fitness*self.mu
        self._has_moved = True
        if bool(np.random.binomial(1, prob_to_move)):
            list_for_moving = []
            cumulative_sum = np.cumsum(probability_for_moving(list_for_moving))
            index = 0
            while not np.random.binomial(1, cumulative_sum[index]):
                index += 1
            return index
        # return Bool, new_location
        pass"""

    def will_migrate(self):
        prob_to_move = self.fitness * self.mu
        return bool(np.random.binomial(1, prob_to_move))

    def birth(self, num_same_species):
        mates = num_same_species - 1
        prob_to_birth = np.minimum(1, (self.gamma * self.fitness * mates))
        if self.weight < self.zeta*(self.w_birth + self.phi_weight):
            return 0

        if np.random.binomial(1, prob_to_birth):
            offspring = type(self)()
            weight_loss = self.xi * offspring.weight

            if self.weight >= weight_loss:
                self.weight -= weight_loss
                return offspring

        return 0

    def lose_weight(self):
        self.weight -= self.eta*self.weight

    def death(self):
        prob_to_die = self.omega*(1-self.fitness)
        dies = np.random.binomial(1, prob_to_die)
        return bool(dies) or self.fitness <= 0

    def feed(self, available_food):  # Will be overwritten by the subclasses
        if self.F <= available_food:
            self.weight += self.beta * self.F
            return available_food - self.F

        if 0 < available_food:
            self.weight += self.beta * available_food

        return 0

    @property
    def fitness(self):
        if self._compute_fitness is True:
            if self.weight <= 0:
                return 0

            pos_q_age = self.phi_age * (self.age - self.a_half)
            neg_q_weight = - (self.phi_weight * (self.weight - self.w_half))

            self._compute_fitness = False
            self._fitness = (sigmoid(pos_q_age)
                             * sigmoid(neg_q_weight)
                             )
            return self._fitness

        return self._fitness

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_age):
        self._compute_fitness = True
        self._age = new_age

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, new_weight):
        self._compute_fitness = True
        self._weight = new_weight

    @property
    def has_moved(self):
        moved = self._has_moved
        self._has_moved = True
        return moved


class Herbivore(Animal):
    w_birth = 8.0
    sigma_birth = 1.5
    beta = 0.9
    eta = 0.05  # sjekker med lavere eta
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
        super().__init__(age, weight)


class Carnivore(Animal):
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
        super().__init__(age, weight)

    def kill_or_not(self, herbivore):
        probability_to_kill = ((self.fitness - herbivore.fitness) /
                               self.DeltaPhiMax)
        return bool(np.random.binomial(1, probability_to_kill))

    def eat(self, meat, eaten):
        if meat + eaten < self.F:
            self.weight += self.beta * meat
        else:
            self.weight += self.beta*(self.F - eaten)

    def feed(self, list_herbivores_least_fit):
        eaten = 0
        deletion_list_ind = []
        for ind, herbivore in enumerate(list_herbivores_least_fit):
            if eaten >= self.F:
                break
            if self.DeltaPhiMax < self.fitness - herbivore.fitness:
                self.eat(herbivore.weight, eaten)
                eaten += herbivore.weight
                deletion_list_ind.append(ind)

            if self.fitness <= herbivore.fitness:
                continue
            else:
                if self.kill_or_not(herbivore):
                    self.eat(herbivore.weight, eaten)
                    eaten += herbivore.weight
                    deletion_list_ind.append(ind)

        for ind in reversed(deletion_list_ind):
            del list_herbivores_least_fit[ind]
        return list_herbivores_least_fit


if __name__ == '__main__':
    
    test_animal = Animal()
    test_herb = Herbivore()
    test_carn = Carnivore()

    print(test_animal, test_herb, test_carn)
