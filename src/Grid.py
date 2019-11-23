from Cell import Cell
from Player import Player
import json
from json.decoder import JSONDecodeError


class Grid:

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
        elif not x in range(self.get_width()) or y not in range(self.get_height()):
            raise ValueError("x and y must be in the grid's dimensions")

        return self.__grid[y][x]

    def get_height(self):
        return self.__height

    def get_width(self):
        return self.__width

    def add_wall(self, wall):
        """ Add a wall to a certain cell

        :param wall: (list) a list of the form [x, y, direction], where x and
            y are the coordinates of a cell in the grid and direction the
            direction of the wall to add
        :raises TypeError: if the list if not of the correct form
        :UC: wall[3] in {'E', 'S'}
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
        :UC: filename.endswith(".json")
        """

        try:
            with open(filename) as f:
                data = json.load(f)
        except FileNotFoundError:
            exit("Error: file not found")
        except JSONDecodeError:
            exit("Error: wrong file type. You must use a JSON file")

        try:
            dimensions = data['dimensions']
            width, height = dimensions['width'], dimensions['height']

            g = cls(width, height)

            final_cell_x, final_cell_y = data['final_cell']

            g.get_cell(final_cell_x, final_cell_y).set_final_cell()

            main_x, main_y = data['players']['main']
            other_players = data['players']['others']

            main_player = Player(main_x, main_y, 0)
            other_players = [Player(x, y, i)
                             for i, (x, y) in enumerate(other_players, 1)]

            players = [main_player] + other_players

            for wall in data['walls']:
                g.add_wall(wall)

            for player in players:
                g.set_player(player)

        except KeyError:
            exit("Invalid config file.")

        return g, players

    def set_player(self, player):
        """ Set a player on the grid depending on its coordinates

        :param player: (Player) the player to set on the grid
        """
        x, y = player.get_coordinates()
        self.get_cell(x, y).set_content(player)

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


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
