# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


from .island import Island
from .visualization import Visuals
from .landscape import (
    Jungle, Ocean, Savanna, Mountain, Desert
)
from .animals import Herbivore, Carnivore
import textwrap
import pandas as pd
import numpy as np
import subprocess
import random
import pickle
import os


FFMPEG = os.path.join(os.path.dirname(__file__), '../../FFMPEG/ffmpeg.exe')

# Retrieved from:
# https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file/32216025


def save_sim(simulation, name):
    """
    Save a state of Simulation

    Parameters
    ----------
    simulation : object
        Instance of Simulation
    name : str
        Save name

    Returns
    -------

    """
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(simulation, f, pickle.HIGHEST_PROTOCOL)


def load_sim(name):
    """
    Loads state of Simulation

    Parameters
    ----------
    name : file
        Name of file

    Returns
    -------
    Loaded file of Simulation

    """
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


class BioSim:
    default_map = """
                      OOOOOOOOOOOOOOOOOOOOO
                      OSSSSSJJJJMMJJJJJJJOO
                      OSSSSSJJJJMMJJJJJJJOO
                      OSSSSSJJJJMMJJJJJJJOO
                      OOSSJJJJJJJMMJJJJJJJO
                      OOSSJJJJJJJMMJJJJJJJO
                      OOOOOOOOSMMMMJJJJJJJO
                      OSSSSSJJJJMMJJJJJJJOO
                      OSSSSSSSSSMMJJJJJJOOO
                      OSSSSSDDDDDJJJJJJJOOO
                      OSSSSSDDDDDJJJJJJJOOO
                      OSSSSSDDDDDJJJJJJJOOO
                      OSSSSSDDDDDMMJJJJJOOO
                      OSSSSDDDDDDJJJJOOOOOO
                      OOSSSSDDDDDDJOOOOOOOO
                      OOSSSSDDDDDJJJOOOOOOO
                      OSSSSSDDDDDJJJJJJJOOO
                      OSSSSDDDDDDJJJJOOOOOO
                      OOSSSSDDDDDJJJOOOOOOO
                      OOOSSSSJJJJJJJOOOOOOO
                      OOOSSSSSSOOOOOOOOOOOO
                      OOOOOOOOOOOOOOOOOOOOO
                  """
    default_map = textwrap.dedent(default_map)

    default_population = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        },
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]

    def __init__(
        self,
        island_map=None,
        ini_pop=None,
        seed=None,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
        movie_fmt="mp4",
        island_save_name=None,
        store_stats=False
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing
            animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal
            densities
        :param img_base: String with beginning of file name for figures,
            including path
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param island_save_name: Name of previously saved game, directory is
            already defined within the project.
        :param store_stats: boolean statement, wether to store all dead and
            born animals overtime for analysis

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        if ini_pop is None:
            ini_pop = self.default_population
        if island_save_name is None:
            if island_map is None:
                self.island = Island(self.default_map, ini_pop, store_stats)
            else:
                self.island = Island(island_map, ini_pop, store_stats)
        else:
            self.island = load_sim(island_save_name)

        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.movie_fmt = movie_fmt

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        animal_species = {'Herbivore': Herbivore,
                          'Carnivore': Carnivore}

        animal_species[species].set_parameters(**params)

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        map_params = {'O': Ocean,
                      'M': Mountain,
                      'D': Desert,
                      'S': Savanna,
                      'J': Jungle}

        map_params[landscape].set_parameters(**params)

    def clean_simulation(self, num_years): # Change name and docstring
        """
        A simulation for running profile, so that it doesnt care about
        the visuals.

        Parameters
        ----------
        num_years : int

        Returns
        -------

        """
        index = 1
        while index <= num_years:
            self.island.simulate_one_year()
            index += 1
            # print(self.year, '\n', self.num_animals_per_species)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
            (default: vis_years)

        Image files will be numbered consecutively.
        """

        num_years_fig = self.island.year + num_years
        visuals = Visuals(self.island, num_years_fig, self.ymax_animals,
                          self.cmax_animals, self.img_base, self.img_fmt)

        if img_years is None:
            img_years = vis_years
        if img_years % vis_years != 0:
            raise ValueError('img_years must be a multiple of vis_years')
        if self.img_base is not None:
            visuals.save_fig()

        index = 1
        while index <= num_years:
            self.island.simulate_one_year()
            if index % vis_years == 0:
                visuals.update_fig(self.island)
            if self.img_base is not None:
                if index % img_years == 0:
                    visuals.save_fig()
            index += 1

    def add_population(self, population):
        """
        Add a population to the island
        Calls function from Island.py

        :param population: List of dictionaries specifying population

        """
        self.island.add_population(population)

    @property
    def year(self):
        """Last year simulated."""
        return self.island.year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.island.num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self.island.num_animals_per_species

    @property
    def animal_distribution(self):
        #Add save the data frame if the user gives a save path
        """Pandas DataFrame with animal count per species for each cell
        on island."""
        dict_for_df = {"Row": [], "Col": [], "Herbivore": [], "Carnivore": []}
        for pos, cell in self.island.map.items():
            row, col = pos
            dict_for_df["Row"].append(row)
            dict_for_df["Col"].append(col)
            dict_for_df["Herbivore"].append(cell.num_herbivores)
            dict_for_df["Carnivore"].append(cell.num_carnivores)

        df_sim = pd.DataFrame.from_dict(dict_for_df)
        df_sim.to_csv(r'C:\Users\pbmar\Documents\NMBU\INF200\data.csv')
        return df_sim

    def island_stats(self):
        """
        Creates dictionary for birth and death rate. Can be used as an example
        for extracting data from stats.

        Returns
        -------
        death_rate_per_year_herb : dict
            key : year, value : float
        death_rate_per_year_carn : dict
            key : year,  value : float
        birth_rate_per_year_herb : dict
            key : year, value : float
        birth_rate_per_year_carn : dict
            key : year, value : float

        """
        death_rate_per_year_herb = {}
        death_rate_per_year_carn = {}
        birth_rate_per_year_herb = {}
        birth_rate_per_year_carn = {}

        for year, value in self.island.stats.items():
            deaths_herb = 0
            deaths_carn = 0
            born_herb = 0
            born_carn = 0
            death_per_pos_herb = value['Herbivore']['death']
            death_per_pos_carn = value['Carnivore']['death']
            birth_per_pos_herb = value['Herbivore']['birth']
            birth_per_pos_carn = value['Carnivore']['birth']

            N_herbivores = value['Herbivore']['alive']
            for dead in death_per_pos_herb.values():
                deaths_herb += len(dead)
            death_rate_per_year_herb[year] = deaths_herb / N_herbivores

            for born in birth_per_pos_herb.values():
                born_herb += len(born)
            birth_rate_per_year_herb[year] = born_herb / N_herbivores

            N_carnivores = value['Carnivore']['alive']
            if N_carnivores <= 0:
                continue
            for dead in death_per_pos_carn.values():
                deaths_carn += len(dead)
            death_rate_per_year_carn[year] = deaths_carn / N_carnivores

            for born in birth_per_pos_carn.values():
                born_carn += len(born)
            birth_rate_per_year_carn[year] = born_carn / N_carnivores

        return (
            death_rate_per_year_herb, death_rate_per_year_carn,
            birth_rate_per_year_herb, birth_rate_per_year_carn
        )

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if self.movie_fmt == 'mp4':
            try:
                subprocess.check_call(f'{FFMPEG} -y -r 24 -i '
                                      f'{self.img_base}_%05d.{self.img_fmt}'
                                      f' -c:v libx264 -vf fps=25 -pix_fmt '
                                      f'yuv420p '
                                      f'{self.img_base}.{self.movie_fmt}')
            except subprocess.CalledProcessError as err:
                raise RuntimeError(f'ERROR: ffmpeg failed with: {err}')
        else:
            raise ValueError('Unknown movie format: ' + self.movie_fmt)

    def save_sim(self, name):
        """Calls function: save_sim outside Simulation"""
        save_sim(self.island, name)


if __name__ == '__main__':
    pass
