from main import generate_maze, print_maze
from exports import export_maze_to_json

def check_maze(maze_size: int = 1):
    maze, w, h = generate_maze(maze_size)
    print_maze(maze, w, h)

    export_maze_to_json(maze, w, h, filename="maze2.json")

check_maze()
