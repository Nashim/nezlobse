import numpy as np
import tkinter as tk
SIZE = 70
EMPTY = -1
PATH = 4
RED = 0
GREEN = 1
YELLOW = 2
BLUE = 3
BOARD_SIZE = 11
COLOR_OFFSET = 5
bg_colors = ["brown", "greenyellow", "gold1", "aqua", "aliceblue", "red", "green", "yellow", "blue"]
player_str = ["red", "green", "yellow", "blue"]
class Window:
    def __init__(self, board, start, finish):
        self.board = board
        self.start = start
        self.finish = finish
        self.die = 0
        self.player = 0
        self.window_layout = EMPTY*np.ones((BOARD_SIZE, BOARD_SIZE), dtype=np.int8)
        #Path
        self.window_layout[4:7, :] = PATH
        self.window_layout[:, 4:7] = PATH
        self.window_layout[5, 5] = EMPTY
        #Home
        self.window_layout[0:2, 0:2] = RED
        self.window_layout[0:2, 9:11] = GREEN
        self.window_layout[9:11, 0:2] = BLUE
        self.window_layout[9:11, 9:11] = YELLOW
        self.home_indices = np.array([[[0, 0], [0, 1], [1, 0], [1, 1]], 
                                [[0, 9], [0, 10], [1, 9], [1, 10]], 
                                [[9, 9], [9, 10], [10, 9], [10, 10]],
                                [[9, 0], [9, 1], [10, 0], [10, 1]]])

        #Finish
        self.window_layout[5, 1:5] = RED
        self.window_layout[1:5, 5] = GREEN
        self.window_layout[5, 6:10] = YELLOW
        self.window_layout[6:10, 5] = BLUE
        self.finish_indices =np.array([[[5, 1], [5, 2], [5, 3], [5, 4]], [[1, 5], [2, 5], [3, 5], [4, 5]], 
                                [[5, 9], [5, 8], [5, 7], [5, 6]], [[9, 5], [8, 5], [7, 5], [6, 5]]])
        self.path_indices = np.array([[4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [3, 4], [2, 4], [1, 4], [0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [3, 6], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10], [5, 10], [6, 10], [6, 9], [6, 8], [6, 7], [6, 6], [7, 6], [8, 6], [9, 6], [10, 6], [10, 5], [10, 4], [9, 4], [8, 4], [7, 4], [6, 4], [6, 3], [6, 2], [6, 1], [6, 0], [5, 0]])

        #Start
        self.window_layout[4, 0] = RED
        self.window_layout[0, 6] = GREEN
        self.window_layout[6, 10] = YELLOW
        self.window_layout[10, 4] = BLUE

        #print(self.window_layout)

        self.window = tk.Tk()
        self.frames = [[0 for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE+1)] 
        self.draw()

    def update_board(self, board, start, finish, die, player):
        board_change = np.where(self.board != board)
        start_change = np.where(self.start != start)
        finish_change = np.where(self.finish != finish)
        self.board = board
        self.start = start
        self.finish = finish
        self.die = die
        self.player = player
        if len(start_change[0]) > 0:
            for player in start_change[0]:
                for at_home in range(4):
                    if start[player] > at_home:
                        self.window_layout[self.home_indices[player, at_home, 0], self.home_indices[player, at_home, 1]] = player + COLOR_OFFSET
                    else:
                        self.window_layout[self.home_indices[player, at_home, 0], self.home_indices[player, at_home, 1]] = player
        if len(finish_change[0]) > 0:
            for [player, figure] in zip(finish_change[0], finish_change[1]):
                if finish[player, figure] == 1:
                    self.window_layout[self.finish_indices[player, figure, 0], self.finish_indices[player, figure, 1]] = player + COLOR_OFFSET
                else:
                    self.window_layout[self.finish_indices[player, figure, 0], self.finish_indices[player, figure, 1]] = player
        if len(board_change[0]) > 0:
            for file_idx in board_change[0]:
                if board[file_idx] == EMPTY:
                    self.window_layout[self.path_indices[file_idx, 0], self.path_indices[file_idx, 1]] = PATH
                    if file_idx == 0:
                        self.window_layout[self.path_indices[file_idx, 0], self.path_indices[file_idx, 1]] = RED
                    elif file_idx == 10:
                        self.window_layout[self.path_indices[file_idx, 0], self.path_indices[file_idx, 1]] = GREEN
                    elif file_idx == 20:
                        self.window_layout[self.path_indices[file_idx, 0], self.path_indices[file_idx, 1]] = YELLOW
                    elif file_idx == 30:
                        self.window_layout[self.path_indices[file_idx, 0], self.path_indices[file_idx, 1]] = BLUE
                else:
                    self.window_layout[self.path_indices[file_idx, 0], self.path_indices[file_idx, 1]] = board[file_idx] + COLOR_OFFSET
        self.redraw()

    def redraw(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.window_layout[i, j] == EMPTY:
                    continue
                self.frames[i][j].config(bg=bg_colors[self.window_layout[i, j]])
        self.frames[BOARD_SIZE][10].config(text=str(player_str[self.player]))
        self.frames[5][5].config(text=str(self.die))
        self.window.update() 

    def draw(self):
        for i in range(BOARD_SIZE+1):
            if i != BOARD_SIZE:
                self.window.columnconfigure(i, weight=1, minsize=SIZE)
                self.window.rowconfigure(i, weight=1, minsize=SIZE)
            self.frames[5][5] = tk.Label(text=str(self.die))
            self.frames[5][5].grid(row=5, column=5)
            for j in range(BOARD_SIZE):
                if i == BOARD_SIZE:
                    if (j == 0):
                        self.frames[i][j] = tk.Label(text="Nezlob se!")
                        self.frames[i][j].grid(row=i, column=j)
                    if (j == 9):
                        self.frames[i][j] = tk.Label(text="Hrac:")
                        self.frames[i][j].grid(row=i, column=j)
                    if (j == 10):
                        self.frames[i][j] = tk.Label(text="red")
                        self.frames[i][j].grid(row=i, column=j)
                    continue
                if self.window_layout[i, j] == EMPTY:
                    continue
                frame = tk.Frame(
                    master=self.window,
                    
                    borderwidth=1
                )
                frame.grid(row=i, column=j, padx=1, pady=1)
                self.frames[i][j] = tk.Frame(master=frame,width=SIZE, height=SIZE, bg=bg_colors[self.window_layout[i, j]])
                self.frames[i][j].pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.window.update() 