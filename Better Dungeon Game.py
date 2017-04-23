import os
import random

CELLS = [(0,0), (1,0), (2,0), (3,0), (4,0),
         (0,1), (1,1), (2,1), (3,1), (4,1),
         (0,2), (1,2), (2,2), (3,2), (4,2),
         (0,3), (1,3), (2,3), (3,3), (4,3),
         (0,4), (1,4), (2,4), (3,4), (4,4)]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_locations():
    return random.sample(CELLS,3)

def move_player(player,move):
    x, y = player
    if move == "LEFT":
        x -= 1
    if move == "RIGHT":
        x += 1
    if move == "UP":
        y -= 1
    if move == "DOWN":
        y += 1
    return x, y

def move_monster(monster):
    xx, yy = monster
    default = [1,2,3,4]
    directions = default

    if xx == 0:
        directions.remove(1)
    if xx == 4:
        directions.remove(2)
    if yy == 0:
        directions.remove(3)
    if yy == 4:
        directions.remove(4)

    mmove = random.choice(directions)
    if mmove == 1:
        xx -= 1
    if mmove == 2:
        xx += 1
    if mmove == 3:
        yy -= 1
    if mmove == 4:
        yy += 1

    return xx, yy

def get_moves(player):
    moves = ["LEFT", "RIGHT", "UP", "DOWN"]
    x, y = player
    if x == 0:
        moves.remove("LEFT")
    if x == 4:
        moves.remove("RIGHT")
    if y == 0:
        moves.remove("UP")
    if y == 4:
        moves.remove("DOWN")
    return moves

def draw_map(player, monster):
    print(" _"*5)
    tile = "|{}"

    for cell in CELLS:
        x, y = cell
        if x < 4:
            line_end = ""
            if cell == player:
                output = tile.format("X")
            elif cell == monster:
                output = tile.format("&")
            else:
                output = tile.format("_")
        else:
            line_end = "\n"
            if cell == player:
                output = tile.format("X|")
            elif cell == monster:
                output = tile.format("&|")
            else:
                output = tile.format("_|")
        print(output, end = line_end)

def game_loop():
    monster, door, player = get_locations()
    playing = True

    while playing:
        clear_screen()
        draw_map(player, monster)
        valid_moves = get_moves(player)

        print("You're currently in room {}".format(player))
        print("You can move {}.".format(", ".join(valid_moves)))
        print("Enter QUIT to give up.")

        move = input("> ")
        move = move.upper()

        if move == 'QUIT':
            print("\n ** See you next time! **\n")
            break

        if move == 'DEBUG':
            print("God Mode Activated. Door is at coordinates {}".format(door))

        if move in valid_moves:
            player = move_player(player, move)
            monster = move_monster(monster)

            if player == monster or (player == monster and player == door):
                print("\n ** Oh no! The monster got you :O Better luck next time! **\n")
                playing = False
            if player == door:
                print("\n ** You escaped! Congratulations!!! **\n")
                playing = False
        else:
            input("\n ** Walls are hard, you don't want to run into them :p ** \n")
    else:
        if input("Play again? [Y/n] ").lower() != "n":
            game_loop()

clear_screen()
print("Welcome to the dungeon!!!!! (We've got fun and games!)")
print("Find the door to escape, but watch out for the roving monster.")
input("Press return to start:")
clear_screen()
game_loop()
