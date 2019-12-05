from Game import Game
from queue import Queue

def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        exit("Error: you have to enter a filename")

    game = Game(filename)

    queue = Queue()
    visited = dict()
    config = game.get_grid()
    queue.put(config)
    solved = False
    visited[config] = None

    while not queue.empty() and not solved:
        config = queue.get()

        for grid in game.moves(config):
            if grid not in visited and game.winning():
                solved = True




if __name__ == "__main__":
    import sys
    main()

