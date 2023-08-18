import numpy as np
import random
import pygame
import sys
import math
import copy

PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

class Board:
    def __init__(self, RC, CC):
        self.row_n = RC
        self.column_n = CC
        self.board = np.zeros((RC,CC))
    def draw_board(self):
        for c in range(self.column_n):
            for r in range(self.row_n):
                pygame.draw.rect(screen, (60,123,150), (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, (5,5,5), (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
        for c in range(self.column_n):
            for r in range(self.row_n):		
                if self.board[r][c] == PLAYER_PIECE:
                    pygame.draw.circle(screen, (205,57,5), (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif self.board[r][c] == AI_PIECE: 
                    pygame.draw.circle(screen, (25,205,0), (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        pygame.display.update()
        
        for c in range(self.column_n):
            for r in range(self.row_n):		
                if self.board[r][c] == PLAYER_PIECE:
                    pygame.draw.circle(screen, (205,57,5), (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif self.board[r][c] == AI_PIECE: 
                    pygame.draw.circle(screen, (25,205,0), (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        pygame.display.update()

    def IVL(self, col):
        return self.board[self.row_n-1][col] == 0
    
    def get_next_open_row(self, col):
        for r in range(self.row_n):
            if self.board[r][col] == 0:
                return r



def winning_move(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def EW(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += EW(window, piece)
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += EW(window, piece)
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += EW(window, piece)
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += EW(window, piece)

    return score

def is_terminal_node(board):
    if winning_move(board.board, PLAYER_PIECE) or winning_move(board.board, AI_PIECE) or len(get_valid_locations(board)) == 0:
        return True
    else:
        return False 

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board.board, AI_PIECE):
                return (None, 99999999999999)
            elif winning_move(board.board, PLAYER_PIECE):
                return (None, -99999999999999)
            else: 
                return (None, 0)
        else: 
            return (None, score_position(board.board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = board.get_next_open_row(col)
            b_copy = copy.deepcopy(board)
            b_copy.board[row][col] = AI_PIECE
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: 
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = board.get_next_open_row(col)
            b_copy = copy.deepcopy(board)
            b_copy.board[row][col,] = PLAYER_PIECE
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if board.IVL(col):
            valid_locations.append(col)
    return valid_locations




def one_player_mode(turn, game_over):
    global screen, width, RADIUS, SQUARESIZE, PLAYER, board, PLAYER_PIECE, myfont, AI_PIECE, AI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (5,5,5), (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, (205,57,5), (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (5,5,5), (0,0, width, SQUARESIZE))
            # Ask for Player 1 Input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if board.IVL(col):
                    row = board.get_next_open_row(col)
                    board.board[row][col] = PLAYER_PIECE

                    if winning_move(board.board, PLAYER_PIECE):
                        label = myfont.render("Player 1 wins!!", 1, (205,57,5))
                        screen.blit(label, (40,10))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    print(np.flip(board.board, 0))
                    board.draw_board()
    if turn == AI and not game_over:				
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        if board.IVL(col):
            row = board.get_next_open_row(col)
            board.board[row][col] = AI_PIECE
            if winning_move(board.board, AI_PIECE):
                label = myfont.render("Player 2 wins!!", 1, (25,205,0))
                screen.blit(label, (40,10))
                game_over = True
            print(np.flip(board.board, 0))
            board.draw_board()
            turn += 1
            turn = turn % 2
    if game_over:
        pygame.time.wait(3000)
    return game_over
def two_player_mode(game_over):
    global turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (5,5,5), (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, (205,57,5), (posx, int(SQUARESIZE/2)), RADIUS)
            else: 
                pygame.draw.circle(screen, (25,205,0), (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (5,5,5), (0,0, width, SQUARESIZE))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if board.IVL(col):
                    row = board.get_next_open_row(col)
                    board.board[row][col] = 1

                    if winning_move(board.board, 1):
                        label = myfont.render("Player 1 wins!!", 1, (205,57,5))
                        screen.blit(label, (40,10))
                        game_over = True
            else:				
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if board.IVL(col):
                    row = board.get_next_open_row(col)
                    board.board[row][col] = 2

                    if winning_move(board.board, 2):
                        label = myfont.render("Player 2 wins!!", 1, (25,205,0))
                        screen.blit(label, (40,10))
                        game_over = True

            print(np.flip(board.board, 0))
            board.draw_board()

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
    return game_over
def zero_player_mode(game_over):
    global turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (5,5,5), (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, (205,57,5), (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()
        
    if turn == AI and not game_over:				
        col, _ = minimax(board, 5, -math.inf, math.inf, True)
        if board.IVL(col):
            row = board.get_next_open_row(col)
            board.board[row][col] = AI_PIECE
            if winning_move(board.board, AI_PIECE):
                label = myfont.render("Player 2 wins!!", 1, (25,205,0))
                screen.blit(label, (40,10))
                game_over = True
            print(np.flip(board.board, 0))
            board.draw_board()
            turn += 1
            turn = turn % 2
        pygame.time.wait(200)
    elif not game_over: 
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        if board.IVL(col):
            row = board.get_next_open_row(col)
            board.board[row][col] = PLAYER_PIECE
            if winning_move(board.board, PLAYER_PIECE):
                label = myfont.render("Player 2 wins!!", 1, (205,57,5))
                screen.blit(label, (40,10))
                game_over = True
            print(np.flip(board.board, 0))
            board.draw_board()
            turn += 1
            turn = turn % 2
        pygame.time.wait(200)
    if game_over:
        pygame.time.wait(3000)
    return game_over 


ROW_COUNT = int(input("input row count: "))
COLUMN_COUNT = int(input("input column count: "))
game_mode = int(input("Select the game mode:\n 1. One player \n 2. Two player \n 3. AI vs AI\n"))
board = Board(ROW_COUNT,COLUMN_COUNT)
print(np.flip(board.board, 0))
game_over = False
pygame.init()
SQUARESIZE = 60
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode((width, height))
board.draw_board()
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 40)
turn = 0            

if game_mode == 2:
    turn = 1

while not game_over:
    if game_mode == 1:
        game_over = one_player_mode(turn, game_over)
    elif game_mode == 2:
        game_over = two_player_mode(game_over)
    else:
        game_over = zero_player_mode(game_over)

    