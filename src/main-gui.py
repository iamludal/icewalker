from Game import Game, GameState
import pygame
from json.decoder import JSONDecodeError


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


def render_final_cell(win, color, x, y):
    pygame.draw.rect(win, color,
                    (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))


def render_wall(win, color, direction, x, y):

    if direction == 'S':
        width = CELL_SIZE
        height = BORDER
        x = x*CELL_SIZE
        y = (y+1)*CELL_SIZE

    elif direction == 'E':
        width = BORDER
        height = CELL_SIZE
        x = (x+1)*CELL_SIZE
        y = y*CELL_SIZE
        
    pygame.draw.rect(win, color, (x, y, width, height))


def render_player(win, player):
    x, y = player.get_coordinates()
    win.blit(IMG[player.get_n()],
            (x*CELL_SIZE + BORDER, y*CELL_SIZE + BORDER))

def draw_main_surface(win, color, dimensions):
    width, height = dimensions

    pygame.draw.rect(win, color, (BORDER, BORDER,
                                  width*CELL_SIZE - BORDER*2,
                                  height*CELL_SIZE - BORDER*2))

def get_corresponding_player(grid, pos):
    mouse_x, mouse_y = pos
    x, y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
    cell = grid.get_cell(x, y)

    if not cell.is_empty():
        return cell.get_content().get_n()


def render(win, grid):
    """ Render the grid [grid] of the game in the pygame window [win]

    :param win: (pygame.Surface) the pygame window in which you render the grid
    :param grid: (Grid) the gruid to render
    :UC: None
    """
    width, height = grid.get_width(), grid.get_height()

    draw_main_surface(win, WHITE, (width, height))

    for x in range(width):
        for y in range(height):
            cell = grid.get_cell(x, y)
            walls = cell.get_walls()

            if cell.is_final_cell():
                render_final_cell(win, CYAN, x, y)

            if not cell.is_empty():
                player = cell.get_content()
                render_player(win, player)   

            for wall in walls:
                render_wall(win, BLACK, wall, x, y)


def load_file(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        exit("The file doesn't exist.")
    except JSONDecodeError:
        exit("The file couldn't be decoded.")


if __name__ == "__main__":
    import sys
    import json
    sys.argv.pop(0)
    pygame.init()

    if len(sys.argv) >= 1:
        filename = sys.argv[0]
        data = load_file(filename)
    else:
        exit("You should enter a filename")

    width, height = data['dimensions']['width'], data['dimensions']['height']
    x, y = data["players"]["main"]

    g = Game(filename)
    grid = g.get_grid()
    win = pygame.display.set_mode((width*CELL_SIZE, height*CELL_SIZE))
    number = 0  # default selected player

    while True:
        # proceed events
        for event in pygame.event.get():
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                number = get_corresponding_player(grid, pos)

            elif event.type == pygame.KEYUP:
                if event.key in KEY_DIRECTIONS:
                    g.next_step(number, KEY_DIRECTIONS[event.key])

                    if g.get_state() == GameState.winning:
                        exit("You win!")

            elif event.type == pygame.QUIT:
                pygame.quit()

        win.fill(BLACK)
        render(win, grid)
        pygame.display.update()
