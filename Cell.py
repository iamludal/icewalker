
class Cell:

    def __init__(self):
        self.__content = None
        self.__walls = set()

    def is_empty(self):
        """ Return a boolean value that says whether or not the cell is empty

        :return: True if the cell is empty, False otherwise
        :rtype: bool
        :Examples:
        >>> c = Cell()
        >>> c.is_empty()
        True
        """
        return self.__content is None

    def add_wall(self, direction):

        if direction not in {'E', 'S'}:
            raise ValueError("direction must be either 'E' or 'S'")

        self.__walls.add(direction)

    def get_walls(self):
        return self.__walls

    def __str__(self):
        """ Convert the cell into a string

        :return: the string corresponding to the cell
        :rtype: str
        :Examples:
        >>> c = Cell()
        >>> str(c)
        ' '
        """

        if 'E' in self.__walls:
            string = '|'
        else:
            string = ' '

        if self.is_empty():
            string += ' '
        else:
            string += str(self.__content)

        return string


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
