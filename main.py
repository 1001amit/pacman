import tkinter as tk
import random
from PIL import Image, ImageTk

cell_size = 20
screen_width = 28 * cell_size
screen_height = 24 * cell_size
black = "#000000"
pacman_size = cell_size
pacman_speed = cell_size
ghost_size = cell_size
ghost_speed = cell_size // 2
ghosts = []
pellet_size = cell_size // 2
pellets = []
wall_map = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X..........................X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X......XX....XX....XX......X",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "XXXXXX.XX          XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "X...........XXXX...........X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X...XX................XX...X",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "X......XX....XX....XX......X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

walls = []
open_paths = []
for y, row in enumerate(wall_map):
    for x, cell in enumerate(row):
        if cell == 'X':
            walls.append((x * cell_size, y * cell_size))
        else:
            open_paths.append((x * cell_size + cell_size // 2, y * cell_size + cell_size // 2))
            if cell == '.':
                pellets.append((x * cell_size + cell_size // 2, y * cell_size + cell_size // 2))

pacman_x, pacman_y = random.choice(open_paths)

for _ in range(4):
    ghost_x, ghost_y = random.choice(open_paths)
    ghost_dir = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
    ghosts.append([ghost_x, ghost_y, ghost_dir])

def check_collision(x1, y1, size1, x2, y2, size2):
    return x1 < x2 + size2 and x1 + size1 > x2 and y1 < y2 + size2 and y1 + size1 > y2

def check_wall_collision(x, y, size):
    for wall in walls:
        if check_collision(x - size // 2, y - size // 2, size, wall[0], wall[1], cell_size):
            return True
    return False

def move_pacman(event):
    global pacman_x, pacman_y
    new_x, new_y = pacman_x, pacman_y
    if event.keysym == 'Left':
        new_x -= pacman_speed
    elif event.keysym == 'Right':
        new_x += pacman_speed
    elif event.keysym == 'Up':
        new_y -= pacman_speed
    elif event.keysym == 'Down':
        new_y += pacman_speed

    if not check_wall_collision(new_x, new_y, pacman_size):
        pacman_x, pacman_y = new_x, new_y

    check_pellet_collision()
    draw()

def move_ghosts():
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

        if check_wall_collision(ghost[0], ghost[1], ghost_size):
            ghost[0], ghost[1] = original_position
            ghost[2] = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])

        if check_collision(pacman_x - pacman_size // 2, pacman_y - pacman_size // 2, pacman_size, ghost[0] - ghost_size // 2, ghost[1] - ghost_size // 2, ghost_size):
            print("Collision with ghost!")
            root.quit()

    root.after(300, move_ghosts)

def check_pellet_collision():
    global pellets
    for pellet in pellets[:]:
        if check_collision(pacman_x - pacman_size // 2, pacman_y - pacman_size // 2, pacman_size, pellet[0] - pellet_size // 2, pellet[1] - pellet_size // 2, pellet_size):
            pellets.remove(pellet)
            print("Pellet collected!")

def draw():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=background_img)
    for wall in walls:
        canvas.create_image(wall[0], wall[1], anchor=tk.NW, image=wall_img)
    canvas.create_image(pacman_x, pacman_y, anchor=tk.CENTER, image=pacman_img)
    for ghost in ghosts:
        canvas.create_image(ghost[0], ghost[1], anchor=tk.CENTER, image=ghost_img)
    for pellet in pellets:
        canvas.create_image(pellet[0], pellet[1], anchor=tk.CENTER, image=pellet_img)

root = tk.Tk()
root.title("Pac-Man")

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

background_img = ImageTk.PhotoImage(Image.open("background.png").resize((screen_width, screen_height)))
pacman_img = ImageTk.PhotoImage(Image.open("pacman.png").resize((pacman_size, pacman_size)))
ghost_img = ImageTk.PhotoImage(Image.open("ghost.png").resize((ghost_size, ghost_size)))
pellet_img = ImageTk.PhotoImage(Image.open("pellet.png").resize((pellet_size, pellet_size)))
wall_img = ImageTk.PhotoImage(Image.open("wall.png").resize((cell_size, cell_size)))

root.bind('<KeyPress>', move_pacman)

move_ghosts()
draw()

root.mainloop()
