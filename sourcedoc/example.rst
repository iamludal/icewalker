=========================
:mod:`Cell` module
=========================

Ce module contient une classe permettant de représenter une cellule (case)
de la grille du plateau de jeu.


Class description
=================

Une classe pour définir un type énuméré pour l'état du jeu.

La classe :class:`GameState`
----------------------------

.. autoclass:: minesweeper.GameState

Les trois états possibles du jeu : gagnant (winning), perdant (losing), ou inachevé (unfinished) sont décrits par trois attributs de mêmes noms.
			   
La classe :class:`Minesweeper`
------------------------------   

.. autoclass:: minesweeper.Minesweeper

Méthodes
~~~~~~~~

.. automethod:: minesweeper.Minesweeper.get_grid

.. automethod:: minesweeper.Minesweeper.get_width

.. automethod:: minesweeper.Minesweeper.get_height

.. automethod:: minesweeper.Minesweeper.get_nbombs
								
.. automethod:: minesweeper.Minesweeper.get_state

.. automethod:: minesweeper.Minesweeper.reveal_all_cells_from
								
Fonction auxiliaire
===================

.. autofunction:: minesweeper.neighborhood


