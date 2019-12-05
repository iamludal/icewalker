from Game import Game
from queue import Queue

def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        exit("Error: you have to enter a filename")

    game = Game.from_file(filename)

    queue = Queue()
    visited = dict()
    config = game.get_grid()
    queue.put(config)
    solved = False
    visited[config] = None

    while not queue.empty() and not solved:
        config = queue.get()
        game = Game(config)

        for grid in game.moves():
            game_bis = Game(grid)

            if not grid.is_in(visited):
                if game_bis.winning():
                    solved = True
                    solution = grid

                visited[grid] = config
                queue.put(grid)

    path = list()

    if not solved:
        print("Not solvable")
        return

    while solution in visited:
        path.append(solution)
        solution = visited[solution]

    path.reverse()

    for i in range(len(path) - 1):
        comp = path[i].get_move_to(path[i+1])
        print(comp)


if __name__ == "__main__":
    import sys
    main()

