import numpy as np
import pygame
import sys
import math

# Define colors
BLUE = (30, 144, 255)  # DodgerBlue
BLACK = (0, 0, 0)
RED = (255, 69, 0)  # RedOrange
YELLOW = (255, 215, 0)  # Gold
GREEN = (0, 255, 0)  # LimeGreen
WHITE = (255, 255, 255)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def get_valid_moves(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_moves = get_valid_moves(board)
    is_terminal = winning_move(board, 1) or winning_move(board, 2) or len(valid_moves) == 0
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 2):
                return (None, 100000000000000)
            elif winning_move(board, 1):
                return (None, -100000000000000)
            else:
                return (None, 0)
        else:
            return (None, evaluate_board(board))

    if maximizing_player:
        value = -math.inf
        column = valid_moves[0]
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 2)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return column, value
    else:
        value = math.inf
        column = valid_moves[0]
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 1)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if beta <= alpha:
                break
        return column, value

def evaluate_board(board):
    score = 0
    # Score center column
    center_array = [int(i) for i in board[:, COLUMN_COUNT // 2]]
    center_count = center_array.count(2)
    score += center_count * 3

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in board[r, :]]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window)

    # Score vertical
    for c in range(COLUMN_COUNT):
        column_array = [int(i) for i in board[:, c]]
        for r in range(ROW_COUNT - 3):
            window = column_array[r:r + 4]
            score += evaluate_window(window)

    # Score positively sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window)

    # Score negatively sloped diagonals
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window)

    return score

def evaluate_window(window):
    score = 0
    if window.count(2) == 4:
        score += 100
    elif window.count(2) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(2) == 2 and window.count(0) == 2:
        score += 2
    if window.count(1) == 3 and window.count(0) == 1:
        score -= 4
    return score

board = create_board()
print_board(board)
game_over = False
turn = 0

# Initialize pygame
pygame.init()

# Define our screen size
SQUARESIZE = 100

# Define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
# Calling function draw_board again
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    if turn == 0:  # Player 1 (Human)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("You won!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

    else:  # Player 2 (AI)
        col, _ = minimax(board, 4, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                label = myfont.render("AI won!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

        print_board(board)
        draw_board(board)

        turn += 1
        turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
