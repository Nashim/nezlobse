from game import *

class Player(Game):
    def __init__(self, player, board, start, finish, initial_file, final_file, ratings):
        self.board = board
        self.start = start
        self.finish = finish
        self.initial_file = initial_file
        self.final_file = final_file
        self.player = player
        self.files_in_game = len(board)
        self.R_FIGURES_ON_BOARD = ratings[0]
        self.R_FIGURES_IN_FINISH = ratings[1]
        self.R_OPPONENT_FIGURES_ON_BOARD = ratings[2]
        self.R_FIGURES_ENDANGERED = ratings[3]
        self.R_LOWEST_DIST_TO_FINISH = ratings[4]
        


    def rate_board(self, board, start, finish):
        rating = 0
        rating += self.R_FIGURES_ON_BOARD * start[self.player]
        rating += self.R_FIGURES_IN_FINISH * (FIGURES_PER_PLAYER - np.sum(finish[self.player] == 1))
        rating += self.R_OPPONENT_FIGURES_ON_BOARD * np.sum((board != self.player) | (board != EMPTY_FILE))
        if len(np.where(board == self.player)[0]) > 0:
            rating += self.R_LOWEST_DIST_TO_FINISH * np.min([self.dist_to_finish(figure) for figure in np.where(board == self.player)[0]])
            for figure in np.where(board == self.player)[0]:
                endangered = self.figure_endangered(figure, board)
                rating += self.R_FIGURES_ENDANGERED*endangered
        return rating
    
    def play(self, board, start, finish, die):
        self.board = board
        self.start = start
        self.finish = finish
        move_rating = []

        # Rate move from start
        from_start_board = self.check_move(self.player, FROM_START, die)
        if from_start_board[0]:
            move_rating.append((FROM_START, self.rate_board(from_start_board[1], from_start_board[2], from_start_board[3])))
        on_board = np.where(self.board == self.player)[0]

        # Rate moves on board
        for figure in on_board:
            on_board_board = self.check_move(self.player, figure, die)
            if on_board_board[0]:
                move_rating.append((figure, self.rate_board(on_board_board[1], on_board_board[2], on_board_board[3])))
        if len(move_rating) > 0:
            print(sorted(move_rating, key=lambda x: x[1]))
            return sorted(move_rating, key=lambda x: x[1])[0][0]
        
        # If no move is possible, try to move in finish
        for figure in np.where(self.finish[self.player] == 1)[0]:
            if self.check_move(self.player, figure+self.files_in_game, die)[0]:
                return figure+self.files_in_game
        # If no move is possible DONT_MOVE
        return DONT_MOVE
        
    def dist_to_finish(self, figure):
        dist = 0
        if figure > self.final_file[self.player]:
            dist = self.files_in_game - figure + self.final_file[self.player]
        else:
            dist = self.final_file[self.player] - figure
        return dist
    
    def between_finish(self, endangered_figure, hunting_figure, board):
        if endangered_figure > hunting_figure:
            if endangered_figure > self.final_file[board[hunting_figure]] and self.final_file[board[hunting_figure]] > hunting_figure:
                return True
        else:
            # Board overflow
            if ((endangered_figure > self.final_file[board[hunting_figure]] and self.final_file[board[hunting_figure]] < hunting_figure)
                 or (endangered_figure < self.final_file[board[hunting_figure]] and self.final_file[board[hunting_figure]] > hunting_figure)):
                return True
        return False
    def figure_endangered(self, figure, board):
        count = 0
        for i in range(1, 6):
            if board[(figure-i)%self.files_in_game] != self.player and board[(figure-i)%self.files_in_game] != EMPTY_FILE:
                count += 1
        return count
            
    def is_at_start(self, board, player):
        return board[self.initial_file[self.player]] == player
    
    def check_move(self, player, figure, steps):
        board = deepcopy(self.board)
        start = deepcopy(self.start)
        finish = deepcopy(self.finish)
        ret = False

        if figure == DONT_MOVE:
            ret = True
        elif figure == FROM_START:
            if start[player] > 0 and steps == 6:
                ret = True
                start = self.return_figure(board, self.initial_file[player])
                board[self.initial_file[player]] = player
                start[player] -= 1
        # In finish
        elif figure >= self.files_in_game:
            figure -= self.files_in_game
            if (figure > FIGURES_PER_PLAYER-1 or self.finish[player][figure] != 1 
                or figure+steps > FIGURES_PER_PLAYER-1) or self.finish[player][figure+steps] == 1:
                pass
            else:
                ret = True
                finish[player][figure] = 0
                finish[player][figure+steps] = 1
        elif self.board[figure] != player:
            print("Not your figure")
            pass
        # Move finish
        elif figure<self.final_file[player] and figure+steps > self.final_file[player]:
            step = figure+steps - self.final_file[player] - 1
            if step < FIGURES_PER_PLAYER and finish[player][step] != 1:
                ret = True
                board[figure] = EMPTY_FILE
                finish[player][step] = 1
                
        # Move on board
        else:
            ret = True
            file = (figure+steps) % self.files_in_game
            start = self.return_figure(board, file)
            board[file] = player
            board[figure] = EMPTY_FILE
        return ret, board, start, finish