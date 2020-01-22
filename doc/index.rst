.. BioSim_G22 documentation master file, created by
   sphinx-quickstart on Mon Jan 20 13:09:28 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BioSim_G22's documentation!
======================================

This is a simulation of
 * an island
 * with varying environments
 * with a herbivorous and carnivorous population

The main interface is within the simulation module.
Beneath the visualization and island modules are called. Island module calls
landscape which calls animals.

In simulation you can change the parameters for the animals and environment,
you can simulate how ever long you want to, and save both figure and the island
for another time.

The Environment:
---------------
 * Jungle - 'J'
 * Savanna - 'S'
 * Desert - 'D'
 * Ocean - 'O'
 * Mountain - 'M'

The Population:
--------------
 * Herbivore - Basic vegetarian
 * Carnivore - Eat herbivores

How to initiate simulation:
--------------
Start by initializing BioSim with inputs (all set to default value):

 * island_map - has its own default map
 * ini_pop - has its own default pop
 * seed - seed for randomness
 * ymax_animals - y-limit for line graph
 * cmax_animals - density limits for heatmap
 * img_base - destination folder for images and movie
 * img_fmt - image format
 * movie_fmt - movie format
 * island_save_name - save of Island instance you want to load from
 * store_stats - set to True if you want a dictionary with lots of information

Then call for example: BioSim.simulate(50) (read documentation for more options)


Have Fun!


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Simulation
   Island
   Landscape
   Animals

   Visuals

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
