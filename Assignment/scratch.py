import math

XSIZE, YSIZE = 14, 14
S_RIGHT, S_LEFT, S_UP, S_DOWN = 0, 1, 2, 3
body = [[2, 1], [2, 0], [2, 2], [1, 2], [0, 2]]

food = [0, 0]


# def print_grid(grid):
#     gridWidth = len(grid)
#     gridHeight = len(grid[0])
#
#     for y in range(gridHeight):
#         for x in range(gridWidth):
#             sys.stdout.write((str(grid[x][y])))
#         sys.stdout.write('\n')


def translate_grid():
    grid = []

    for i in range(XSIZE):
        grid.append([0] * YSIZE)

    for i in body:
        grid[i[0]][i[1]] = 2

    grid.insert(0, [2] * XSIZE)
    grid.insert(YSIZE + 1, [2] * XSIZE)

    for r in grid:
        r.insert(0, 2)
        r.insert(XSIZE + 1, 2)

    return grid


def floodFill(grid, x, y, oldChar, newChar, info=None):
    if info is None:
        info = ((-1.0, -1.0), [])

    gridWidth = len(grid)
    gridHeight = len(grid[0])

    if oldChar is None:
        oldChar = grid[x][y]

    if grid[x][y] != oldChar:
        return info

    grid[x][y] = newChar
    t = info[1]
    t.append((x, y))

    val = point_difference((x, y))

    if val == 1:
        coord_next_to_head = (x, y)
        info = (coord_next_to_head, t)
    else:
        info = (info[0], t)

    if x > 0:  # left
        info = floodFill(grid, x - 1, y, oldChar, newChar, info)
    if y > 0:  # up
        info = floodFill(grid, x, y - 1, oldChar, newChar, info)
    if x < gridWidth - 1:  # right
        info = floodFill(grid, x + 1, y, oldChar, newChar, info)
    if y < gridHeight - 1:  # down
        info = floodFill(grid, x, y + 1, oldChar, newChar, info)

    return info


def point_difference(point):
    # Increment required as the grid's boundary are manually added in when processing the grid
    a = math.pow(point[0] - (body[0][0] + 1), 2)
    b = math.pow(point[1] - (body[0][1] + 1), 2)

    return math.sqrt(a + b)


direction = S_LEFT


def get_room_info(grid):
    grid_width = len(grid)
    grid_height = len(grid[0])
    rooms_found = 0
    results = []

    for x in range(grid_width):
        for y in range(grid_height):
            if grid[x][y] == 0:
                coord_next_to_head, coords = floodFill(grid, x, y, 0, 1)
                results.append((coord_next_to_head, coords))

    room_info = 0

    for ival in results:
        # Adjust to new coordinates because of manual boundary insertion
        next_point = [body[0][0] + 1, body[0][1] + 1]

        if direction == S_RIGHT:
            next_point = (next_point[0] + 1, next_point[1])
        elif direction == S_LEFT:
            next_point = (next_point[0] - 1, next_point[1])
        elif direction == S_UP:
            next_point = (next_point[0], next_point[1] - 1)
        elif direction == S_DOWN:
            next_point = (next_point[0], next_point[1] + 1)

        if next_point in ival[1] and point_difference(next_point) == 1:
            # (point closest to head, room coordinates)
            rooms_found += 1
            room_info = (ival[0], ival[1])

    return rooms_found, room_info


grid = translate_grid()
info = get_room_info(grid)

if info[0]:
    print("\nPoint closest to snake's head: %s. Room size: %s. Room big enough? %s. Room coordinates: %s" % (
    info[1][0], len(info[1][1]), (len(body) < len(info[1][1])), info[1][1]))
else:
    print("\nNo rooms found")
