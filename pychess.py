import random

import pygame
import time

SCREEN_SIZE = (960, 1060)

BG_COL = (144, 164, 174)
BUTTON_COL = (200, 230, 201)
FONT_COLOR = (0, 72, 81)

X = 0
Y = 1

POS = 0
COL = 1

PLAY_BUTTON = ((SCREEN_SIZE[0] / 2 - 200, SCREEN_SIZE[1] / 2 - 50, 400, 150), BUTTON_COL)
QUIT_BUTTON = ((SCREEN_SIZE[0] / 2 - 200, SCREEN_SIZE[1] / 2 + 200, 400, 150), BUTTON_COL)
QUIT_GAME_BUTTON = ((10, 10, 100, 50), BUTTON_COL)
BOARD_COORD = (0, 100, 960, 960)
SQUARE = 120

B_PAWN = "resources/black_pawn.png"
B_ROOK = "resources/black_rook.png"
B_KNIGHT = "resources/black_knight.png"
B_KING = "resources/black_king.png"
B_BISHOP = "resources/black_bishop.png"
B_QUEEN = "resources/black_queen.png"
W_PAWN = "resources/white_pawn.png"
W_ROOK = "resources/white_rook.png"
W_BISHOP = "resources/white_bishop.png"
PIECES = [B_KNIGHT, B_PAWN, B_ROOK, B_KING, B_QUEEN, B_BISHOP, W_PAWN, W_ROOK, W_BISHOP]


class Board:
    def __init__(self, surface):
        black = True
        self.surface = surface
        self.board = [[None] * 8] * 8
        for j in range(8):
            for i in range(8):

                if j == 0:
                    if i == 0 or i == 7:
                        self.board[i][j] = Rook(black, self.surface)
                    elif i == 1 or i == 6:
                        self.board[i][j] = Knight(black, self.surface)
                    elif i == 2 or i == 5:
                        self.board[i][j] = Bishop(black, self.surface)
                    elif i == 3:
                        self.board[i][j] = Queen(black, self.surface)
                    else:
                        self.board[i][j] = King(black, self.surface)
                elif j == 7:
                    if i == 0 or i == 7:
                        self.board[i][j] = Rook(not black, self.surface)
                    elif i == 1 or i == 6:
                        self.board[i][j] = Knight(not black, self.surface)
                    elif i == 2 or i == 5:
                        self.board[i][j] = Bishop(not black, self.surface)
                    elif i == 3:
                        self.board[i][j] = Queen(not black, self.surface)
                    else:
                        self.board[i][j] = King(not black, self.surface)
                elif j == 1:
                    self.board[i][j] = Pawn(black, self.surface)
                elif j == 6:
                    self.board[i][j] = Pawn(not black, self.surface)

    def get_board(self):
        return self.board

    def print_board(self):
        board_img = pygame.image.load("resources/board.jpg")
        self.surface.blit(pygame.transform.scale(board_img, (960, 960)), (0, 100))
        for j in range(8):
            for i in range(8):
                if self.board[i][j] is not None:
                    self.board[i][j].draw((i, j))
        pygame.display.flip()


class Pawn:
    def __init__(self, black, surface):
        self.is_black = black
        self.surface = surface

    def draw(self, pos):
        if self.is_black:
            image = pygame.image.load(B_PAWN)
        else:
            image = pygame.image.load(W_PAWN)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 50, pos[1] * SQUARE + 20))


class Rook:
    def __init__(self, black, surface):
        self.is_black = black
        self.surface = surface

    def draw(self, pos):
        if self.is_black:
            image = pygame.image.load(B_ROOK)
        else:
            image = pygame.image.load(W_ROOK)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 50, pos[1] * SQUARE + 20))


class Knight:
    def __init__(self, black, surface):
        self.is_black = black
        self.surface = surface

    def draw(self, pos):
        if self.is_black:
            image = pygame.image.load(B_KNIGHT)
        else:
            image = pygame.image.load(B_KNIGHT)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 50, pos[1] * SQUARE + 20))


class Bishop:
    def __init__(self, black, surface):
        self.is_black = black
        self.surface = surface

    def draw(self, pos):
        if self.is_black:
            image = pygame.image.load(B_BISHOP)
        else:
            image = pygame.image.load(W_BISHOP)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 50, pos[1] * SQUARE + 20))


class Queen:
    def __init__(self, black, surface):
        self.is_black = black
        self.surface = surface

    def draw(self, pos):
        if self.is_black:
            image = pygame.image.load(B_QUEEN)
        else:
            image = pygame.image.load(B_QUEEN)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 50, pos[1] * SQUARE + 20))


class King:
    def __init__(self, black, surface):
        self.is_black = black
        self.surface = surface

    def draw(self, pos):
        if self.is_black:
            image = pygame.image.load(B_KING)
        else:
            image = pygame.image.load(B_KING)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 50, pos[1] * SQUARE + 20))


class Move:
    pass


class Game:

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(SCREEN_SIZE)

    def colision(self, object, mouse_pos):
        x_axis_col = mouse_pos[0] >= object[0] and mouse_pos[0] <= object[0] + object[2]
        y_axis_col = mouse_pos[1] >= object[1] and mouse_pos[1] <= object[1] + object[3]
        return x_axis_col and y_axis_col

    def in_menu(self):
        in_menu = True
        self.draw_menu()
        while in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_menu = False
                if pygame.mouse.get_pressed()[POS]:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.colision(PLAY_BUTTON[POS], mouse_pos):
                        in_menu = self.in_game()
                    elif self.colision(QUIT_BUTTON[POS], mouse_pos):
                        in_menu = False

    def in_game(self):
        in_game = True
        self.surface.fill(BG_COL)
        board = Board(self.surface)
        board.print_board()
        while in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
            if pygame.mouse.get_pressed()[POS]:
                mouse_pos = pygame.mouse.get_pos()
                if self.colision(QUIT_GAME_BUTTON[POS], mouse_pos):
                    in_game = False
        return in_game

    def draw_menu(self):
        # TODO: complete piece list
        font = pygame.font.SysFont(None, 100)
        title_font = pygame.font.SysFont(None, 150)
        self.surface.fill(BG_COL)
        pygame.draw.rect(self.surface, PLAY_BUTTON[COL], PLAY_BUTTON[POS], 200)
        pygame.draw.rect(self.surface, QUIT_BUTTON[COL], QUIT_BUTTON[POS], 200)
        title = title_font.render("PYCHESS", True, FONT_COLOR)
        play_txt = font.render("Play", True, FONT_COLOR)
        quit_txt = font.render("Quit", True, FONT_COLOR)
        self.surface.blit(title, (SCREEN_SIZE[0] / 2 - 250, 75))
        self.surface.blit(play_txt, (PLAY_BUTTON[POS][X] + 120, PLAY_BUTTON[POS][Y] + 40))
        self.surface.blit(quit_txt, (QUIT_BUTTON[POS][X] + 120, QUIT_BUTTON[POS][Y] + 40))
        image = pygame.image.load(random.choice(PIECES))
        self.surface.blit(image, (SCREEN_SIZE[0] / 2 - 65, 220))
        pygame.display.flip()


game = Game()
game.in_menu()
pygame.quit()
exit(1)
