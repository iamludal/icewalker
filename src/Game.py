from Grid import Grid
from Player import Player
import json
from enum import Enum


class GameState(Enum):
    """
    A class to define an enumerated type with three values :

    * ``winning``
    * ``losing``
    * ``unfinished``

    for the three state of ice walker game.
    """
    winning = 1
    unfinished = 2


class PlayerNotFoundError:
    pass


class Game:

    def __init__(self, filename):
        self.__grid, self.__players = Grid.from_file(filename)
        self.__nb_of_players = len(self.__players)

    def play(self):

        print(self.__grid)

        play = input("Your play 'num, direction' or 'q' (quit):").strip()

        if play.lower() == 'q':
            exit("You just gave up the game")

        try:
            num, direction = map(lambda x: x.strip(), play.split(","))
            num, direction = int(num), direction.upper()

            if direction not in {'N', 'W', 'E', 'S'}:
                raise ValueError
            elif num not in range(self.__nb_of_players):
                raise PlayerNotFoundError

        except ValueError:
            print('Wrong input. Please try again.')
            self.play()
        except PlayerNotFoundError:
            print('Error: Player not found. Please try again')
            self.play()
        else:
            self.next_step(num, direction)

            if self.get_state() == GameState.winning:
                exit("You win!")

    def next_step(self, num, direction):
        player = self.__players[num]
        x, y = player.get_coordinates()

        if x == 0 and direction == 'W':
            return
        elif y == 0 and direction == 'N':
            return
        elif x == self.__grid.get_width() - 1 and direction == 'E':
            return
        elif y == self.__grid.get_height() - 1 and direction == 'S':
            return

        if direction == 'W':
            wall = 'E' in self.__grid.get_cell(x-1, y).get_walls()
            new_x = x - 1
            new_y = y

        elif direction == 'E':
            wall = 'E' in self.__grid.get_cell(x, y).get_walls()
            new_x = x + 1
            new_y = y

        elif direction == 'S':
            wall = 'S' in self.__grid.get_cell(x, y).get_walls()
            new_y = y + 1
            new_x = x

        elif direction == 'N':
            wall = 'S' in self.__grid.get_cell(x, y-1).get_walls()
            new_y = y - 1
            new_x = x

        next_cell = self.__grid.get_cell(new_x, new_y)

        if (next_cell.is_empty() or next_cell.is_final_cell()) and not wall:
            # Update grid cells and player's position
            player.set_coordinates(new_x, new_y)
            self.__grid.get_cell(x, y).set_content(None)
            self.__grid.set_player(player)

            self.next_step(num, direction)

    def get_state(self):
        x, y = self.__players[0].get_coordinates()

        if self.__grid.get_cell(x, y).is_final_cell():
            return GameState.winning
        else:
            return GameState.unfinished

    def get_grid(self):
        return self.__grid

    def __str__(self):
        return str(self.__grid)

    def __repr__(self):
        return str(self)
