import random

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {
            'N': True, 'S': True, 'E': True, 'W': True,
            'NE': False, 'NW': False, 'SE': False, 'SW': False
        }
        self.visited = False

    def remove_wall(self, other, direction):
        self.walls[direction] = False
        opposites = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        if direction in opposites:
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

    # Add diagonal markers
    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            # Corners
            if cell.walls['N'] and cell.walls['W']:
                cell.walls['NW'] = True
            if cell.walls['N'] and cell.walls['E']:
                cell.walls['NE'] = True
            if cell.walls['S'] and cell.walls['W']:
                cell.walls['SW'] = True
            if cell.walls['S'] and cell.walls['E']:
                cell.walls['SE'] = True

            # Vertical alignment
            if in_bounds(x, y + 1, width, height):
                below = grid[x][y + 1]
                if cell.walls['S'] and below.walls['N']:
                    cell.walls['SE'] = True
                    cell.walls['SW'] = True

            # Horizontal alignment
            if in_bounds(x + 1, y, width, height):
                right = grid[x + 1][y]
                if cell.walls['E'] and right.walls['W']:
                    cell.walls['NE'] = True
                    cell.walls['SE'] = True

def generate_maze(difficulty=10):
    difficulty = max(1, min(difficulty, 100))
    size = 5 + difficulty
    width = height = size

    grid = init_grid(width, height)

    # Start carving from bottom center
    start_x = width // 2
    start_y = height - 1
    carve_passages_from(start_x, start_y, grid, width, height)

    # Open entry and exit
    grid[start_x][height - 1].walls['S'] = False
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
    level = int(input("enter the maze size: "))
    maze, w, h = generate_maze(level)
    print_maze(maze, w, h)
