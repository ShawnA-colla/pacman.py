import random
import pygame
import sys

pygame.init()

# ---------------- WINDOW ----------------
width = 600
height = 600

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man")

# ---------------- GRID ----------------
rows = 15
col = 15

cell = min(width // col, height // rows)

# ---------------- FONT ----------------
my_font = pygame.font.SysFont("courier", 35, True)

# ---------------- TIMER ----------------
time = 10

# ---------------- MAZE ----------------
maze = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,1,1,1,1,1,1,1,1,1,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
[1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
[1,0,1,0,0,0,0,0,0,0,1,0,0,0,1],
[1,0,1,1,1,1,1,1,1,0,1,1,1,0,1],
[1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
[1,0,1,1,1,0,1,1,1,0,1,0,1,0,1],
[1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
[1,0,1,0,1,0,1,1,1,0,1,1,1,0,1],
[1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
[1,1,1,0,1,0,1,0,1,1,1,0,1,0,1],
[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# ---------------- PACMAN ----------------
pac_row = 1
pac_col = 1

dx = 0
dy = 0

# ---------------- GHOSTS ----------------
ghosts = [
    {"row": 3, "col": 10, "dir": (0, 1)},
    {"row": 13, "col": 1, "dir": (1, 0)}
]

clock = pygame.time.Clock()

# ---------------- MOVE CHECK ----------------
def can_move(r, c):

    if 0 <= r < rows and 0 <= c < col:

        if maze[r][c] == 0:
            return True

    return False

# ---------------- START SCREEN ----------------
def start_screen():

    waiting = True

    while waiting:

        display.fill((255, 255, 255))

        title = my_font.render("PACMAN", True, (0, 0, 0))
        info = my_font.render("Press SPACE to Start", True, (0, 0, 0))

        display.blit(title, (180, 220))
        display.blit(info, (50, 300))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    waiting = False

# ---------------- START GAME ----------------
start_screen()

# ---------------- GAME LOOP ----------------
running = True

while running:

    clock.tick(15)

    time -= 0.1
    # time=int(time)

    # ---------- EVENTS ----------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                dx = 0
                dy = -1

            elif event.key == pygame.K_RIGHT:
                dx = 0
                dy = 1

            elif event.key == pygame.K_UP:
                dx = -1
                dy = 0

            elif event.key == pygame.K_DOWN:
                dx = 1
                dy = 0

            elif event.key == pygame.K_SPACE:
                dx = 0
                dy = 0

    # ---------- MOVE PACMAN ----------
    new_r = pac_row + dx
    new_c = pac_col + dy

    if can_move(new_r, new_c):
        pac_row = new_r
        pac_col = new_c

    # ---------- MOVE GHOSTS ----------
    for ghost in ghosts:

        gr = ghost["row"]
        gc = ghost["col"]

        dr, dc = ghost["dir"]

        if can_move(gr + dr, gc + dc):

            ghost["row"] += dr
            ghost["col"] += dc

        else:

            directions = [
                (0,1),
                (0,-1),
                (1,0),
                (-1,0)
            ]

            ghost["dir"] = random.choice(directions)

    # ---------- COLLISION ----------
    for ghost in ghosts:

        if ghost["row"] == pac_row and ghost["col"] == pac_col:
            display.fill((0,0,0))
            game_over = my_font.render("GAME OVER", True, (255,0,0))

            display.blit(game_over, (190, 280))

            pygame.display.update()

            pygame.time.delay(2000)

            running = False
    if time <= 0:

        display.fill((0,0,0))

        over = my_font.render("YOU WON", True, (0,255,0))

        display.blit(over, (180,280))

        pygame.display.update()

        pygame.time.delay(2000)

        running = False
    # ---------- DRAW ----------
    display.fill((0, 0, 0))# DRAW MAZE
    for r in range(rows):

        for c in range(col):

            if maze[r][c] == 1:

                pygame.draw.rect(
                    display,
                    (0, 0, 255),
                    (c * cell, r * cell, cell, cell)
                )

    # DRAW PACMAN
    pygame.draw.circle(
        display,
        (255,255,0),
        (
            pac_col * cell + cell//2,
            pac_row * cell + cell//2
        ),
        cell//3
    )

    # DRAW GHOSTS
    for ghost in ghosts:

        pygame.draw.circle(
            display,
            (255,0,0),
            (
                ghost["col"] * cell + cell//2,
                ghost["row"] * cell + cell//2
            ),
            cell//3
        )

    # DRAW TIMER
    timer_text = my_font.render(
        f"Time: {int(time)}",
        True,
        (255,255,255),
        
    )

    display.blit(timer_text, (1, 1))

    pygame.display.update()

pygame.quit()
