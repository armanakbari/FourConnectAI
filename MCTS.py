import random
import sys
import copy
import pygame
import math
from board_mcst import *

def Board_init():
    board = []
    for x in range(BOARDWIDTH):
        board.append([' '] * 7)
    return board

def get_move_MCST(player, board, numberofIterations):
    print("Number of iterations {}".format(numberofIterations))
    arrayofNodes = list()
    bestRatio = 0
    bestMove = 0
    for i in range(0, board.width):
        arrayofNodes.append(Node(board))
    for i in range(numberofIterations):
        randomColumn = random.randint(1, board.width)
        dupelicateBoard = copy.deepcopy(board)
        childToPlay = arrayofNodes[randomColumn - 1]
        dupelicateBoard.makeMove(player, randomColumn - 1)
        childToPlay.incrementVisits()
        if (dupelicateBoard.isWinner(player)):
            childToPlay.incrementWins()

    for i in range(0, board.width):
        ratio = float(arrayofNodes[i].wins / arrayofNodes[i].visits)
        if (ratio > bestRatio):
            bestRatio = ratio
            bestMove = i
    if bestMove == 0:
        bestMove = random.randint(1, board.width) - 1
    print("Best ratio is : {}".format(bestRatio))
    print("Best move is : {}".format(bestMove + 1))
    return bestMove

class Node:
    def __init__(self, board):
        self.board = board
        self.visits = 0
        self.wins = 0    

    def incrementVisits(self):
        self.visits += 1
    
    def incrementWins(self):
        self.wins += 1

def draw_board(board):
	for c in range(BOARDWIDTH):
		for r in range(BOARDHEIGHT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(BOARDWIDTH):
		for r in range(BOARDHEIGHT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(r*SQUARESIZE+SQUARESIZE/2), int(c*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(r*SQUARESIZE+SQUARESIZE/2), int(c*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()



typeOfGame = 1

player1Choice, player2Choice = ['X', 'O']
PLAYER_PIECE = player1Choice
AI_PIECE = player2Choice
player = 'Player 1' 

print('%s will go first.' % player.title())
mainBoard = Board(Board_init())

pygame.init() 
SQUARESIZE = 60
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(mainBoard.board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 40)

flag = 0
while True:
    if flag == 1:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if player == 'Player 1':
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            if player == 'Player 1':
                mainBoard.drawBoard()
                if typeOfGame == 1:
                    posx = event.pos[0]
                    move = int(math.floor(posx/SQUARESIZE))
                    print(move)
                    mainBoard.makeMove(player1Choice, move)
                    
                elif typeOfGame == 2:
                    move = get_move_MCST(player1Choice, mainBoard, PLAYER1ITERATIONS)
                    mainBoard.makeMove(player1Choice, move)
                if mainBoard.isWinner(player1Choice):
                    winner = 'Player 1'
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40,10))
                    pygame.time.wait(1000)
                    PLAYER1WINS += 1
                    flag = 1
                    break
                player = 'Player 2'
            
    if player == 'Player 2':
        mainBoard.drawBoard()	
        move = get_move_MCST(player2Choice, mainBoard, PLAYER2ITERATIONS)
        print('AI', move)
        mainBoard.makeMove(player2Choice, move)
        draw_board(mainBoard.board)
        if mainBoard.isWinner(player2Choice):
            winner = 'Player 2'
            label = myfont.render("Player 2 wins!!", 1, YELLOW)
            screen.blit(label, (40,10))
            PLAYER2WINS += 1
            pygame.time.wait(3000)
            break			
        player = 'Player 1'
    if mainBoard.isBoardFull():
        winner = 'Draw game'
        NUMBEROFDRAWS += 1
        draw_board(mainBoard.board)
        break
mainBoard.drawBoard()
print('Winner is: %s' % winner)