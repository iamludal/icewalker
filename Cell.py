
class Cell:

    def __init__(self):
        """ Create a new cell for the icewalker grid

        :Examples:
        >>> c = Cell()
        >>> c.get_walls()
        set()
        >>> c.is_final_cell()
        False
        >>> c.get_content() # Return nothing since it's None
        """
        self.__content = None
        self.__walls = set()

    def is_final_cell(self):
        """ Return True if the cell if the final one, False otherwise

        :return: (bool) True if the cell if the final one
        :Examples:
        >>> c = Cell()
        >>> c.is_final_cell()
        False
        >>> c.set_final_cell()
        >>> c.is_final_cell()
        True
        """
        return self.__content == '☐'

    def set_final_cell(self):
        """ Define the current cell as the final one

        :Examples:
        >>> c = Cell()
        >>> c.set_final_cell()
        >>> c.is_final_cell()
        True
        """
        self.__content = '☐'

    def is_empty(self):
        """ Return a boolean value that says whether or not the cell is empty

        :return: (bool) True if the cell is empty, False otherwise
        :Examples:
        >>> c = Cell()
        >>> c.is_empty()
        True
        >>> from Player import Player
        >>> p = Player(1, 2, 0)
        >>> c.set_content(p)
        >>> c.is_empty()
        False
        """
        return self.__content == None

    def get_content(self):
        """ Get the content of the current cell

        :Examples:
        >>> c = Cell()
        >>> c.get_content() # Returns nothing since it's 'None'
        >>> c.set_final_cell()
        >>> c.get_content()
        '☐'
        """
        return self.__content

    def set_content(self, content):
        """ Define the new content of the cell

        :param content: (any) the content to put in the cell
        :UC: None
        :Examples:
        >>> c = Cell()
        >>> from Player import Player
        >>> p = Player(1, 2, 3)
        >>> c.set_content(p)
        >>> c.get_content()
        Player 3
        """
        self.__content = content

    def add_wall(self, direction):

        if direction not in {'E', 'S'}:
            raise ValueError("direction must be either 'E' or 'S'")

        self.__walls.add(direction)

    def get_walls(self):
        """ Returns the walls of the cell

        :return: (set) the walls around the cell
        :Examples:
        >>> c = Cell()
        >>> c.get_walls()
        set()
        >>> c.add_wall('E')
        >>> c.get_walls().issubset({'E'})
        True
        >>> c.add_wall('S')
        >>> walls = c.get_walls()
        >>> walls.issubset({'E', 'S'})
        True
        >>> 'E' in walls and 'S' in walls
        True
        """
        return self.__walls

    def __str__(self):
        """ Convert the cell into a string

        :return: (str) the string corresponding to the cell
        :Examples:
        >>> c = Cell()
        >>> str(c)
        '  '
        >>> c.set_final_cell()
        >>> str(c)
        '☐ '
        >>> c.add_wall('E')
        >>> str(c)
        '☐|'
        >>> from Player import Player
        >>> p = Player(1, 2, 0)
        >>> c.set_content(p)
        >>> str(c)
        '0|'
        """

        if self.is_empty():
            string = ' '
        else:
            string = str(self.__content)

        if 'E' in self.__walls:
            string += '|'
        else:
            string += ' '

        return string

    def __repr__(self):
        """ Get a representation of the cell

        :Examples:
        >>> c = Cell()
        >>> c
        <BLANKLINE>
        >>> c.add_wall('E')
        >>> c
         |
        """
        return str(self)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
