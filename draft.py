## Global functions and such
import os
import random
import sys
from operator import itemgetter
import pandas as pd

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
        print("\n Here are the teams still available:")
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
                      #This catch is working, but it skips a player as a result, need to fix
            else:
                x[picking] = chosen_team
                print("Here are the teams chosen by each player so far:")
                print(x)

NUM_ROUNDS = 5
rounds_to_tier = {x+1: NUM_ROUNDS-x for x in range(0,NUM_ROUNDS)} # create a dict -> {1: 5, 2: 4, 3: 2... etc}
player_teams = {}

# iterate through each round/tier in rounds_to_tier
# Define this as a function too
for ROUND, tier in rounds_to_tier.items():
    ## Choose teams for `round` with players from `tier`
    tier_file = 'tier_{}_teams.txt'.format(tier)
    set_teams(tier_file)
    player_teams[ROUND] = dict.fromkeys(players,)

    print("Round {} begins now!!!".format(ROUND))
    randomizer(players)
    for player in players:
        team_assign(player_teams[ROUND], teams)
    bonus_round.extend(teams)

## Choose teams for the bonus round
## could this be an if statement in the loop above? if last round then don't pull the normal teams list
player_teams[6] = dict.fromkeys(players,)
print("Bonus round begins now, choose one team from any that have not been chosen yet!")
randomizer(players)
for player in players:
    team_assign(player_teams[6],bonus_round)

## Crete user friendly DataFrame for export
print("\n Alright sports fans, here are all of the players and their teams this year:")
output = pd.DataFrame(player_teams)
output.columns = ['Tier {}'.format(tier) for tier, col in enumerate(output, 1)]
output.rename(columns={output.columns[-1]:'Bonus Tier'},inplace = True)
print(output)

if input("Want to save this to excel? Y/N: ").upper() == 'Y':
    output.to_excel('draft_results.xlsx')
    print("All set, check the folder below for your file.")
    cwd = os.getcwd()
    print(cwd)
else:
    print("\n Good luck this year!")
    sys.exit()
