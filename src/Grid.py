from Cell import Cell
from Player import Player
import json
from json.decoder import JSONDecodeError


class Grid:
    """ This class represents a Grid of the Ice Walker game, which
    means the main board on which the players are

    :Examples:

    >>> grid = Grid(2, 2)
    >>> grid.add_wall([0, 1, 'E'])
    >>> grid.get_cell(0, 1)
     |
    >>> p = Player(1, 0, 0)
    >>> grid.set_player(p)
    >>> grid.get_cell(1, 0)
    0|
    >>> print(grid)
    +-+-+
    |  0|
    +   +
    | | |
    +-+-+
    """

    def __init__(self, width, height):
        """ Create a grid to represent a new icewalker game

        :param width: (int) the width of the grid
        :param height: (int) the height of the grid
        :raises TypeError: if width/height are not integers
        :raises ValueError: if width < 0 or height < 0
        :UC: width > 0, height > 0
        :Examples:

        >>> g = Grid(2, 2)
        >>> g = Grid('E', 'S')
        Traceback (most recent call last):
        ...
        TypeError: Grid dimensions must be positive integers
        >>> g = Grid(2, -1)
        Traceback (most recent call last):
        ...
        ValueError: Grid dimensions must be positive integers
        """

        if type(width) != int or type(height) != int:
            raise TypeError("Grid dimensions must be positive integers")
        elif width <= 0 or height <= 0:
            raise ValueError("Grid dimensions must be positive integers")

        self.__width = width
        self.__height = height
        self.__grid = [[Cell() for x in range(width)] for y in range(height)]
        self.players = []

        for line in self.__grid:
            line[-1].add_wall('E')

    def get_cell(self, x, y):
        """ Return the cell of coordinates (x, y)

        :param x: (int) the x coordinate
        :param y: (int) the y coordinate
        :return: (Cell) the corresponding cell
        :UC: x in range(grid_width) and y in range(grid_height)
        :Examples:

        >>> g = Grid(2, 2)
        >>> g.add_wall([1, 0, 'E'])
        >>> g.get_cell(1, 0)
         |
        >>> g.get_cell(1, 2)
        Traceback (most recent call last):
        ...
        ValueError: x and y must be in the grid's dimensions
        """

        if type(x) != int or type(y) != int:
            raise TypeError("x and y must be positive integers")
        elif x not in range(self.get_width()) or y not in range(self.get_height()):
            raise ValueError("x and y must be in the grid's dimensions")

        return self.__grid[y][x]

    def get_height(self):
        """ Return the height of the grid
        :return: (int) the height
        """
        return self.__height

    def get_width(self):
        """ Return the width of the grid
        :return: (int) the width
        """
        return self.__width

    def add_wall(self, wall):
        """ Add a wall to a certain cell

        :param wall: (list) a list of the form [x, y, direction], where x and
            y are the coordinates of a cell in the grid and direction the
            direction of the wall to add
        :raises TypeError: if the list if not of the correct form
        :UC: wall[2] in {'E', 'S'}
        :Examples:

        >>> g = Grid(3, 3)
        >>> g.add_wall([2, 2, 'E'])
        >>> g.get_cell(2, 2)
         |
        >>> g.add_wall([1, 2])
        Traceback (most recent call last):
        ...
        TypeError: wall must be a list (or a tuple) of length 3
        """
        if type(wall) not in {list, tuple} or len(wall) != 3:
            raise TypeError("wall must be a list (or a tuple) of length 3")

        x, y, direction = wall

        self.get_cell(x, y).add_wall(direction)

    @classmethod
    def from_file(cls, filename):
        """ Load a grid from a JSON file

        :param filename: (str) the path to the file to load
        :return: (tuple) the newly created instance of the grid + the list
            of players
        :UC: filename.endswith(".json")

        """

        try:
            with open(filename) as f:
                data = json.load(f)
        except FileNotFoundError:
            exit("File not found")
        except JSONDecodeError:
            exit("The config is either badly-formed or not a JSON file.")

        try:
            width, height = data["dimensions"]

            grid = cls(width, height)

            final_cell_x, final_cell_y = data['final_cell']

            grid.get_cell(final_cell_x, final_cell_y).set_final_cell()

            main_x, main_y = data['players']['main']
            other_players = data['players']['others']

            main_player = Player(main_x, main_y, 0)
            other_players = [Player(x, y, i)
                             for i, (x, y) in enumerate(other_players, 1)]

            players = [main_player] + other_players
            grid.players = []

            for wall in data['walls']:
                grid.add_wall(wall)

            for player in players:
                grid.set_player(player)

            for x, y in data['thawed']:
                grid.get_cell(x, y).thaw()

        except (KeyError, TypeError, ValueError):
            exit("Invalid config file.")

        return grid

    def set_player(self, player):
        """ Set a player on the grid depending on its coordinates

        :param player: (Player) the player to set on the grid
        :return: None
        :UC: player_x in range(grid_width), player_y in range(grid_height)
        :Examples:

        >>> p = Player(2, 4, 0)
        >>> g = Grid(8, 8)
        >>> g.get_cell(2, 4).is_empty()
        True
        >>> g.set_player(p)
        >>> g.get_cell(2, 4).is_empty()
        False

        """
        x, y = player.get_coordinates()

        self.get_cell(x, y).set_content(player)

        if player not in self.players:
            self.players.insert(player.get_n(), player)

    def __str__(self):
        """ Draw the grid

        :Examples:

        >>> g = Grid(3, 3)
        >>> g.add_wall([0, 2, 'E'])
        >>> print(g)
        +-+-+-+
        |     |
        +     +
        |     |
        +     +
        | |   |
        +-+-+-+
        >>> g.add_wall([0, 0, 'E'])
        >>> print(g)
        +-+-+-+
        | |   |
        +     +
        |     |
        +     +
        | |   |
        +-+-+-+
        >>> g.add_wall([1, 0, 'S'])
        >>> g.add_wall([0, 0, 'E'])
        >>> g.add_wall([1, 0, 'E'])
        >>> print(g)
        +-+-+-+
        | | | |
        + +-+ +
        |     |
        +     +
        | |   |
        +-+-+-+
        >>> g.add_wall([1, 1, 'E'])
        >>> g.add_wall([1, 1, 'S'])
        >>> print(g)
        +-+-+-+
        | | | |
        + +-+ +
        |   | |
        + +-+ +
        | |   |
        +-+-+-+
        >>> g.add_wall([2, 1, 'S'])
        >>> print(g)
        +-+-+-+
        | | | |
        + +-+ +
        |   | |
        + +-+-+
        | |   |
        +-+-+-+
        >>> g = Grid(4, 3)
        >>> g.add_wall([1, 0, 'E'])
        >>> g.add_wall([1, 1, 'E'])
        >>> print(g)
        +-+-+-+-+
        |   |   |
        +   +   +
        |   |   |
        +       +
        |       |
        +-+-+-+-+
        """

        grid = '+-' * self.get_width() + '+' + '\n'  # top border

        for y, line in enumerate(self.__grid):

            grid += '|'  # left border

            for cell in line:
                grid += str(cell)

            # To start a new line
            grid += '\n'

            # Last line
            if y + 1 >= self.get_height():
                break

            # Other lines
            grid += '+'  # start of the 2nd line

            for x, cell in enumerate(line):

                E_in_cell_walls = 'E' in cell.get_walls()
                S_in_cell_walls = 'S' in cell.get_walls()

                if S_in_cell_walls:
                    grid += '-'
                else:
                    grid += ' '

                E_in_south_cell = 'E' in self.get_cell(x, y+1).get_walls() \
                    if y + 1 < self.get_height() else False
                S_in_east_cell = 'S' in self.get_cell(x+1, y).get_walls() \
                    if x + 1 < self.get_width() else False

                if x >= self.get_width() - 1:
                    break
                elif E_in_cell_walls and S_in_cell_walls:
                    grid += '+'
                elif E_in_cell_walls and S_in_east_cell:
                    grid += '+'
                elif S_in_cell_walls and E_in_south_cell:
                    grid += '+'
                elif E_in_south_cell and S_in_east_cell:
                    grid += '+'
                elif S_in_cell_walls and S_in_east_cell:
                    grid += '+'
                elif E_in_cell_walls and E_in_south_cell:
                    grid += '+'
                else:
                    grid += ' '

            grid += '+' + '\n'  # right border

        grid += '+-' * self.get_width() + '+'  # bottom border

        return grid

    def coord_players(self):
        """ Returns a list containing the coordinates of all players

        :return: (list) all the coordinates
        :Examples:

        >>> from Player import Player
        >>> grid = Grid(4, 4)
        >>> p1 = Player(1, 1, 0)
        >>> p2 = Player(2, 3, 1)
        >>> grid.set_player(p1)
        >>> grid.set_player(p2)
        >>> grid.coord_players()
        [(1, 1), (2, 3)]
        """
        return [player.get_coordinates() for player in self.players]

    def is_in(self, iterable):
        """ Returns True if the grid is in a set of grids, False otherwise

        :param iterable: (iterable) a set/list/tuple of grids
        :return: (bool) true if the grid is inside the iterable
        :UC: all(isinstance(elt, Grid) for elt in iterable)
        :Examples:

        >>> g1 = Grid(3, 3)
        >>> g2 = Grid(3, 3)
        >>> p1 = Player(1, 1, 0)
        >>> g2.set_player(p1)
        >>> g1.is_in([g2])
        False
        >>> g1.set_player(p1)
        >>> g1.is_in([g2])
        True
        """
        return all(self.coord_players() == other.coord_players()
                   for other in iterable)

    def get_move_to(self, other):
        """ Get the move to go from a grid to another

        :param other: (Grid) the other grid
        :return: (tuple) the player to move and the direction
        :UC: self players and other players must be the same and the grid must
            have equal lengths
        :Examples:

        >>> g1 = Grid(3, 3)
        >>> g2 = Grid(3, 3)
        >>> g1.set_player(Player(0, 1, 0))
        >>> g2.set_player(Player(2, 1, 0))
        >>> g1.get_move_to(g2)
        (0, 'E')
        """
        self_coords, other_coords = self.coord_players(), other.coord_players()

        for i in range(len(self_coords)):
            if self_coords[i] != other_coords[i]:
                player_to_move = i

        x_from, y_from = self_coords[player_to_move]
        x_to, y_to = other_coords[player_to_move]

        if x_from < x_to:
            direction = "E"
        elif x_from > x_to:
            direction = "W"
        elif y_from < y_to:
            direction = "S"
        elif y_from > y_to:
            direction = "N"

        return player_to_move, direction


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
