from Game import Game


def usage():
    print("To play ice walker, type in the following command:")
    print("                                                  ")
    print("    $ python3 main-console.py [filename]          ")
    print("                                                  ")
    print("where [filename] is the path of the configuration ")
    print("                                                  ")
    print("Example:                                          ")
    print("    $ python3 main-console.py ../data/grid1.json  ")
    print("                                                  ")
    exit()


def main():
    """ main function of this module
    """
    try:
        filename = sys.argv[1]
    except IndexError:
        usage()

    game = Game.from_file(filename)

    while not (game.winning() or game.losing()):
        print(game)
        game.play()

    if game.winning():
        exit("You win!")
    elif game.losing():
        exit("You lose!")


if __name__ == "__main__":
    import sys
    main()
