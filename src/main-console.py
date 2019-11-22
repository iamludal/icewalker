from Game import Game, GameState


def main():
    """ main function of this module
    """
    try:
        filename = sys.argv[0]
    except IndexError:
        exit("You must provide a filename.")

    game = Game(filename)

    while game.get_state() != GameState.winning:
        print(game)
        game.play()

    exit("You win!")


if __name__ == "__main__":
    import sys
    sys.argv.pop(0)
    main()
