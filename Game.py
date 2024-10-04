import pygame
from collections import deque
import time

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10  # Size of the maze (10x10 grid)
TILE_SIZE = WIDTH // COLS
FPS = 5  # Adjust the FPS for slower or faster movement

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver with BFS - Simulation")

# The maze grid, 0 = open path, 1 = wall
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Start and goal positions
start = (1, 1)
goal = (1, 8)

# BFS Algorithm
def bfs(maze, start, goal):
    queue = deque([([start], start)])  # The queue stores (path, current position)
    visited = set([start])

    while queue:
        path, current = queue.popleft()

        if current == goal:
            return path

        x, y = current

        # Define movements in 4 directions: down, up, right, left
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in visited:
                queue.append((path + [(nx, ny)], (nx, ny)))
                visited.add((nx, ny))

    return None  # If no path is found

# Draw the maze grid
def draw_maze(window, maze, path, player_pos=None):
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            if maze[row][col] == 1:
                pygame.draw.rect(window, BLACK, (x, y, TILE_SIZE, TILE_SIZE))
            elif (row, col) in path:
                pygame.draw.rect(window, GREEN, (x, y, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(window, WHITE, (x, y, TILE_SIZE, TILE_SIZE))

            pygame.draw.rect(window, GRAY, (x, y, TILE_SIZE, TILE_SIZE), 1)

    # Draw the player at its current position
    if player_pos:
        px, py = player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE
        pygame.draw.rect(window, YELLOW, (px, py, TILE_SIZE, TILE_SIZE))

    # Draw the goal position
    gx, gy = goal[1] * TILE_SIZE, goal[0] * TILE_SIZE
    pygame.draw.rect(window, RED, (gx, gy, TILE_SIZE, TILE_SIZE))

# Main game loop
def main():
    clock = pygame.time.Clock()
    path = bfs(maze, start, goal)  # Get the path using BFS
    player_pos = start  # Start the player at the initial position
    path_index = 0  # Index to track the player's current step in the path

    run = True
    while run:
        clock.tick(FPS)  # Control the speed of the movement

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Move the player along the path
        if path_index < len(path):
            player_pos = path[path_index]
            path_index += 1

        # Draw the maze and the player's movement
        window.fill(WHITE)
        draw_maze(window, maze, path, player_pos)
        pygame.display.update()

        # Stop if player reached the goal
        if player_pos == goal:
            time.sleep(2)  # Wait for 2 seconds before closing the game
            run = False

    pygame.quit()

if __name__ == "__main__":
    main()
