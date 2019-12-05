from Game import Game


def main():
    """ main function of this module
    """
    try:
        filename = sys.argv[1]
    except IndexError:
        exit("You must provide a filename.")

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
