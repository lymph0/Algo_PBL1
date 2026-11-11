# -*- coding: utf-8 -*-
from collections import deque


def read_maze(filename):
    matrix = []  # 2D list to store the maze

    # Open the text file
    with open(filename, 'r', encoding='utf-8-sig') as file:

        # Read the file line by line
        for line in file:

            # Remove newline characters and surrounding spaces
            line = line.strip()

            # Skip empty lines
            if line == '':
                continue

            # Convert the string into a list of characters
            matrix.append(list(line))

    # Check if the maze is empty
    if not matrix:
        raise ValueError("The maze is empty.")

    # Check if all rows have the same length
    if any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("All rows must have the same length.")

    # Check if there is exactly one starting point
    if sum(row.count('@') for row in matrix) != 1:
        raise ValueError("There must be exactly one starting point (@).")

    # Check if there is exactly one goal
    if sum(row.count('G') for row in matrix) != 1:
        raise ValueError("There must be exactly one goal (G).")

    # Check for invalid characters
    allowed = set("#.@GabcdefABCDEF")

    if any(cell not in allowed for row in matrix for cell in row):
        raise ValueError("The maze contains invalid characters.")

    return matrix


def shortestPathAllKeys(grid):
    m, n = len(grid), len(grid[0])

    start = None
    key_mask = 0

    # Find the starting point and all keys
    for r in range(m):
        for c in range(n):
            if grid[r][c] == '@':
                start = (r, c)

            if 'a' <= grid[r][c] <= 'f':
                bit = 1 << (ord(grid[r][c]) - ord('a'))
                key_mask |= bit

    # Target state: all keys collected
    target = key_mask

    # Initialize BFS
    queue = deque([(start[0], start[1], 0, 0)])
    visited = set()
    visited.add((start[0], start[1], 0))

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        r, c, mask, dist = queue.popleft()

        # Check if all keys are collected and the goal is reached
        if grid[r][c] == 'G':
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check grid boundaries
            if not (0 <= nr < m and 0 <= nc < n):
                continue

            cell = grid[nr][nc]

            # Check wall
            if cell == '#':
                continue

            # Check lock
            if 'A' <= cell <= 'F':
                bit = 1 << (ord(cell) - ord('A'))

                if not (mask & bit):
                    continue

            # Collect key
            new_mask = mask

            if 'a' <= cell <= 'f':
                bit = 1 << (ord(cell) - ord('a'))
                new_mask |= bit

            # Check whether the state has been visited
            state = (nr, nc, new_mask)

            if state in visited:
                continue

            visited.add(state)
            queue.append((nr, nc, new_mask, dist + 1))

    # Return -1 if no valid path exists
    return -1


# Main execution
if __name__ == "__main__":

    while True:
        filename = input("Maze file name: ")

        try:
            maze = read_maze(filename)
            break

        except FileNotFoundError:
            print("File not found. Please enter the filename again.")

        except (OSError, UnicodeError, ValueError) as exc:
            print(f"Input error: {exc}")
            print("Please check the file and try again.")

    # Print the maze
    print("\nInput maze:")
    for row in maze:
        print(''.join(row))

    # Find the shortest path
    min_dist = shortestPathAllKeys(maze)

    # Print the result
    print("\nShortest distance:", min_dist)
