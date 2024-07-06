import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600

black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pac-Man")

pacman_size = 50
pacman_x = screen_width // 2
pacman_y = screen_height // 2
pacman_speed = 5

ghost_size = 50
ghost_speed = 3
ghosts = []
for _ in range(4):
    ghost_x = random.randint(0, screen_width - ghost_size)
    ghost_y = random.randint(0, screen_height - ghost_size)
    ghosts.append([ghost_x, ghost_y])

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

    pygame.draw.circle(screen, yellow, (pacman_x, pacman_y), pacman_size // 2)

    for ghost in ghosts:
        pygame.draw.rect(screen, blue, (ghost[0], ghost[1], ghost_size, ghost_size))

    pygame.display.flip()
    clock.tick(30)
