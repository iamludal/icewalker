
class Player:

    def __init__(self, x, y, n):

        if not isinstance(x, int):
            raise TypeError("x coordinate must be a positive integer")
        elif x < 0:
            raise ValueError("x coordinate must be a positive integer")

        if not isinstance(y, int):
            raise TypeError("y coordinate must be a positive integer")
        elif y < 0:
            raise ValueError("y coordinate must be a positive integer")

        if not isinstance(n, int):
            raise TypeError("Player number must be a positive integer")
        elif n < 0:
            raise TypeError("Player number must be a positive integer")

        self.__x = x
        self.__y = y
        self.__n = n

    def __str__(self):
        return str(self.__n)

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
