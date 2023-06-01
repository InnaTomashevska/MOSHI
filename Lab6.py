import pygame
import sys
import random

# Розміри екрану
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300

# Розмір поля
BOARD_SIZE = 300

# Колір фону
BACKGROUND_COLOR = (255, 255, 255)

# Колір лінійок на полі
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 2

# Колір кола та хрестика
CIRCLE_COLOR = (255, 0, 0)
CIRCLE_RADIUS = 40
CIRCLE_WIDTH = 5

CROSS_COLOR = (0, 0, 255)
CROSS_WIDTH = 5

# Колір червоної лінії на виграшній лінії
WIN_LINE_COLOR_PLAYER = (255, 0, 0)
WIN_LINE_COLOR_COMPUTER = (0, 255, 0)
WIN_LINE_WIDTH = 5

# Розмір комірки
CELL_SIZE = BOARD_SIZE // 3

# Відступи для хрестика
PADDING = 40


# Функція для ініціалізації pygame
def initialize_pygame():
    pygame.init()
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Функція для візуалізації поля гри
def draw_board(screen, board):
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, BOARD_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, BOARD_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE), (BOARD_SIZE, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * CELL_SIZE), (BOARD_SIZE, 2 * CELL_SIZE), LINE_WIDTH)

    for row in range(3):
        for col in range(3):
            cell_x = col * CELL_SIZE
            cell_y = row * CELL_SIZE

            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (cell_x + PADDING, cell_y + CELL_SIZE - PADDING),
                                 (cell_x + CELL_SIZE - PADDING, cell_y + PADDING), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (cell_x + PADDING, cell_y + PADDING),
                                 (cell_x + CELL_SIZE - PADDING, cell_y + CELL_SIZE - PADDING), CROSS_WIDTH)

    # Відобразити червону лінію на виграшній лінії
    winner = check_winner(board)
    if winner is not None:
        if winner == 1:
            line_color = WIN_LINE_COLOR_PLAYER
        else:
            line_color = WIN_LINE_COLOR_COMPUTER

        if board[0][0] == board[1][1] == board[2][2] == winner:
            pygame.draw.line(screen, line_color, (0, 0), (BOARD_SIZE, BOARD_SIZE), WIN_LINE_WIDTH)
        elif board[0][2] == board[1][1] == board[2][0] == winner:
            pygame.draw.line(screen, line_color, (BOARD_SIZE, 0), (0, BOARD_SIZE), WIN_LINE_WIDTH)
        else:
            for i in range(3):
                if board[i][0] == board[i][1] == board[i][2] == winner:
                    pygame.draw.line(screen, line_color, (0, i * CELL_SIZE + CELL_SIZE // 2),
                                     (BOARD_SIZE, i * CELL_SIZE + CELL_SIZE // 2), WIN_LINE_WIDTH)
                if board[0][i] == board[1][i] == board[2][i] == winner:
                    pygame.draw.line(screen, line_color, (i * CELL_SIZE + CELL_SIZE // 2, 0),
                                     (i * CELL_SIZE + CELL_SIZE // 2, BOARD_SIZE), WIN_LINE_WIDTH)

    pygame.display.update()


# Функція для перевірки переможця
def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return None


# Функція для перевірки закінчення гри
def is_game_over(board):
    if check_winner(board) is not None:
        return True
    for row in board:
        if 0 in row:
            return False
    return True


# Функція для здійснення ходу комп'ютера
def make_computer_move(board):
    available_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                available_moves.append((i, j))
    if available_moves:
        best_move = random.choice(available_moves)
        board[best_move[0]][best_move[1]] = 2


# Функція для гри
def play_game(screen):
    pygame.display.set_caption("Крестики-нолики")
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    player_turn = True

    while not is_game_over(board):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = mouseY // CELL_SIZE
                clicked_col = mouseX // CELL_SIZE

                if board[clicked_row][clicked_col] == 0:
                    board[clicked_row][clicked_col] = 1
                    player_turn = False

        if not player_turn:
            make_computer_move(board)
            player_turn = True

        draw_board(screen, board)
        pygame.time.wait(100)

    winner = check_winner(board)
    if winner == 1:
        print("Гравець переміг!")
    elif winner == 2:
        print("Комп'ютер переміг!")
    else:
        print("Нічия!")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()


# Ініціалізувати pygame та екран
screen = initialize_pygame()

# Почати гру
play_game(screen)
