import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
grey = (169, 169, 169)

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pac-Man")

# Pac-Man settings
pacman_size = 50
pacman_x = screen_width // 2
pacman_y = screen_height // 2
pacman_speed = 5

# Ghost settings
ghost_size = 40
ghost_speed = 3
ghosts = []
for _ in range(4):
    ghost_x = random.randint(0, screen_width - ghost_size)
    ghost_y = random.randint(0, screen_height - ghost_size)
    ghost_dir = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
    ghosts.append([ghost_x, ghost_y, ghost_dir])

# Pellet settings
pellet_size = 10
pellets = []

# Define the grid size and wall map
grid_size = 40
wall_map = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "",
    "X............XX............X",
    "",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "",
    "X..........................X",
    "",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "",
    "X......XX....XX....XX......X",
    "",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "",
    "XXXXXX.XX          XX.XXXXXX",
    "",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "",
    "X...........XXXX...........X",
    "",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "",
    "X...XX................XX...X",
    "",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "",
    "X......XX....XX....XX......X",
    "",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "",
    "X..........................X",
    "",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Create walls and pellets based on wall_map
walls = []
for y, row in enumerate(wall_map):
    for x, cell in enumerate(row):
        if cell == 'X':
            walls.append(pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size))
        elif cell == '.':
            pellets.append([x * grid_size + grid_size // 2, y * grid_size + grid_size // 2])

def check_collision(x1, y1, size1, x2, y2, size2):
    return x1 < x2 + size2 and x1 + size1 > x2 and y1 < y2 + size2 and y1 + size1 > y2

def check_wall_collision(rect):
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        new_x = pacman_x - pacman_speed
        new_y = pacman_y
        if not any(wall.collidepoint(new_x - pacman_size // 2, new_y) or wall.collidepoint(new_x + pacman_size // 2, new_y) for wall in walls):
            pacman_x = new_x
    if keys[pygame.K_RIGHT]:
        new_x = pacman_x + pacman_speed
        new_y = pacman_y
        if not any(wall.collidepoint(new_x + pacman_size // 2, new_y) or wall.collidepoint(new_x - pacman_size // 2, new_y) for wall in walls):
            pacman_x = new_x
    if keys[pygame.K_UP]:
        new_x = pacman_x
        new_y = pacman_y - pacman_speed
        if not any(wall.collidepoint(new_x, new_y - pacman_size // 2) or wall.collidepoint(new_x, new_y + pacman_size // 2) for wall in walls):
            pacman_y = new_y
    if keys[pygame.K_DOWN]:
        new_x = pacman_x
        new_y = pacman_y + pacman_speed
        if not any(wall.collidepoint(new_x, new_y + pacman_size // 2) or wall.collidepoint(new_x, new_y - pacman_size // 2) for wall in walls):
            pacman_y = new_y

    # Move ghosts and check for collisions
    for ghost in ghosts:
        original_position = ghost[:2]
        
        if ghost[2] == 'LEFT':
            ghost[0] -= ghost_speed
        elif ghost[2] == 'RIGHT':
            ghost[0] += ghost_speed
        elif ghost[2] == 'UP':
            ghost[1] -= ghost_speed
        elif ghost[2] == 'DOWN':
            ghost[1] += ghost_speed

        ghost_rect = pygame.Rect(ghost[0], ghost[1], ghost_size, ghost_size)
        
        if check_wall_collision(ghost_rect):
            ghost[0], ghost[1] = original_position
            ghost[2] = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])

    screen.fill(black)

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, grey, wall)

    # Draw Pac-Man
    pygame.draw.circle(screen, yellow, (pacman_x, pacman_y), pacman_size // 2)

    # Draw ghosts
    for ghost in ghosts:
        pygame.draw.rect(screen, blue, (ghost[0], ghost[1], ghost_size, ghost_size))

    # Draw pellets
    for pellet in pellets:
        pygame.draw.circle(screen, white, (pellet[0], pellet[1]), pellet_size // 2)

    # Check for collisions with ghosts
    for ghost in ghosts:
        if check_collision(pacman_x - pacman_size // 2, pacman_y - pacman_size // 2, pacman_size, ghost[0], ghost[1], ghost_size):
            print("Collision with ghost!")
            running = False

    # Check for collisions with pellets
    for pellet in pellets[:]:
        if check_collision(pacman_x - pacman_size // 2, pacman_y - pacman_size // 2, pacman_size, pellet[0] - pellet_size // 2, pellet[1] - pellet_size // 2, pellet_size):
            pellets.remove(pellet)
            print("Pellet collected!")

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
