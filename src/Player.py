
class Player:

    def __init__(self, x, y, n):
        """ Creation a new icewalker Player

        :param x: (int) the x coordinate of the player
        :param y: (int) the y coordinate of the player
        :param n: (int) the number corresponding to the player
        :UC: x > 0, y > 0, n >= 0
        :raises TypeError: if x, y or n is not an integer
        :raises ValueError: if x, y or n is less than 0
        :Examples:
        >>> p = Player(1, 2, 0)
        >>> p.get_coordinates()
        (1, 2)
        >>> p.get_n()
        0
        >>> p = Player(-1, 2, 0) 
        Traceback (most recent call last):
        ...
        ValueError: x coordinate must be a positive integer
        >>> p = Player(2, '3', 0)
        Traceback (most recent call last):
        ...
        TypeError: y coordinate must be a positive integer
        >>> p = Player(2, 3, -5)
        Traceback (most recent call last):
        ...
        ValueError: Player number must be an integer in [0, 10]
        """

        if type(x) != int:
            raise TypeError("x coordinate must be a positive integer")
        elif x < 0:
            raise ValueError("x coordinate must be a positive integer")

        if type(y) != int:
            raise TypeError("y coordinate must be a positive integer")
        elif y < 0:
            raise ValueError("y coordinate must be a positive integer")

        if type(n) != int:
            raise TypeError("Player number must be an integer in [0, 10]")
        elif n not in range(11):
            raise ValueError("Player number must be an integer in [0, 10]")

        self.__x = x
        self.__y = y
        self.__n = n

    def get_coordinates(self):
        """ Return the coordinates of the Player

        :return: (tuple) the coordinates
        :Examples:
        >>> p = Player(3, 2, 0)
        >>> p.get_coordinates()
        (3, 2)
        """
        return self.__x, self.__y

    def get_n(self):
        """ Return the number of the player

        :return: (int) the number
        :Examples:
        >>> p = Player(3, 2, 0)
        >>> p.get_n() == 0
        True
        """
        return self.__n

    def __str__(self):
        """ Convert the player into a string which can be printed to the grid

        :return: (str) the string corresponding to the player
        :Examples:
        >>> p = Player(1, 2, 3)
        >>> str(p)
        '3'
        >>> p = Player(2, 2, 0)
        >>> str(p)
        '0'
        """
        return str(self.__n)

    def __repr__(self):
        """ Convert the player into a human readable text to represent it

        :return: (str) a human readable string
        :Examples:
        >>> p = Player(2, 2, 6)
        >>> p
        Player 6
        >>> p = Player(2, 2, 0)
        >>> p
        Player 0
        """
        return "Player {}".format(self.__n)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
