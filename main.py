import random

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False

    def remove_wall(self, other, direction):
        self.walls[direction] = False
        opposites = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        other.walls[opposites[direction]] = False

def init_grid(width, height):
    return [[Cell(x, y) for y in range(height)] for x in range(width)]

def in_bounds(x, y, width, height):
    return 0 <= x < width and 0 <= y < height

def carve_passages_from(cx, cy, grid, width, height):
    stack = [(cx, cy)]
    while stack:
        x, y = stack[-1]
        current = grid[x][y]
        current.visited = True

        directions = [('N', (0, -1)), ('S', (0, 1)), ('E', (1, 0)), ('W', (-1, 0))]
        random.shuffle(directions)

        for direction, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny, width, height):
                neighbor = grid[nx][ny]
                if not neighbor.visited:
                    current.remove_wall(neighbor, direction)
                    stack.append((nx, ny))
                    break
        else:
            stack.pop()

def generate_maze(difficulty=10):
    difficulty = max(1, min(difficulty, 100))
    size = 5 + difficulty
    width = height = size

    grid = init_grid(width, height)

    # Start carving from bottom center
    start_x = width // 2
    start_y = height - 1
    carve_passages_from(start_x, start_y, grid, width, height)

    # Open entry at bottom center
    grid[start_x][height - 1].walls['S'] = False

    # Open exit at top center
    grid[start_x][0].walls['N'] = False

    return grid, width, height

def print_maze(grid, width, height):
    # Print top boundary line including exit gap
    top_line = " "
    for x in range(width):
        if not grid[x][0].walls['N']:
            top_line += "  "
        else:
            top_line += "_ "
    print(top_line)

    for y in range(height):
        line = "|"
        for x in range(width):
            cell = grid[x][y]
            # Floor or bottom wall
            line += " " if not cell.walls['S'] else "_"
            # East wall or open space
            line += " " if not cell.walls['E'] else "|"
        print(line)

if __name__ == "__main__":
    try:
        level = int(input("Enter difficulty (1 = easy, 10 = medium, 50 = hard): ").strip())
    except ValueError:
        level = 10
    maze, w, h = generate_maze(level)
    print_maze(maze, w, h)
