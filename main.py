import pygame
import math


# CONSTANTS
WIDTH, HEIGHT = 1200, 600  
GAME_WIDTH = 600
GRID_SIZE = 3
CELL_SIZE = GAME_WIDTH // GRID_SIZE
LINE_WIDTH = 5
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 15
OFFSET = 50


# CONSTANT COLORS
BG_COLOR = (30, 170, 160)
LINE_COLOR = (30, 145, 135)
CIRCLE_COLOR = (230, 230, 200)
CROSS_COLOR = (80, 80, 80)
BLANK_COLOR = (200, 200, 200) 


# DRAW FUNCTIONS
def drawGrid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (GAME_WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)


def drawMarks():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 'X':
                drawCross(row, col)
            elif board[row][col] == 'O':
                drawCircle(row, col)


def drawCircle(row, col):
    center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)


def drawCross(row, col):
    a1 = (col * CELL_SIZE + OFFSET, row * CELL_SIZE + OFFSET)
    a2 = (col * CELL_SIZE + CELL_SIZE - OFFSET, row * CELL_SIZE + CELL_SIZE - OFFSET)
    b1 = (col * CELL_SIZE + OFFSET, row * CELL_SIZE + CELL_SIZE - OFFSET)
    b2 = (col * CELL_SIZE + CELL_SIZE - OFFSET, row * CELL_SIZE + OFFSET)
    pygame.draw.line(screen, CROSS_COLOR, a1, a2, CROSS_WIDTH)
    pygame.draw.line(screen, CROSS_COLOR, b1, b2, CROSS_WIDTH)


# GAME FUNCTIONS
def resetGame():
    # Initialize
    global board, gameOver, running, playerTurn
    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    gameOver = False
    running = True
    playerTurn = True

    # Draw
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BLANK_COLOR, (GAME_WIDTH, 0, WIDTH, WIDTH))
    drawGrid()

def getAvailableMoves(board):
    moves = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == ' ':
                moves.append((i, j))
    return moves


def checkWinner(board, player):
    for i in range(GRID_SIZE):
        if all(board[i][j] == player for j in range(GRID_SIZE)):
            return True
        if all(board[j][i] == player for j in range(GRID_SIZE)):
            return True
    if all(board[i][i] == player for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - 1 - i] == player for i in range(GRID_SIZE)):
        return True
    return False


def isBoardFull(board):
    return all(board[i][j] != ' ' for i in range(GRID_SIZE) for j in range(GRID_SIZE))


# MINIMAX FUNCTIONS
def minimax(board, depth, maximizingPlayer):
    if checkWinner(board, 'X'):
        return -10 + depth
    if checkWinner(board, 'O'):
        return 10 - depth
    if isBoardFull(board):
        return 0

    if maximizingPlayer:
        maxEval = -math.inf
        for move in getAvailableMoves(board):
            row, col = move
            board[row][col] = 'O'
            eval = minimax(board, depth + 1, False)
            board[row][col] = ' '
            maxEval = max(maxEval, eval)
        return maxEval
    else:
        minEval = math.inf
        for move in getAvailableMoves(board):
            row, col = move
            board[row][col] = 'X'
            eval = minimax(board, depth + 1, True)
            board[row][col] = ' '
            minEval = min(minEval, eval)
        return minEval


def getBestMove(board):
    bestMove = None
    bestEval = -math.inf
    for move in getAvailableMoves(board):
        row, col = move
        board[row][col] = 'O'
        eval = minimax(board, 0, False)
        board[row][col] = ' '
        if eval > bestEval:
            bestEval = eval
            bestMove = move
    return bestMove


# MAIN LOOP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font(None, 60)
resetGame()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                resetGame()


        if not gameOver:
            if playerTurn:
                if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] <= GAME_WIDTH:
                    clickedRow = int(event.pos[1] // CELL_SIZE)
                    clickedCol = int(event.pos[0] // CELL_SIZE)

                    if board[clickedRow][clickedCol] == ' ' and playerTurn:
                        board[clickedRow][clickedCol] = 'X'
                        if checkWinner(board, 'X'):
                            gameOver = True
                            text = font.render("Player wins!", True, (0, 0, 0))
                            screen.blit(text, (GAME_WIDTH // 2 - 80, 0))
                        elif isBoardFull(board):
                            gameOver = True
                            text = font.render("It's a draw!", True, (0, 0, 0))
                            screen.blit(text, (GAME_WIDTH // 2 - 80, 0))
                        else:
                            playerTurn = False

            else:

                # Draw Mini Boards
                pygame.draw.rect(screen, BLANK_COLOR, (GAME_WIDTH, 0, WIDTH - GAME_WIDTH, HEIGHT))  
                for idx, move in enumerate(getAvailableMoves(board)):
                    row, col = move

                    # Run MiniMax on Move
                    board[row][col] = 'O'
                    eval = minimax(board, 0, False)
                    board[row][col] = ' '

                    # Draw Miniboard for the Move
                    miniBoardX = GAME_WIDTH + 40 + (idx % 3) * 200  
                    miniBoardY = 10 + (idx // 3) * 200 
                    pygame.draw.rect(screen, LINE_COLOR, (miniBoardX - 5, miniBoardY - 5, 130, 130), 2)

                    for r in range(GRID_SIZE):
                        for c in range(GRID_SIZE):
                            cellX = miniBoardX + c * 40
                            cellY = miniBoardY + r * 40
                            if r == row and c == col:
                                pygame.draw.rect(screen, (255, 255, 0), (cellX, cellY, 40, 40)) 
                                if board[r][c] == ' ':
                                    pygame.draw.circle(screen, (0, 0, 255), (cellX + 20, cellY + 20), 15, 2) 
                            if board[r][c] == 'X':
                                pygame.draw.line(screen, CROSS_COLOR, (cellX + 5, cellY + 5), (cellX + 35, cellY + 35), 2)
                                pygame.draw.line(screen, CROSS_COLOR, (cellX + 35, cellY + 5), (cellX + 5, cellY + 35), 2)
                            elif board[r][c] == 'O':
                                pygame.draw.circle(screen, CIRCLE_COLOR, (cellX + 20, cellY + 20), 15, 2)

                    # Draw Mini Board Text
                    moveText = pygame.font.Font(None, 40).render(f"Score: {eval}", True, (0, 0, 0))
                    screen.blit(moveText, (miniBoardX, miniBoardY + 135))  

                    # Update Screen with Delay
                    pygame.display.update()
                    pygame.time.delay(300) 


                # Make the Best Move
                bestMove = getBestMove(board)
                if bestMove:
                    aiRow, aiCol = bestMove
                    board[aiRow][aiCol] = 'O'
                    if checkWinner(board, 'O'):
                        gameOver = True
                        text = font.render("AI wins!", True, (0, 0, 0))
                        screen.blit(text, (GAME_WIDTH // 2 - 80, 0))
                    elif isBoardFull(board):
                        gameOver = True
                        text = font.render("It's a draw!", True, (0, 0, 0))
                        screen.blit(text, (GAME_WIDTH // 2 - 80, 0))
                    playerTurn = True

    drawMarks()
    pygame.display.update()

pygame.quit()