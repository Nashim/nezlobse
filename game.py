import numpy as np
from random import randint
from copy import deepcopy


FILES_PER_PLAYER = 10
FIGURES_PER_PLAYER = 4


EMPTY_FILE = -1
FROM_START = -1
DONT_MOVE = -2

class Game:
    def __init__(self, num_players):
        self.num_players = num_players
        self.files_in_game = self.num_players*FILES_PER_PLAYER
        self.board = EMPTY_FILE*np.ones(self.files_in_game, dtype=np.int8)
        self.start = FIGURES_PER_PLAYER*np.ones(self.num_players, dtype=np.int8)
        self.finish = np.zeros((self.num_players, FIGURES_PER_PLAYER), dtype=np.int8)
        self.initial_file = np.arange(0, self.files_in_game, FILES_PER_PLAYER)
        self.final_file = (self.initial_file-1)%self.files_in_game
        self.die = 0
        
    def reset(self):
        self.board = EMPTY_FILE*np.ones(self.files_in_game, dtype=np.int8)
        self.start = FIGURES_PER_PLAYER*np.ones(self.num_players, dtype=np.int8)
        self.finish = np.zeros((self.num_players, FIGURES_PER_PLAYER), dtype=np.int8)
        self.die = 0
        
    def return_figure(self, board, file):
        start = deepcopy(self.start)
        if board[file] >= 0:
            start[board[file]] += 1
        return start
        
    def move(self, player, figure):
        steps = self.die
        if figure == DONT_MOVE:
            return True
        elif figure == FROM_START:
            if self.start[player] == 0 or steps != 6:
                return False
            self.start = self.return_figure(self.board, self.initial_file[player])
            self.board[self.initial_file[player]] = player
            self.start[player] -= 1
        # In finish
        elif figure >= self.files_in_game:
            figure -= self.files_in_game

            if (figure > FIGURES_PER_PLAYER-1 or self.finish[player][figure] != 1 
                or figure+steps > FIGURES_PER_PLAYER-1) or self.finish[player][figure+steps] == 1:
                return False
            self.finish[player][figure] = 0
            self.finish[player][figure+steps] = 1
        elif self.board[figure] != player:
            return False
        # Move finish
        elif figure<=self.final_file[player] and figure+steps > self.final_file[player]:
            step = figure+steps - self.final_file[player] - 1
            if step > FIGURES_PER_PLAYER-1 or self.finish[player][step] == 1:
                return False
            self.board[figure] = EMPTY_FILE
            self.finish[player][step] = 1
        # Move on board
        else:
            file = (figure+steps) % self.files_in_game
            self.start = self.return_figure(self.board, file)
            self.board[file] = player
            self.board[figure] = EMPTY_FILE
        return True
            
    def throw_die(self):
        self.die = randint(1, 6)
        return self.die
    
    def check_end(self):
        for i in range(self.num_players):
            if np.all(self.finish[i] == 1):
                return i
        return -1
    
    def check_total_end(self):
        for i in range(self.num_players):
            if np.any(self.finish[i] == 0):
                return False
        return True