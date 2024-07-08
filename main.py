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

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pac-Man")

# Pac-Man settings
pacman_size = 50
pacman_x = screen_width // 2
pacman_y = screen_height // 2
pacman_speed = 5

# Ghost settings
ghost_size = 50
ghosts = []
for _ in range(4):
    ghost_x = random.randint(0, screen_width - ghost_size)
    ghost_y = random.randint(0, screen_height - ghost_size)
    ghosts.append([ghost_x, ghost_y])

# Pellet settings
pellet_size = 10
pellets = []
for _ in range(20):
    pellet_x = random.randint(0, screen_width - pellet_size)
    pellet_y = random.randint(0, screen_height - pellet_size)
    pellets.append([pellet_x, pellet_y])

def check_collision(x1, y1, size1, x2, y2, size2):
    return x1 < x2 + size2 and x1 + size1 > x2 and y1 < y2 + size2 and y1 + size1 > y2

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        pacman_x += pacman_speed
    if keys[pygame.K_UP]:
        pacman_y -= pacman_speed
    if keys[pygame.K_DOWN]:
        pacman_y += pacman_speed

    screen.fill(black)

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
