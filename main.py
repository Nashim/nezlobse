from player import Player
from game import Game, DONT_MOVE
from copy import deepcopy
import numpy as np
import tkinter as tk
from window import Window
import time

SIMULATION = 0
SIMULATION_GAMES = 300
if not SIMULATION:
    SIMULATION_GAMES = 1

NUM_PLAYERS = 4
player_ratings = [[300, 200, 50, 50, 5],
                  [50, 300, 50, 50, 1],
                  [50, 200, 300, 50, 5],
                  [50, 200, 50, 300, 5]]

game = Game(NUM_PLAYERS)
players = []


for player in range(NUM_PLAYERS):
    players.append(Player(player, game.board, game.start, game.finish, game.initial_file, game.final_file, player_ratings[player]))

if not SIMULATION:
    window = Window(game.board, game.start, game.finish)
running = True
players_finished = np.array([0]*NUM_PLAYERS)
players_finished_sum = np.array([0]*NUM_PLAYERS)

order = 1
start_time = time.time()
for game_count in range(SIMULATION_GAMES):
    # Main game loop
    while running:
        # One round
        for player_num, player in enumerate(players):
            # Check if game is finished
            running = np.sum(players_finished != 0) < NUM_PLAYERS
            if not running:
                break

            # Check if player is finished
            if players_finished[player_num] > 0:
                continue
            
            # One player round
            while True:
                if np.all(game.finish[player_num] == 1):
                    players_finished[player_num] = order
                    order += 1
                    break
                
                if not SIMULATION:
                    ch = input()
                    if ch == "q":
                        exit()
                
                die = game.throw_die()
                play = player.play(deepcopy(game.board), deepcopy(game.start), 
                                deepcopy(game.finish), die)
                
                game.move(player_num, play)
                if not SIMULATION:
                    print("Player:", player_num+1, "Die:", die, "Play", play)
                    window.update_board(deepcopy(game.board), deepcopy(game.start), deepcopy(game.finish), die, player_num)
                
                # End round
                if die != 6 or (die == 6 and play == DONT_MOVE):
                    break
    players_finished_sum += players_finished
    game.reset()
    players_finished = np.array([0]*NUM_PLAYERS)
    order = 1
    running = True

end_time = time.time()
print("Time:", end_time-start_time, (end_time-start_time)/SIMULATION_GAMES)
print("Game finished")
print(players_finished_sum)
print(players_finished_sum/np.min(players_finished_sum))
if not SIMULATION:
    while input() != "q":
        continue         

