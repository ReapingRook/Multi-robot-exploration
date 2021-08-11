import pygame, sys
import random


class cell:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.color = c

        self.occupied = 0
        self.visited = 0

        self.Frontier = 0


class robot:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y

        self.color = c

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


def get_tile_color(tile_contents):
    tile_color = BLACK
    if tile_contents == "w":
        tile_color = BROWN
    if tile_contents == ".":
        tile_color = LIGHT_GREY

    return tile_color


def create_environment(surface, map_tiles):
    for j, tile in enumerate(map_tiles):
        for i, tile_contents in enumerate(tile):

            Cells.append(cell(i, j, get_tile_color(tile_contents)))

            block = pygame.Rect(i*BLOCK_W, j*BLOCK_H, BLOCK_W, BLOCK_H)
            pygame.draw.rect(surface, get_tile_color(tile_contents), block)

    for i in range(NUMBER_OF_BLOCKS_WIDE):
        new_h = round(i * BLOCK_H)
        new_w = round(i * BLOCK_W)
        pygame.draw.line(surface, BLACK, (0, new_h), (SCREEN_W, new_h), 2)
        pygame.draw.line(surface, BLACK, (new_w, 0), (new_w, SCREEN_H), 2)

def check_if_wall(x, y):
    wall_check = False

    for i in range(len(Cells)):
        if x == Cells[i].x and y == Cells[i].y and Cells[i].color == BROWN:
            wall_check == True

    return wall_check

def add_robots(surface, robot_num):

    rand_x = random.randint(1, 39)
    rand_y = random.randint(1, 39)

    for i in range(robot_num):
        wall_check = True

        if i == 0:
            while wall_check == True:
                wall_check = check_if_wall(rand_x, rand_y)

                if wall_check == True:
                    rand_x = random.randint(1, 39)
                    rand_y = random.randint(1, 39)

            robots.append(robot(rand_x, rand_y, RED))

        elif i == 1:

            while wall_check == True:
                rand_x += 1

                wall_check = check_if_wall(rand_x, rand_y)

                if wall_check == True:
                    rand_x += 1

            robots.append(robot(rand_x, rand_y, RED))
        elif i == 2:
            while wall_check == True:
                rand_x += 1

                wall_check = check_if_wall(rand_x, rand_y)

                if wall_check == True:
                    rand_x += 1

            robots.append(robot(rand_x, rand_y, RED))
        elif i == 3:
            while wall_check == True:
                rand_x += 1

                wall_check = check_if_wall(rand_x, rand_y)

                if wall_check == True:
                    rand_x += 1

            robots.append(robot(rand_x, rand_y, RED))
        elif i == 4:
            while wall_check == True:
                rand_x += 1

                wall_check = check_if_wall(rand_x, rand_y)

                if wall_check == True:
                    rand_x += 1

            robots.append(robot(rand_x, rand_y, RED))

    for f in range(len(robots)):
        for e in range(len(Cells)):
            if robots[f].x == Cells[e].x and robots[f].y == Cells[e].y:
                Cells[e].occupied = 1
                Cells[e].visited = 1
        testr = pygame.Rect(robots[f].x * BLOCK_W, robots[f].y * BLOCK_H,
                            BLOCK_W, BLOCK_H)
        pygame.draw.rect(surface, robots[f].color, testr)

    for e in range(len(Cells)):
        if Cells[e].occupied == 1:

            for l in range(len(movement)):
                add_to_frontier(Cells[e], movement[l])


def add_to_frontier(cell_temp, m):
    x, y = movement_converter(cell_temp.x, cell_temp.y, m)

    for n in range(len(Cells)):
        if x == Cells[n].x and y == Cells[n].y and Cells[n].visited == 0 and Cells[n].Frontier == 0 and Cells[n].color != BROWN:
            Cells[n].Frontier = 1


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def movement_converter(x, y, m):

    if m == "N":
        y = y + 1
    elif m == "NE":
        x = x + 1
        y = y + 1
    elif m == "E":
        x = x + 1
    elif m == "SE":
        x = x + 1
        y = y - 1
    elif m == "S":
        y = y - 1
    elif m == "SW":
        x = x - 1
        y = y - 1
    elif m == "W":
        x = x - 1
    elif m == "NW":
        x = x - 1
        y = y + 1

    new_point = (x, y)

    return new_point


def utility_function(config_c):
    temp_points = (0,0)

    total_score = 0

    for i in range(len(robots)):
        limit_check = 0

        temp_points = movement_converter(robots[i].x, robots[i].y, config_c[i])

        temp_x, temp_y = temp_points
        temp_cell = Cells[i]

        Frontier_Cells = []

        for j in range(len(Cells)):
            if temp_x == Cells[j].x and temp_y == Cells[j].y:
                temp_cell = Cells[j]

        if temp_cell.color == BROWN or temp_cell.occupied == 1:
            total_score += -10000000
        else:
            for k in range(len(robots)):
                if limit_check == 0:
                    if manhattan_distance(temp_x, temp_y, robots[k].x, robots[k].y) > limit:
                        total_score += -10000000
                        limit_check = 1

            if limit_check != 1:

                for z in range(len(Cells)):
                    if Cells[z].Frontier == 1:
                        Frontier_Cells.append(Cells[z])
                if len(Frontier_Cells) != 0:
                    least = manhattan_distance(temp_x, temp_y, Frontier_Cells[0].x, Frontier_Cells[0].y)
                    for j in range(len(Frontier_Cells)):
                        if manhattan_distance(temp_x, temp_y, Frontier_Cells[j].x, Frontier_Cells[j].y) < least:
                            least = manhattan_distance(temp_x, temp_y, Frontier_Cells[j].x, Frontier_Cells[j].y)

                    total_score += -1 * least

    return total_score


def test_search(surface):
    t = 0
    T = 150000

    while t < T:
        cfg_max = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.event.get()

        limit_checker = 0

        pop = []
        k = random.randint(0, 50)

        for i in range(k):
            cfg_c = []
            for j in range(len(robots)):
                m = random.randint(0, 8)
                cfg_c.append(movement[m])
            pop.append(cfg_c)

        cfg_max = cfg_c

        for u in range(k):
            if utility_function(pop[u]) >= utility_function(cfg_max):
                cfg_max = pop[u]

        for v in range(len(robots)):
            temp_points = movement_converter(robots[v].x, robots[v].y, cfg_max[v])

            temp_x, temp_y = temp_points
            temp_cell = Cells[v]

            for e in range(len(Cells)):
                if temp_x == Cells[e].x and temp_y == Cells[e].y:
                    temp_cell = Cells[e]

            if temp_cell.color != BROWN:
                if temp_cell.occupied != 1:

                    for z in range(len(robots)):
                        if robots[v].x == robots[z].x and robots[v].y == robots[z].y:
                            continue
                        elif manhattan_distance(temp_x, temp_y, robots[z].x, robots[z].y) > limit:
                            limit_checker = 1
                        else:
                            limit_checker = 0

                    if limit_checker != 1:
                        for q in range(len(Cells)):
                            if robots[v].x == Cells[q].x and robots[v].y == Cells[q].y:
                                Cells[q].occupied = 0

                            if temp_x == Cells[q].x and temp_y == Cells[q].y:
                                Cells[q].occupied = 1
                                Cells[q].visited = 1
                                Cells[q].Frontier = 0

                                for l in range(len(movement)):
                                    add_to_frontier(Cells[q], movement[l])

                        testr = pygame.Rect(robots[v].x * BLOCK_W,
                                            robots[v].y * BLOCK_H,
                                            BLOCK_W, BLOCK_H)
                        pygame.draw.rect(surface, GREEN, testr)

                        robots[v].update_position(temp_x, temp_y)

                        testr2 = pygame.Rect(robots[v].x * BLOCK_W, robots[v].y * BLOCK_H,
                                            BLOCK_W, BLOCK_H)
                        pygame.draw.rect(surface, robots[v].color, testr2)

                        for i in range(NUMBER_OF_BLOCKS_WIDE):
                            new_h = round(i * BLOCK_H)
                            new_w = round(i * BLOCK_W)
                            pygame.draw.line(surface, BLACK, (0, new_h), (SCREEN_W, new_h), 2)
                            pygame.draw.line(surface, BLACK, (new_w, 0), (new_w, SCREEN_H), 2)

                        pygame.display.update()

        t = t + 1


def game_loop(surface, environment_layout, robot_num):
    create_environment(surface, environment_layout)
    add_robots(surface, robot_num)
    pygame.display.flip()
    test_search(surface)


def initialize_game():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.DOUBLEBUF, 8)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    clock.tick(300)
    surface.set_alpha(None)

    surface.fill(LIGHT_GREY)
    return surface


def get_environment(file):
    with open(file, 'r') as f:
        environment_layout = f.readlines()
    environment_layout = [line.strip() for line in environment_layout]
    return environment_layout


def main():

    global limit
    global robots
    global Cells

    again = "Y"
    while again == "Y" or again == "y":
        robots = []
        Cells = []

        environment_choice = input("Choose Environment 1 or 2: ")

        while environment_choice != "1" and environment_choice != "2":
            print(f'Incorrect input:  {environment_choice}')

            environment_choice = input("Choose Environment 1 or 2: ")

        environment_choice = int(environment_choice)
        robot_num = input("Enter the amount of robots (3,4,5): ")

        while robot_num != "3" and robot_num != "4" and robot_num != "5":
            print(f'Incorrect input: {robot_num}')

            robot_num = input("Enter the amount of robots (3,4,5): ")

        robot_num = int(robot_num)
        limit = input("Enter the range of communication for the robots: ")

        while not limit.isdigit():
            print(f'Incorrect input not a number: {limit}')

            limit = input("Enter the range of communication for the robots: ")

        limit = int(limit)

        if environment_choice == 1:
            environment_layout = get_environment(ENVIRONMENT_1)
        elif environment_choice == 2:
            environment_layout = get_environment(ENVIRONMENT_2)

        surface = initialize_game()
        game_loop(surface, environment_layout, robot_num)

        again = input("Run the program again (Type Y for Yes)? ")

    sys.exit()


if __name__=="__main__":
    SCREEN_W = 800
    SCREEN_H = 800
    BLACK = (0, 0, 0)
    LIGHT_GREY = (210, 210, 210)
    BROWN = (102, 51, 0)
    PALE_YELLOW = (255, 255, 150)
    RED = (255, 0, 0)
    BLUE = (55, 55, 255)
    GREEN = (53, 252, 3)
    ORANGE = (255, 140, 0)
    PURPLE = (235, 52, 229)
    NUMBER_OF_BLOCKS_WIDE = 50
    NUMBER_OF_BLOCKS_HIGH = 50
    BLOCK_H = round(SCREEN_H / NUMBER_OF_BLOCKS_HIGH)
    BLOCK_W = round(SCREEN_W / NUMBER_OF_BLOCKS_WIDE)
    ENVIRONMENT_TEST = "testmap.txt"
    ENVIRONMENT_1 = "map.txt"
    ENVIRONMENT_2 = "map2.txt"
    TITLE = "I'm Working"

    Cells = []
    movement = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "R"]
    robots = []
    limit = 6

    main()