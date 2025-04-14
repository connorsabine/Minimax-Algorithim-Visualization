import pygame
import math

WIDTH, HEIGHT = 1200, 600  
GAME_WIDTH = 600
GRID_SIZE = 3
CELL_SIZE = GAME_WIDTH // GRID_SIZE
LINE_WIDTH = 5
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 15
OFFSET = 50

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
BLANK_COLOR = (200, 200, 200) 

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

pygame.draw.rect(screen, BLANK_COLOR, (GAME_WIDTH, 0, WIDTH, WIDTH))
font = pygame.font.Font(None, 60)

board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
game_over = False


def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (GAME_WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)


def draw_marks():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 'X':
                draw_cross(row, col)
            elif board[row][col] == 'O':
                draw_circle(row, col)


def draw_circle(row, col):
    center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)


def draw_cross(row, col):
    start1 = (col * CELL_SIZE + OFFSET, row * CELL_SIZE + OFFSET)
    end1 = (col * CELL_SIZE + CELL_SIZE - OFFSET, row * CELL_SIZE + CELL_SIZE - OFFSET)
    start2 = (col * CELL_SIZE + OFFSET, row * CELL_SIZE + CELL_SIZE - OFFSET)
    end2 = (col * CELL_SIZE + CELL_SIZE - OFFSET, row * CELL_SIZE + OFFSET)
    pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
    pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)


def get_available_moves(board):
    moves = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == ' ':
                moves.append((i, j))
    return moves


def check_winner(board, player):
    for i in range(GRID_SIZE):
        if all(board[i][j] == player for j in range(GRID_SIZE)):
            return True
        if all(board[j][i] == player for j in range(GRID_SIZE)):
            return True
    if all(board[i][i] == player for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - 1 - i] == player for i in range(GRID_SIZE)):
        return True
    return False


def is_board_full(board):
    return all(board[i][j] != ' ' for i in range(GRID_SIZE) for j in range(GRID_SIZE))


def minimax(board, depth, maximizing_player):
    if check_winner(board, 'X'):
        return -10 + depth
    if check_winner(board, 'O'):
        return 10 - depth
    if is_board_full(board):
        return 0

    if maximizing_player:
        max_eval = -math.inf
        for move in get_available_moves(board):
            row, col = move
            board[row][col] = 'O'
            eval = minimax(board, depth + 1, False)
            board[row][col] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for move in get_available_moves(board):
            row, col = move
            board[row][col] = 'X'
            eval = minimax(board, depth + 1, True)
            board[row][col] = ' '
            min_eval = min(min_eval, eval)
        return min_eval


def get_best_move(board):
    best_move = None
    best_eval = -math.inf
    for move in get_available_moves(board):
        row, col = move
        board[row][col] = 'O'
        eval = minimax(board, 0, False)
        board[row][col] = ' '
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move


def reset_board():
    global board, game_over
    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BLANK_COLOR, (GAME_WIDTH, 0, WIDTH, WIDTH))
    draw_grid()


# Main game loop
draw_grid()
running = True
player_turn = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not event.pos[0] >= GAME_WIDTH:
            mouse_x, mouse_y = event.pos
            clicked_row = int(mouse_y // CELL_SIZE)
            clicked_col = int(mouse_x // CELL_SIZE)

            if board[clicked_row][clicked_col] == ' ' and player_turn:
                board[clicked_row][clicked_col] = 'X'
                if check_winner(board, 'X'):
                    game_over = True
                    text = font.render("Player wins!", True, (0, 0, 0))
                    screen.blit(text, (GAME_WIDTH // 2 - 80, 0))
                elif is_board_full(board):
                    game_over = True
                    text = font.render("It's a draw!", True, (0, 0, 0))
                    screen.blit(text, (GAME_WIDTH // 2 - 80, 0))
                else:
                    player_turn = False
                    
            draw_marks()
            pygame.display.update()


        # AI TURN
        if not player_turn and not game_over:
            best_move = get_best_move(board)
            pygame.draw.rect(screen, BLANK_COLOR, (GAME_WIDTH, 0, WIDTH - GAME_WIDTH, HEIGHT))  
            pygame.display.update()
            for idx, move in enumerate(get_available_moves(board)):
                row, col = move
                board[row][col] = 'O'

                eval = minimax(board, 0, False)
                board[row][col] = ' '

                mini_board_x = GAME_WIDTH + 40 + (idx % 3) * 200  
                mini_board_y = 10 + (idx // 3) * 200 
                pygame.draw.rect(screen, LINE_COLOR, (mini_board_x - 5, mini_board_y - 5, 130, 130), 2)

                for r in range(GRID_SIZE):
                    for c in range(GRID_SIZE):
                        cell_x = mini_board_x + c * 40
                        cell_y = mini_board_y + r * 40
                        if r == row and c == col:
                            pygame.draw.rect(screen, (255, 255, 0), (cell_x, cell_y, 40, 40)) 
                            if board[r][c] == ' ':
                                pygame.draw.circle(screen, (0, 0, 255), (cell_x + 20, cell_y + 20), 15, 2) 
                        if board[r][c] == 'X':
                            pygame.draw.line(screen, CROSS_COLOR, (cell_x + 5, cell_y + 5), (cell_x + 35, cell_y + 35), 2)
                            pygame.draw.line(screen, CROSS_COLOR, (cell_x + 35, cell_y + 5), (cell_x + 5, cell_y + 35), 2)
                        elif board[r][c] == 'O':
                            pygame.draw.circle(screen, CIRCLE_COLOR, (cell_x + 20, cell_y + 20), 15, 2)

                small_font = pygame.font.Font(None, 40)
                move_text = small_font.render(f"Score: {eval}", True, (0, 0, 0))
                screen.blit(move_text, (mini_board_x, mini_board_y + 135))  
                
                pygame.display.update()
                pygame.time.delay(300) 

            if best_move:
                ai_row, ai_col = best_move
                board[ai_row][ai_col] = 'O'
                if check_winner(board, 'O'):
                    game_over = True
                    text = font.render("AI wins!", True, (0, 0, 0))
                    screen.blit(text, (GAME_WIDTH // 2 - 80, 0))
                elif is_board_full(board):
                    game_over = True
                    text = font.render("It's a draw!", True, (0, 0, 0))
                    screen.blit(text, (GAME_WIDTH // 2 - 80, 0))
                player_turn = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_board()
                player_turn = True

    pygame.display.update()
    draw_marks()

pygame.quit()
