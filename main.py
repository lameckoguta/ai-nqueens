import random
import pygame
import sys


# Constants
N = 8
WINDOW_SIZE = 400
CELL_SIZE = WINDOW_SIZE // N

WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
RED = (220, 20, 60)
GREEN = (50, 205, 50)


def random_state(n):
    """
    Create a random board state.
    """
    return [random.randint(0, n - 1) for _ in range(n)]


def heuristic(state):
    """
    Count attacking queen pairs.
    Lower is better.
    Goal = 0
    """
    attacks = 0
    n = len(state)

    for i in range(n):
        for j in range(i + 1, n):

            # Same row
            if state[i] == state[j]:
                attacks += 1

            # Same diagonal
            if abs(state[i] - state[j]) == abs(i - j):
                attacks += 1

    return attacks


def get_neighbors(state):
    """
    Generate all neighboring states.
    Move one queen within its column.
    """
    neighbors = []
    n = len(state)

    for col in range(n):
        current_row = state[col]

        for row in range(n):
            if row != current_row:
                neighbor = state.copy()
                neighbor[col] = row
                neighbors.append(neighbor)

    return neighbors


def hill_climb(initial_state):
    current = initial_state

    while True:
        current_h = heuristic(current)

        if current_h == 0:
            return current

        neighbors = get_neighbors(current)

        best_neighbor = current
        best_h = current_h

        for neighbor in neighbors:
            h = heuristic(neighbor)

            if h < best_h:
                best_neighbor = neighbor
                best_h = h

        # Local optimum reached
        if best_h >= current_h:
            return current

        current = best_neighbor



pygame.init()

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("N-Queens Hill Climbing")

font = pygame.font.SysFont(None, 48)


def draw_board(state):
    """
    Draw chessboard and queens.
    """
    for row in range(N):
        for col in range(N):

            color = WHITE if (row + col) % 2 == 0 else BLACK

            pygame.draw.rect(
                screen,
                color,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

    # Draw queens
    for col, row in enumerate(state):
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(
            screen,
            RED,
            (center_x, center_y),
            CELL_SIZE // 3
        )

        text = font.render("Q", True, GREEN)
        rect = text.get_rect(center=(center_x, center_y))
        screen.blit(text, rect)

    pygame.display.flip()


initial = random_state(N)

print("Initial State:", initial)
print("Initial Heuristic:", heuristic(initial))

solution = hill_climb(initial)

print("Final State:", solution)
print("Final Heuristic:", heuristic(solution))

# Visualization loop
running = True

while running:
    screen.fill((0, 0, 0))

    draw_board(solution)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()