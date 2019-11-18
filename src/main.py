from Game import Game
import pygame


CELL_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER = 4
CYAN = (175, 240, 240)
GRAY = (50, 180, 180)
RADIUS = CELL_SIZE // 3

def render(grid, win):
    width, height = grid.get_width(), grid.get_height()

    pygame.draw.rect(win, WHITE, (BORDER, BORDER, width*CELL_SIZE - BORDER*2,
                                                height*CELL_SIZE - BORDER*2))

    for x in range(width):
        for y in range(height):
            
            walls = grid.get_cell(x, y).get_walls()

            if grid.get_cell(x, y).is_final_cell():
                pygame.draw.rect(win, CYAN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

            if not grid.get_cell(x, y).is_empty():
                pygame.draw.circle(win, GRAY, (x*CELL_SIZE + CELL_SIZE//2, y*CELL_SIZE + CELL_SIZE//2), RADIUS)

            if 'E' in walls:
                pygame.draw.rect(win, BLACK, ((x+1)*CELL_SIZE - BORDER/2, y*CELL_SIZE, BORDER, CELL_SIZE))

            if 'S' in walls:
                pygame.draw.rect(win, BLACK, (x*CELL_SIZE, (y+1)*CELL_SIZE - BORDER/2, CELL_SIZE, BORDER))


            # x_bis = CELL_SIZE*y + MARGIN*y
            # y_bis = CELL_SIZE*x + MARGIN*x
            # pygame.draw.rect(win, , (x_bis, y_bis, CELL_SIZE, CELL_SIZE))



if __name__ == "__main__":
    import sys, json
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

    g = Game(filename)
    win = pygame.display.set_mode((width*CELL_SIZE, height*CELL_SIZE))
    

    while True:
        pygame.time.delay(1000)  # Refresh delay (1s)
        win.fill(BLACK)
        render(g.get_grid(), win)
        pygame.display.update()
        g.play()