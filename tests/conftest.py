# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import pytest
import textwrap
from biosim.animals import Herbivore
from biosim.landscape import Jungle
from biosim.island import Island


@pytest.fixture
def plain_map_string():
    return "OOOO\nOJSO\nOOOO"


@pytest.fixture
def test_island(ini_herbs, ini_carns):
    """
    Important that all animals are inserted to one cell.
    And only uses Jungle as passable cell

    Returns
    -------
    test_island: Island
        instance of Island class
    """
    geogr = """\
            OOOO
            OJJO
            OJJO
            OOOO"""
    geogr = textwrap.dedent(geogr)
    test_island = Island(geogr, ini_herbs)
    test_island.add_population(ini_carns)

    return test_island


@pytest.fixture
def ini_herbs():
    ini_herbs = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 40}
                for _ in range(100)
            ],
        }
    ]
    return ini_herbs


@pytest.fixture
def ini_carns():
    ini_carns = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Carnivore", "age": 2, "weight": 20}
                for _ in range(10)
            ],
        }
    ]
    return ini_carns


@pytest.fixture
def prob_herb(test_island):
    """
    It

    Returns
    -------

    """
    island = test_island
    prob_herb = island.probability_calc((1, 1), 'Herbivore')
    return prob_herb


@pytest.fixture
def prob_carn(test_island):
    island = test_island
    prob_carn = island.probability_calc((1, 1), 'Carnivore')
    return prob_carn


@pytest.fixture
def parameters_savanna():
    return {'passable': False,
            'f_max': 100,
            'alpha': 1
            }


@pytest.fixture
def default_parameters_savanna():
    return {'f_max': 300,
            'alpha': 0.3
            }


@pytest.fixture
def animal_list():
    """
    Must be to herbivores and one carnivore. (At least that maybe)

    Returns
    -------

    """
    return [
        {'species': 'Herbivore', 'age': 10, 'weight': 100},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 50},
            ]


@pytest.fixture
def carnivore_list():
    return [
        {'species': 'Carnivore', 'age': 10, 'weight': 100},
        {'species': 'Carnivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 50},
            ]


@pytest.fixture
def jungle_many_animals(animal_list):
    list_tuple = []
    for x in range(10):
        for y in range(5, 20):
            list_tuple.append((x, y))
    jungle = Jungle()
    for x, y in list_tuple:
        jungle.herbivores.append(Herbivore(x, y))
    jungle.add_animals(animal_list)
    return jungle


@pytest.fixture
def jungle_with_animals(animal_list):
    jungle = Jungle()
    jungle.add_animals(animal_list)
    return jungle


@pytest.fixture
def carnivore_parameters_right():
    return {'eta': 0.125, 'phi_age': 0.4, 'DeltaPhiMax': 10.0}


@pytest.fixture
def carnivore_parameters_wrong():
    return {'zettet': 7}


@pytest.fixture
def herbivore_list():
    list_ = []
    for x in range(10):
        for y in range(5, 20):
            list_.append((x, y))
    herb_list = []
    for x, y in list_:
        herb_list.append(Herbivore(x, y))

    return herb_list


# This is just for testing that this module setup works
@pytest.fixture
def just_five():
    return 5
