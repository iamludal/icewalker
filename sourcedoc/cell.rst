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

.. autoclass:: Cell.Cell

La classe :class:`Minesweeper`
------------------------------   

.. autoclass:: minesweeper.Minesweeper

Méthodes
~~~~~~~~

.. automethod:: Cell.Cell.is_empty
.. automethod:: Cell.Cell.get_content
.. automethod:: Cell.Cell.set_content
.. automethod:: Cell.Cell.is_final_cell
.. automethod:: Cell.Cell.set_final_cell
.. automethod:: Cell.Cell.get_walls
.. automethod:: Cell.Cell.add_wall

