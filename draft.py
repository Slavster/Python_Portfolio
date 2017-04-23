## Global functions and such
import os
import random
import sys
from operator import itemgetter

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

## Define list of players, this should run first
def player_add_instructions():
    clear()
    print("Type the name of the player you wish to add to the draft")
    print("""
Enter 'DONE' when all players are in.
Enter 'HELP' to show this message again.
Enter 'REMOVE' to delete a player from the list.
""")

def show_players():
    print("Here is the current list of players")
    print(players)

def remove_player():
    whom_to_remove = input("Which player should be removed?\n> ")
    try:
        players.remove(whom_to_remove)
    except ValueError:
        clear()
        print("{} is not a player...\n"
              "".format(whom_to_remove))

players = []
player_select = 1
player_add_instructions()

while player_select == 1:
    new_player = input("> ")

    if new_player.upper() == 'DONE' or new_player.upper() == 'QUIT':
        player_select = 0
        break
    elif new_player.upper() == 'HELP':
        player_add_instructions()
        continue
    elif new_player.upper() == 'REMOVE':
        remove_player()
    else:
        players.append(new_player)

    show_players()

## Assign a random number to each player
def randomizer(players):
    random_list = list(random.sample(range(1, 100),len(players)))
    rand_player = dict(zip(players,random_list))
    ## Get a sorted list of Tuples for player order
    rand_player_tuple = rand_player.items()
    final_rand_player = sorted(rand_player_tuple,key=itemgetter(1), reverse = True)
    print("Here is the choose order for each player this round:")
    print(final_rand_player)
    rand_player = None

## Get list of teams
def set_teams(z):
    try:
        file = open(z)
    except IOError:
        print("Unable to form a list of teams, exiting the game. :(")
        sys.exit()
    else:
        global teams
        teams = list(file.read().split('\n'))
        file.close()
## specifying round 1
z = 'tier_5_teams.txt'
set_teams(z)

## Assigning teams to players
player_teams = dict.fromkeys(players,)
x = player_teams
y = teams
bonus_round = []

def team_assign(x,y):
    picking = input("Which player is choosing a team?\n> ")
    if picking not in players:
        clear()
        print("{} is not a player...\n"
              "".format(picking))
    else:
        print("Here are the teams still available:")
        print(y)
        chosen_team = input("Which team would you like to pick? ")
        if chosen_team.upper() == 'DONE':
            clear()
            print("Here are the teams chosen by each player so far:")
            print(x)
        else:
            clear()
            try:
                y.remove(chosen_team)
            except ValueError:
                clear()
                print("{} is not a team...\n"
                      "".format(chosen_team))
            else:
                x[picking] = chosen_team
                print("Here are the teams chosen by each player so far:")
                print(x)

randomizer(players)
for player in players:
    team_assign(x,y)
bonus_round.extend(y)

round_counter = 2
## Choose teams for round 2
z = 'tier_4_teams.txt'
set_teams(z)
player_teams_2 = dict.fromkeys(players,)
x = player_teams_2
y = teams

print("Round {} begins now!!!".format(round_counter))
randomizer(players)
for player in players:
    team_assign(x,y)
bonus_round.extend(y)
round_counter += 1

## Choose teams for round 3
z = 'tier_3_teams.txt'
set_teams(z)
player_teams_3 = dict.fromkeys(players,)
x = player_teams_3
y = teams

print("Round {} begins now!!!".format(round_counter))
randomizer(players)
for player in players:
    team_assign(x,y)
bonus_round.extend(y)
round_counter += 1

## Choose teams for round 4
z = 'tier_2_teams.txt'
set_teams(z)
player_teams_4 = dict.fromkeys(players,)
x = player_teams_4
y = teams

print("Round {} begins now!!!".format(round_counter))
randomizer(players)
for player in players:
    team_assign(x,y)
bonus_round.extend(y)
round_counter += 1

## Choose teams for round 5
z = 'tier_1_teams.txt'
set_teams(z)
player_teams_5 = dict.fromkeys(players,)
x = player_teams_5
y = teams

print("Round {} begins now!!!".format(round_counter))
randomizer(players)
for player in players:
    team_assign(x,y)
bonus_round.extend(y)

## Choose teans for the bonus round
player_teams_6 = dict.fromkeys(players,)
x = player_teams_6
y = bonus_round

print("Bonus round begins now!!!")
randomizer(players)
for player in players:
    team_assign(x,y)

print("Alright sports fans, here are all of the players and their teams this year:")
 