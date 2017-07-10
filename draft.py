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

def show_players(players):
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

## players is used in a bunch of fuctions; figure out a way to move out of global, current hangup is Main function
def player_define():
    players = []
    player_select = 1
    player_add_instructions()

    while player_select == 1:
        new_player = input("> ")
        if new_player.upper() == 'DONE' or new_player.upper() == 'QUIT':
            player_select = 0
            return players
        elif new_player.upper() == 'HELP':
            player_add_instructions()
            continue
        elif new_player.upper() == 'REMOVE':
            remove_player()
        else:
            players.append(new_player)

        show_players(players)

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

## Get list of teams from a file
def set_teams(tier_file):
    try:
        file = open(tier_file)
    except IOError:
        print("Unable to form a list of teams, exiting the game. :(")
        sys.exit()
    else:
        teams = list(file.read().split('\n'))
        file.close()
        return teams

# Ensures each player has chosen a valid team
def team_assign(player_teams,teams,players):
    player_counter = len(players)
    while player_counter > 1:
        picking = input("Which player is choosing a team?\n> ")
        if picking not in players:
            clear()
            print("{} is not a player...\n"
                  "".format(picking))
        else:
            print("\n Here are the teams still available:")
            print(teams)
            chosen_team = input("Which team would you like to pick? ")
            clear()
            try:
                teams.remove(chosen_team)
            except ValueError:
                clear()
                print("{} is not a team...\n"
                      "".format(chosen_team))
            else:
                player_teams[picking] = chosen_team
                print("Here are the teams chosen by each player so far:")
                print(player_teams)
                player_counter -= 1

## Create user friendly DataFrame for export
def exporter (player_teams):
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

# Iterates through each round/tier to produce a dictionary that holds a player's name and their chosen team
def main():
    players = player_define()
    rounds_to_tier = {x+1: NUM_ROUNDS-x-1 for x in range(0,NUM_ROUNDS)}
    # create a dict so that highest tier teams are chosen last and lowest tiers first  -> {1: 5, 2: 4, 3: 2... etc}
    player_teams = {}
    bonus_round = []

    for ROUND, tier in rounds_to_tier.items():
        if ROUND == 6:
            pass
        ## define the list of teams to be used for a particular round
        else:
            tier_file = 'tier_{}_teams.txt'.format(tier)
            teams = set_teams(tier_file)
        player_teams[ROUND] = dict.fromkeys(players,)
        # create a dict -> {player1:None,player2:None.... etc}, teams assigned to 'None' later

        if ROUND == 6:
            print("Bonus round begins now, choose one team from any that have not been chosen yet!")
        else:
            print("Round {} begins now!!!".format(ROUND))
        randomizer(players)

        for player in players:
            if ROUND == 6:
                team_assign(player_teams[ROUND], bonus_round, players)
            else:
                team_assign(player_teams[ROUND], teams, players)
        if ROUND == 6:
            break
        else:
            bonus_round.extend(teams)

    exporter(player_teams)

NUM_ROUNDS = 6
main()
