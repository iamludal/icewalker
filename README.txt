How to use it ?
===============

1. Move into the src/ folder
2. Open up a terminal and type in the following command:

  $ python3 main-console.py ../data/[grid].json
  (to play with the console, where grid is a grid from the data/ folder)

  $ python3 main-gui.py ../data/[grid].json
  (to play with the graphical interface, where grid is a grid from the data/ folder)


How to solve a game ?
=====================

To solve a game, move into the src/ folder, open up
a terminal and just type in the following command:

  $ python3 Solver.py [config]
  (where [config] is the path of the config file)

    Example:
      $python3 Solver.py ../data/grid4.json


Changelog
=========

To see the different changes, with their corresponding
dates, just move into the root folder of the project and
type in a terminal the following command:

  $ git log --oneline

If you want informations about a specific change:
  $ git show [commit_hash]

