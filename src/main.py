from Game import Game, GameState
import pygame


# Constants declarations
CELL_SIZE = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER = 4
CYAN = (175, 240, 240)
GRAY = (50, 180, 180)
LEO = pygame.image.load("../images/weinberg.png")
NOE = pygame.image.load("../images/noe.png")
EW = pygame.image.load("../images/ew.png")
MEFT = pygame.image.load("../images/meftali.png")
LEO = pygame.transform.scale(LEO, (CELL_SIZE, CELL_SIZE))
NOE = pygame.transform.scale(NOE, (CELL_SIZE, CELL_SIZE))
EW = pygame.transform.scale(EW, (CELL_SIZE, CELL_SIZE))
MEFT = pygame.transform.scale(MEFT, (CELL_SIZE, CELL_SIZE))
PROF = ["E. Wegrzynowski", "L. Noé", "L. Weinberg", "S. Meftali"]
IMG = [EW, NOE, LEO, MEFT]
KEY_DIRECTIONS = {273: 'N', 274: 'S', 275: 'E', 276: 'W'}


def render(grid, win):
    """ Render the grid [grid] of the game in the pygame window [win]

    :param grid: (Grid) the gruid to render
    :param win: (pygame.Surface) the pygame window in which you render the grid
    :UC: None
    """
    width, height = grid.get_width(), grid.get_height()

    pygame.draw.rect(win, WHITE, (BORDER, BORDER,
                                  width*CELL_SIZE - BORDER*2,
                                  height*CELL_SIZE - BORDER*2))

    for x in range(width):
        for y in range(height):

            walls = grid.get_cell(x, y).get_walls()

            if grid.get_cell(x, y).is_final_cell():
                pygame.draw.rect(win, CYAN, (x*CELL_SIZE, y*CELL_SIZE,
                                             CELL_SIZE, CELL_SIZE))

            if not grid.get_cell(x, y).is_empty():
                player = grid.get_cell(x, y).get_content()
                win.blit(IMG[player.get_n()], (x*CELL_SIZE + BORDER,
                                               y*CELL_SIZE + BORDER))

            if 'E' in walls:
                pygame.draw.rect(
                    win, BLACK, ((x+1)*CELL_SIZE - BORDER/2, y*CELL_SIZE,
                                 BORDER, CELL_SIZE))

            if 'S' in walls:
                pygame.draw.rect(win, BLACK, (x*CELL_SIZE,
                                              (y+1)*CELL_SIZE - BORDER/2,
                                              CELL_SIZE, BORDER))


if __name__ == "__main__":
    import sys
    import json
    sys.argv.pop(0)
    pygame.init()

    try:
        filename = sys.argv[0]

        with open(filename) as f:
            data = json.load(f)
    except IndexError:
        exit("You must enter a filename")
    except FileNotFoundError:
        exit("The file doesn't exist")

    width, height = data['dimensions']['width'], data['dimensions']['height']
    x, y = data["players"]["main"]

    g = Game(filename)
    win = pygame.display.set_mode((width*CELL_SIZE, height*CELL_SIZE))
    number = 0  # default selected player

    while True:
        ev = pygame.event.get()
        # proceed events
        for event in ev:
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                x, y = x // CELL_SIZE, y // CELL_SIZE
                cell = g.get_grid().get_cell(x, y)

                if not cell.is_empty():
                    number = cell.get_content().get_n()

            elif event.type == pygame.KEYUP:
                if event.key in KEY_DIRECTIONS:
                    g.next_step(number, KEY_DIRECTIONS[event.key])

                    if g.get_state() == GameState.winning:
                        exit("You win!")

            elif event.type == pygame.QUIT:
                pygame.quit()

        win.fill(BLACK)
        render(g.get_grid(), win)
        pygame.display.update()
