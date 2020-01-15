# -*- coding: utf-8 -*-

"""
"""

import numpy as np

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


def sigmoid(value):
    return 1/(1 + np.exp(value))


def choose_new_location(prob_list):
    """
    Draws one out of a list with weights.

    Parameters
    ----------
    prob_list - list of tuple(loc, probabilities)

    Returns
    -------
    new_location - tuple of (y, x)
    """

    probabilities = [x[1] for x in prob_list]
    cumulative_sum = np.cumsum(probabilities)
    locations = [x[0] for x in prob_list]
    random_number = np.random.random()
    index = 0
    while random_number >= cumulative_sum[index]:
        index += 1
    new_position = locations[index]
    return new_position


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
    def set_parameters(cls, w_birth=None, sigma_birth=None, beta=None,
                       eta= None, a_half=None, phi_age=None, w_half=None,
                       phi_weight=None, mu=None, lambda_=None, gamma=None,
                       zeta=None, xi=None, omega=None, F=None,
                       DeltaPhiMax=None):
        # By checking all parameters first, set parameters does not change
        # any parameters before it is sure that all parameters are valid

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
        # self.name = generate_rand_name()
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
        # Farlig kode! Hvis du vil sjekke mer enn en gang så er den alltid True
        moved = self._has_moved
        self._has_moved = True
        return moved

    def reset_has_moved(self):
        self._has_moved = False

    def rand_move(self):
        prob_to_move = self.fitness * self.mu
        return bool(np.random.binomial(1, prob_to_move))

    def will_move(self):
        if not self.has_moved:
            if not self.rand_move():
                return True
        return False

    def migrate(self, prob_list):
        try:
            new_position = choose_new_location(prob_list)
        except ValueError:
            new_position = None
        return new_position

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

    def lose_weight(self):
        self.weight -= self.eta*self.weight


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
        deletion_list = []
        for herbivore in list_herbivores_least_fit:
            if eaten >= self.F:
                break
            if self.DeltaPhiMax < self.fitness - herbivore.fitness:
                self.eat(herbivore.weight, eaten)
                eaten += herbivore.weight
                deletion_list.append(herbivore)

            if self.fitness <= herbivore.fitness:
                continue
            else:
                if self.kill_or_not(herbivore):
                    self.eat(herbivore.weight, eaten)
                    eaten += herbivore.weight
                    deletion_list.append(herbivore)

        for herbivore in deletion_list:
            list_herbivores_least_fit.remove(herbivore)
        return list_herbivores_least_fit


if __name__ == '__main__':
    
    test_animal = Animal()
    test_herb = Herbivore()
    test_carn = Carnivore()

    print(test_animal, test_herb, test_carn)
