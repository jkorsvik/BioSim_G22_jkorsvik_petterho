# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


from src.biosim.island import Island
from src.biosim.visualization import Visuals
from src.biosim.landscape import (
    Jungle, Ocean, Savanna, Mountain, Desert
)
import textwrap
import pandas as pd
import numpy as np
import subprocess
import random
import pickle


# Needs to be updated to the filepath in your directory

FFMPEG = r'C:\Users\Jkors\OneDrive\Dokumenter\INF200\Prosjekt' \
         r'\BioSim_G22_jkorsvik_petterho\BioSim_G22_jkorsvik_petterho' \
         r'\FFMPEG\ffmpeg.exe'

# Retrieved from:
# https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file/32216025


def save_sim(simulation, name ):
    with open('saved_simulation/' + name + '.pkl', 'wb') as f:
        pickle.dump(simulation, f, pickle.HIGHEST_PROTOCOL)


def load_sim(name):
    with open('saved_simulation/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
#

class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed=None,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
        movie_fmt="mp4",
        island_save_name=None
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
        if island_save_name is None:
            self.island = Island(island_map, ini_pop)
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
        globals()[species].set_parameters(**params)

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

    def clean_simulation(self, num_years):
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
            print(self.num_animals_per_species, '\n',
                  self.year)

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
        visuals.save_fig()

        index = 1
        while index <= num_years:
            self.island.simulate_one_year()
            if index % vis_years == 0:
                visuals.update_fig(self.island)
            if index % img_years == 0:
                visuals.save_fig()
            index += 1
            print(self.num_animals_per_species, '\n',
                  self.year)

    def add_population(self, population):
        """
        Add a population to the island
        Calls function from Island.py

        :param population: List of dictionaries specifying population

        Parameters
        ----------
        self
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

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if self.movie_fmt == 'mp4':
            try:
                subprocess.check_call(f'{FFMPEG} -y -r 24 -i '
                                      f'{self.img_base}%03d.{self.img_fmt}'
                                      f' -c:v libx264 -vf fps=25 -pix_fmt '
                                      f'yuv420p '
                                      f'{self.img_base}.{self.movie_fmt}')
            except subprocess.CalledProcessError as err:
                raise RuntimeError(f'ERROR: ffmpeg failed with: {err}')
        else:
            raise ValueError('Unknown movie format: ' + self.movie_fmt)

    def save_sim(self, name):
        save_sim(self.island, name)


if __name__ == '__main__':
    geography = """\
            OOOOOOOOOOOOOOOOOOOOO
            OOOOOOOOSMMMMJJJJJJJO
            OSSSSSJJJJMMJJJJJJJOO
            OSSSSSSSSSMMJJJJJJOOO
            OSSSSSJJJJJJJJJJJJOOO
            OSSSSSJJJDDJJJSJJJOOO
            OSSJJJJJDDDJJJSSSSOOO
            OOSSSSJJJDDJJJSOOOOOO
            OSSSJJJJJDDJJJJJJJOOO
            OSSSSJJJJDDJJJJOOOOOO
            OOSSSSJJJJJJJJOOOOOOO
            OOOSSSSJJJJJJJOOOOOOO
            OOOOOOOOOOOOOOOOOOOOO
            """
    geography = textwrap.dedent(geography)

    ini_herbs = [
        {
            "loc": (2, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(2000)
            ],
        }
    ]

    ini_carn = [
        {
            "loc": (2, 1),
            "pop": [
                {"species": "Carnivore", "age": 2, "weight": 40}
                for _ in range(6)
            ],
        }
    ]


    sim = BioSim(geography, ini_herbs,
                 img_base=(r'C:\Users\Jkors\OneDrive\Dokumenter\INF200\Prosjekt\BioSim_G22_jkorsvik_petterho\BioSim_G22_jkorsvik_petterho\images_and_movies\sim_island'))
    sim.add_population(ini_carn)
    sim.simulate(100)
    sim.save_sim('Sjokolade')
    sim.make_movie()

