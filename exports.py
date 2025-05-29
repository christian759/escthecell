import json
from main import generate_maze, print_maze

def export_maze_to_json(grid, width, height, filename="maze.json"):
    cells = []
    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            cells.append({
                "x": x,
                "y": y,
                "walls": cell.walls
            })
    maze_dict = {
        "width": width,
        "height": height,
        "cells": cells
    }
    with open(filename, "w") as f:
        json.dump(maze_dict, f, indent=4)
    print(f"Maze exported to {filename}")


# Inside __main__ after generating the maze
if __name__ == "__main__":
    for i in range (1, 20):
        maze, w, h = generate_maze(i)
        if i == 1:
            print_maze(maze, w, h)

        export_maze_to_json(maze, w, h, f"output_json/maze{i}.json")
    print("done")
