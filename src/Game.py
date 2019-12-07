from Grid import Grid
from copy import deepcopy


class PlayerNotFoundError(Exception):
    """ A class to define an error that is thrown when the user
    inputs a number that doesn't correspond to any player
    """
    pass


class Game:
    """ A class to represent the Game of icewalker
    """

    def __init__(self, grid):
        self.__grid = grid
        self.__players = grid.players

    def play(self):
        """ Asks the user for a move and the plays it

        :return: None
        """

        play = input("Your play 'num, direction' or 'q' (quit): ").strip()

        if play.lower() == 'q':
            exit("You just gave up the game")

        try:
            num, direction = map(lambda x: x.strip(), play.split(","))
            num, direction = int(num), direction.upper()

            if direction not in {'N', 'W', 'E', 'S'}:
                raise ValueError
            elif num not in range(len(self.__players)):
                raise PlayerNotFoundError

        except ValueError:
            print('Wrong input. Please try again.')
            self.play()
        except PlayerNotFoundError:
            print('Error: Player not found. Please try again')
            self.play()
        else:
            self.next_step(num, direction)

    def player_can_move(self, pos, direction, grid):
        """ Returns a boolean value that says whether or not the player
        can move

        :param pos: (tuple) the player's coordinates in the form (x, y)
        :param direction: (str) the direction to move the player into
        :param grid: (Grid) the grid where the player is
        :return: (bool) True if the player can move, False otherwise
        :UC: x in range(grid.width()) and y in range(grid.height())
             direction in {'E', 'N', 'S', 'W'}

        """
        x, y = pos

        if x <= 0 and direction == 'W':
            return False
        elif y <= 0 and direction == 'N':
            return False
        elif x >= grid.get_width() - 1 and direction == 'E':
            return False
        elif y >= grid.get_height() - 1 and direction == 'S':
            return False
        else:
            return True

    def get_new_position(self, pos, direction, grid):
        """ Get the new position of the player depending on the current
        position, the direction and the grid

        :param pos: (tuple) the current position (x, y)
        :param direction: (str) the direction
        :param grid: (Grid) the grid
        :return: (tuple) a tuple of the form (new_x, new_y, blocked)
            where new_x and new_y are the new coordinates and [blocked] is
            a boolean value that says weather or not the player is blocked
            by a wall or a player
        :UC: x in range(grid.width()) and y in range(grid.height())
             direction in {'E', 'S', 'N', 'W'}

        """
        x, y = pos

        if direction == 'W':
            blocked = 'E' in grid.get_cell(x-1, y).get_walls()
            new_x = x - 1
            new_y = y

        elif direction == 'E':
            blocked = 'E' in grid.get_cell(x, y).get_walls()
            new_x = x + 1
            new_y = y

        elif direction == 'S':
            blocked = 'S' in grid.get_cell(x, y).get_walls()
            new_y = y + 1
            new_x = x

        elif direction == 'N':
            blocked = 'S' in grid.get_cell(x, y-1).get_walls()
            new_y = y - 1
            new_x = x

        return new_x, new_y, blocked

    def move_player(self, player, pos, grid):
        """ Move the player to a new position

        :param player: (Player) the player to move
        :param pos: (tuple) where to move the player (x, y)
        :param grid: (Grid) the grid where the player is
        :return: None
        :UC: pos[0] in range(grid.width()) and pos[1] in range(grid.height())
             player is in the grid

        """
        x, y = player.get_coordinates()
        player.set_coordinates(*pos)
        grid.get_cell(x, y).set_content(None)
        grid.set_player(player)

    def next_step(self, num, direction):
        """ Move the player in a direction until he reaches a wall, a
        player or a grid border

        :param num: (int) the number corresponding to the player to move
        :param direction: (str) the direction where to move the player towards
        :return: None
        :UC: num >= 0 and direction in {'E', 'N', 'S', 'W'}

        """
        player = self.__players[num]
        x, y = pos = player.get_coordinates()
        grid = self.get_grid()

        if not self.player_can_move(pos, direction, grid):
            return
        elif grid.get_cell(x, y).is_thawed():
            return

        new_x, new_y, blocked = self.get_new_position(pos, direction, grid)
        next_cell = grid.get_cell(new_x, new_y)

        if next_cell.is_empty() and not blocked:
            self.move_player(player, (new_x, new_y), grid)
            self.next_step(num, direction)

    @classmethod
    def from_file(cls, filename):
        """ Creates a new game from a grid configuration in a file

        :param filename: (str) the path to the grid's file
        :return: (Game) a new game
        :UC: filename.endswith(".json")
        """
        grid = Grid.from_file(filename)
        return cls(grid)

    def winning(self):
        """ Returns a boolean that says whether or not the player
        wins the game

        :return: (bool) true if the player wins, false otherwise
        """
        x, y = self.__players[0].get_coordinates()
        return self.get_grid().get_cell(x, y).is_final_cell()

    def losing(self):
        """ Returns a boolean that says whether or not the player
        loses the game

        :return: (bool) true if the player loses, false otherwise
        """
        grid = self.get_grid()
        coordinates = (p.get_coordinates() for p in self.__players)
        return any(grid.get_cell(x, y).is_thawed() for (x, y) in coordinates)

    def get_grid(self):
        """ Get the grid corresponding to the current game

        :return: (Grid) the grid of the game
        """
        return self.__grid

    def explore(self, num, direction):
        """ Explore the game without affecting the current one. It will return
        a new instance of game, generated by exploring the initial one in the
        direction [direction] with the player [player]

        :param num: (int) the number of the player
        :param direction: (str) the direction to explore
        :return: (Game) a new instance of game
        :UC: n in range(num_of_players)
             direction in {"E", "S", "N", "W"}
        """
        grid = deepcopy(self.get_grid())
        g = Game(grid)
        g.next_step(num, direction)
        return g

    def moves(self):
        """ Returns a list containing the grids generated by playing all the players
        of the current grid in all directions.

        :return: (list of Grid objects) the list of all grids
        """
        grids = []

        for player in self.__players:
            for direction in {"N", "S", "E", "W"}:
                game = self.explore(player.get_n(), direction)
                grids.append(game.get_grid())

        return grids

    def __str__(self):
        return str(self.__grid)

    def __repr__(self):
        return str(self)
