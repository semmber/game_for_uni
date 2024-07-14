import tkinter
import random


def move_wrap(canvas, obj, move):
    canvas.move(obj, move[0], move[1])
    x, y = canvas.coords(obj)
    if x >= 0:
        canvas.move(obj, -600, 0)
    if x + move[0] <= 600:
        canvas.move(obj, 600, 0)
    if y >= 0:
        canvas.move(obj, 0, -600)
    if y + move[1] <= 600:
        canvas.move(obj, 0, 600)


def move_towards(enemy):
    enemy_x, enemy_y = canvas.coords(enemy)
    player_x, player_y = canvas.coords(player)
    if enemy_x < player_x:
        return (step, 0)
    elif enemy_x > player_x:
        return (-step, 0)
    elif enemy_y < player_y:
        return (0, step)
    elif enemy_y > player_y:
        return (0, -step)
    else:
        return (0, 0)


def check_move():
    global stop_move
    for h in hourglass:
        if canvas.coords(player) == canvas.coords(h):
            label.config(text="Ты подобрал звезду!")
            stop_move = 6
            hourglass.remove(h)
            canvas.delete(h)
    if canvas.coords(player) == canvas.coords(exit_p):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(player) == canvas.coords(f):
            label.config(text="Проиграл!")
            master.bind("<KeyPress>", do_nothing)
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e):
            label.config(text="Тебя съели!")
            master.bind("<KeyPress>", do_nothing)



def check_positions():
    player_coords = canvas.coords(player)
    exit_coords = canvas.coords(exit_p)
    if player_coords == exit_coords:
        return False
    for fire in fires:
        fire_coords = canvas.coords(fire)
        if player_coords == fire_coords or exit_coords == fire_coords:
            return False
    for enemy in enemies:
        enemy_coords = canvas.coords(enemy)
        if player_coords == enemy_coords or exit_coords == enemy_coords:
            return False
    for enemy in enemies:
        for fire in fires:
            fire_coords = canvas.coords(fire)
            enemy_coords = canvas.coords(enemy)
            if fire_coords == enemy_coords:
                return False
    for hour in hourglass:
        hour_coords = canvas.coords(hour)
        if hour_coords == player_coords or exit_coords == hour_coords:
            return False
        for fire in fires:
            fire_coords = canvas.coords(fire)
            if fire_coords == hour_coords:
                return False
        for enemy in enemies:
            enemy_coords = canvas.coords(enemy)
            if enemy_coords == hour_coords:
                return False
    return True

def key_pressed(event):
    global stop_move
    if event.keysym == 'space':
        canvas.coords(player, (300, 300, 310, 310))
    if event.keysym == 'Up':
        move_wrap(canvas, player, (0, -step))
    if event.keysym == 'Down':
        move_wrap(canvas, player, (0, step))
    if event.keysym == 'Right':
        move_wrap(canvas, player, (step, 0))
    if event.keysym == 'Left':
        move_wrap(canvas, player, (-step, 0))
    for enemy in enemies:
        if stop_move == 0:
            direction = move_towards(enemy)
            move_wrap(canvas, enemy, direction)
        else:
            stop_move -= 1
    check_move()


def do_nothing(x):
    pass


def prepare_and_start():
    global player, exit_p, fires, enemies, hourglass, stop_move
    canvas.delete("all")
    stop_move = 0
    player_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
    exit_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
    player = canvas.create_image((player_pos[0], player_pos[1]), image=player_pic, anchor='nw')
    exit_p = canvas.create_image((exit_pos[0], exit_pos[1]), image=exit_pic, anchor='nw')
    n_fires = 4
    fires = []
    for i in range(n_fires):
        fire_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        fire = canvas.create_image((fire_pos[0], fire_pos[1]), image=fire_pic, anchor='nw')
        fires.append(fire)
    n_enemies = 2
    enemies = []
    for i in range(n_enemies):
        enemy_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        enemy = canvas.create_image((enemy_pos[0], enemy_pos[1]), image=enemy_pic, anchor='nw')
        enemies.append(enemy)
    n_hourglass = 2
    hourglass = []
    for i in range(n_hourglass):
        hour_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        hour = canvas.create_image((hour_pos[0], hour_pos[1]), image=hourglass_pic, anchor='nw')
        hourglass.append(hour)
    while not check_positions():
        prepare_and_start()
    label.config(text="Найди выход!")
    master.bind("<KeyPress>", key_pressed)


master = tkinter.Tk()
step = 60
N_X = 10
N_Y = 10
canvas = tkinter.Canvas(master, bg='#B0E0E6', width=600, height=600)
label = tkinter.Label(master, text="Найди выход")
player_pic = tkinter.PhotoImage(file="cat.gif")
enemy_pic = tkinter.PhotoImage(file="crow.gif")
exit_pic = tkinter.PhotoImage(file="exit.gif")
fire_pic = tkinter.PhotoImage(file="fire.gif")
hourglass_pic = tkinter.PhotoImage(file="hourglass.gif")
label.pack()
canvas.pack()
restart = tkinter.Button(master, text="Начать заново", command=prepare_and_start)
restart.pack()
prepare_and_start()
master.mainloop()
