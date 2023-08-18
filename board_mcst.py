BOARDWIDTH = 7
BOARDHEIGHT = 6
DONTCARE = []
PLAYER1WINS = 0
PLAYER2WINS = 0
NUMBEROFDRAWS = 0
PLAYER1ITERATIONS = 80
PLAYER2ITERATIONS = 80
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROW_COUNT = 6
COLUMN_COUNT = 7



class Board:
    def __init__(self, board):
        self.height = BOARDHEIGHT
        self.width = BOARDWIDTH
        self.board = board

    def isWinner(self, move):
        for y in range(BOARDHEIGHT):
            for x in range(BOARDWIDTH - 3):
                if self.board[x][y] == move and self.board[x+1][y] == move and \
                 self.board[x+2][y] == move and self.board[x+3][y] == move:
                    return True
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT - 3):
                if self.board[x][y] == move and self.board[x][y+1] == move and \
                 self.board[x][y+2] == move and self.board[x][y+3] == move:
                    return True
        for x in range(BOARDWIDTH - 3):
            for y in range(3, BOARDHEIGHT):
                if self.board[x][y] == move and self.board[x+1][y-1] == move and \
                self.board[x+2][y-2] == move and self.board[x+3][y-3] == move:
                    return True
        for x in range(BOARDWIDTH - 3):
            for y in range(BOARDHEIGHT - 3):
                if self.board[x][y] == move and self.board[x+1][y+1] == move and \
                self.board[x+2][y+2] == move and self.board[x+3][y+3] == move:
                    return True
        return False
    def isValidMove(self, move):
        if move < 0 or move >= (BOARDWIDTH):
            return False
        if self.board[move][0] != ' ' and self.board[move][0] != '#':
            return False
        return True
    def isBoardFull(self):
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if self.board[x][y] == ' ':
                    return False
        return True

    def makeMove(self, player, column):
        for y in range(BOARDHEIGHT, -1, -1):
            if self.board[column][y] == ' ':
                self.board[column][y] = player
                return


    def drawBoard(self):
        print()
        print(' ', end='')
        for x in range(1, BOARDWIDTH + 1):
            print(' %s  ' % x, end='')
        print()
        print(('====' * (BOARDWIDTH)))
        for y in range(BOARDHEIGHT):
            for x in range(BOARDWIDTH):
                print(' %s |' % self.board[x][y], end='')
            print()

            print('----' + ('----' * (BOARDWIDTH - 1)))

def Board_init():
    board = []
    for x in range(BOARDWIDTH):
        board.append([' '] * 7)
    return board
