import tkinter as tk
from tkinter import messagebox
import math


def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)


def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                moves.append((i, j))
    return moves


def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_board_full(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))


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


def on_click(row, col):
    if board[row][col] == ' ':
        board[row][col] = 'X'
        buttons[row][col].config(text='X', state=tk.DISABLED)
        if check_winner(board, 'X'):
            messagebox.showinfo("Game Over", "Player wins!")
            reset_board()
            return
        if is_board_full(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
            return

        # AI TURN HERE
        best_move = get_best_move(board)
        if best_move:
            ai_row, ai_col = best_move
            board[ai_row][ai_col] = 'O'
            buttons[ai_row][ai_col].config(text='O', state=tk.DISABLED)
            if check_winner(board, 'O'):
                messagebox.showinfo("Game Over", "AI wins!")
                reset_board()
                return
            if is_board_full(board):
                messagebox.showinfo("Game Over", "It's a draw!")
                reset_board()
                return


def reset_board():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text='', state=tk.NORMAL)


# Main Game
root = tk.Tk()
root.title("Tic Tac Toe")
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='', font=('Arial', 24), width=5, height=2,
                                  command=lambda row=i, col=j: on_click(row, col))
        buttons[i][j].grid(row=i, column=j)

board = [[' ' for _ in range(3)] for _ in range(3)]
root.mainloop()