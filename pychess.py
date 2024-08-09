import random

import pygame
import time

SCREEN_SIZE = (960, 1060)

BG_COL = (144, 164, 174)
BUTTON_COL = (200, 230, 201)
FONT_COLOR = (0, 72, 81)
OUTLINE_COL = (245, 229, 0)
DOT_COL = (158, 158, 158)
KILL_COL = (173, 26, 26)

X = 0
Y = 1

POS = 0
COL = 1

PLAY_BUTTON = ((SCREEN_SIZE[0] / 2 - 200, SCREEN_SIZE[1] / 2 - 50, 400, 150), BUTTON_COL)
QUIT_BUTTON = ((SCREEN_SIZE[0] / 2 - 200, SCREEN_SIZE[1] / 2 + 200, 400, 150), BUTTON_COL)
QUIT_GAME_BUTTON = ((10, 10, 100, 50), BUTTON_COL)
BOARD_COORD = (0, 100, 960, 960)
SQUARE = 120

SQUARE_BUTTON = ((0, 0, SQUARE, SQUARE), OUTLINE_COL)

B_PAWN = "resources/black_pawn.png"
B_ROOK = "resources/black_rook.png"
B_KNIGHT = "resources/black_knight.png"
B_KING = "resources/black_king.png"
B_BISHOP = "resources/black_bishop.png"
B_QUEEN = "resources/black_queen.png"
W_PAWN = "resources/white_pawn.png"
W_ROOK = "resources/white_rook.png"
W_BISHOP = "resources/white_bishop.png"
W_KNIGHT = "resources/white_knight.png"
W_QUEEN = "resources/white_queen.png"
W_KING = "resources/white_king.png"
PIECES = [B_KNIGHT, B_PAWN, B_ROOK, B_KING, B_QUEEN, B_BISHOP, W_PAWN, W_ROOK, W_BISHOP, W_KNIGHT, W_QUEEN, W_KING]

# PIECES :

########################################################################################################################################
########################################################################################################################################

class Pawn:
    def __init__(self, black, surface):
        self.black = black
        self.surface = surface
        self.moved = False

    def draw(self, pos):
        if self.black:
            image = pygame.image.load(B_PAWN)
        else:
            image = pygame.image.load(W_PAWN)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 30, pos[1] * SQUARE + 67))
    def is_black(self):
        return self.black
    
    def has_moved(self):
        self.moved = True
    
    def possible_dest_finder(self, board_array, orig_coords):
        possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1
        if not self.moved:
            y_dest = orig_coords[Y] + 2 * player_factor
            if (y_dest >= 0 and y_dest <= 7) and board_array[orig_coords[X]][y_dest] is None and board_array[orig_coords[X]][orig_coords[Y] + 1 * player_factor] is None:
                possible_dest.append((orig_coords[X], y_dest))
        y_dest = orig_coords[Y] + 1 * player_factor
        if (y_dest >= 0 and y_dest <= 7) and board_array[orig_coords[X]][y_dest] is None:
            possible_dest.append((orig_coords[X], y_dest))
        x_dest = orig_coords[X] + 1 * player_factor
        if (x_dest >= 0 and x_dest <= 7) and board_array[x_dest][y_dest] is not None and board_array[x_dest][y_dest].is_black() != self.black:
            possible_dest.append((x_dest, y_dest))
        x_dest = orig_coords[X] - 1 * player_factor
        if (x_dest >= 0 and x_dest <= 7) and board_array[x_dest][y_dest] is not None and board_array[x_dest][y_dest].is_black() != self.black:
            possible_dest.append((x_dest, y_dest))    
        # TODO adding en passant     

        return possible_dest



########################################################################################################################################

class Rook:
    def __init__(self, black, surface):
        self.black = black
        self.surface = surface

    def draw(self, pos):
        if self.black:
            image = pygame.image.load(B_ROOK)
        else:
            image = pygame.image.load(W_ROOK)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 24, pos[1] * SQUARE + 56))
        
    def is_black(self):
        return self.black
    
    def possible_dest_finder(self, board_array, orig_coords):
        possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1

        for x in range(1, 8):
            x = x * player_factor
            if orig_coords[X] + x >= 0 and orig_coords[X] + x <= 7:
                is_not_none = board_array[orig_coords[X] + x][orig_coords[Y]] is not None
                if is_not_none and board_array[orig_coords[X] + x][orig_coords[Y]].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] + x, orig_coords[Y]))
                    if is_not_none and board_array[orig_coords[X] + x][orig_coords[Y]].is_black() != self.black:
                        break

        for x in range(1, 8):
            x = x * player_factor
            if orig_coords[X] - x >= 0 and orig_coords[X] - x <= 7:
                is_not_none = board_array[orig_coords[X] - x][orig_coords[Y]] is not None
                if is_not_none and board_array[orig_coords[X] - x][orig_coords[Y]].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] - x, orig_coords[Y]))
                    if is_not_none and board_array[orig_coords[X] - x][orig_coords[Y]].is_black() != self.black:
                        break        

        for y in range(1, 8):
            y = y * player_factor
            if orig_coords[Y] + y >= 0 and orig_coords[Y] + y <= 7:
                is_not_none = board_array[orig_coords[X]][orig_coords[Y] + y] is not None
                if is_not_none and board_array[orig_coords[X]][orig_coords[Y] + y].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X], orig_coords[Y] + y))
                    if is_not_none and board_array[orig_coords[X]][orig_coords[Y] + y].is_black() != self.black:
                        break

        for y in range(1, 8):
            y = y * player_factor
            if orig_coords[Y] - y >= 0 and orig_coords[Y] - y <= 7:
                is_not_none = board_array[orig_coords[X]][orig_coords[Y] - y] is not None
                if is_not_none and board_array[orig_coords[X]][orig_coords[Y] - y].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X], orig_coords[Y] - y))
                    if is_not_none and board_array[orig_coords[X]][orig_coords[Y] - y].is_black() != self.black:
                        break

        return possible_dest
########################################################################################################################################

class Knight:
    def __init__(self, black, surface):
        self.black = black
        self.surface = surface

    def draw(self, pos):
        if self.black:
            image = pygame.image.load(B_KNIGHT)
        else:
            image = pygame.image.load(W_KNIGHT)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 20, pos[1] * SQUARE + 54))
    def is_black(self):
        return self.black
    
    def possible_dest_finder(self, board_array, orig_coords):
        possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1
        y_dest = orig_coords[Y] + 2 * player_factor
        if (y_dest >= 0 and y_dest <= 7) and board_array[orig_coords[X]][y_dest] is None:
            possible_dest.append((orig_coords[X], y_dest))
        y_dest = orig_coords[Y] + 1 * player_factor
        if (y_dest >= 0 and y_dest <= 7) and board_array[orig_coords[X]][y_dest] is None:
            possible_dest.append((orig_coords[X], y_dest))
        x_dest = orig_coords[X] + 1 * player_factor
        if (x_dest >= 0 and x_dest <= 7) and board_array[x_dest][y_dest] is not None and board_array[x_dest][y_dest].is_black() != self.black:
            possible_dest.append((x_dest, y_dest))
        x_dest = orig_coords[X] - 1 * player_factor
        if (x_dest >= 0 and x_dest <= 7) and board_array[x_dest][y_dest] is not None and board_array[x_dest][y_dest].is_black() != self.black:
            possible_dest.append((x_dest, y_dest))    
        # TODO adding en passant     

        return possible_dest

########################################################################################################################################

class Bishop:
    def __init__(self, black, surface):
        self.black = black
        self.surface = surface

    def draw(self, pos):
        if self.black:
            image = pygame.image.load(B_BISHOP)
        else:
            image = pygame.image.load(W_BISHOP)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 25, pos[1] * SQUARE + 56))
    def is_black(self):
        return self.black
    
    def possible_dest_finder(self, board_array, orig_coords):
        possible_dest = []
        player_factor = -1
        for i in range(1, 8):
            i = i * player_factor
            if orig_coords[X] + i >= 0 and orig_coords[X] + i <= 7 and orig_coords[Y] + i >= 0 and orig_coords[Y] + i <= 7:
                is_not_none = board_array[orig_coords[X] + i][orig_coords[Y] + i] is not None
                if is_not_none and board_array[orig_coords[X] + i][orig_coords[Y] + i].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] + i, orig_coords[Y] + i))
                    if is_not_none and board_array[orig_coords[X] + i][orig_coords[Y] + i].is_black() != self.black:
                        break
        
        for i in range(1, 8):
            i = i * player_factor
            if orig_coords[X] - i >= 0 and orig_coords[X] - i <= 7 and orig_coords[Y] - i >= 0 and orig_coords[Y] - i <= 7:
                is_not_none = board_array[orig_coords[X] - i][orig_coords[Y] - i] is not None
                if is_not_none and board_array[orig_coords[X] - i][orig_coords[Y] - i].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] - i, orig_coords[Y] - i))
                    if is_not_none and board_array[orig_coords[X] - i][orig_coords[Y] - i].is_black() != self.black:
                        break

        for i in range(1, 8):
            i = i * player_factor
            if orig_coords[X] + i >= 0 and orig_coords[X] + i <= 7 and orig_coords[Y] - i >= 0 and orig_coords[Y] - i <= 7:
                is_not_none = board_array[orig_coords[X] + i][orig_coords[Y] - i] is not None
                if is_not_none and board_array[orig_coords[X] + i][orig_coords[Y] - i].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] + i, orig_coords[Y] - i))
                    if is_not_none and board_array[orig_coords[X] + i][orig_coords[Y] - i].is_black() != self.black:
                        break

        for i in range(1, 8):
            i = i * player_factor
            if orig_coords[X] - i >= 0 and orig_coords[X] - i <= 7 and orig_coords[Y] + i >= 0 and orig_coords[Y] + i <= 7:
                is_not_none = board_array[orig_coords[X] - i][orig_coords[Y] + i] is not None
                if is_not_none and board_array[orig_coords[X] - i][orig_coords[Y] + i].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] - i, orig_coords[Y] + i))
                    if is_not_none and board_array[orig_coords[X] - i][orig_coords[Y] + i].is_black() != self.black:
                        break
        
        return possible_dest

########################################################################################################################################

class Queen:
    def __init__(self, black, surface):
        self.black = black
        self.surface = surface

    def draw(self, pos):
        if self.black:
            image = pygame.image.load(B_QUEEN)
        else:
            image = pygame.image.load(W_QUEEN)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 30, pos[1] * SQUARE + 54))
    def is_black(self):
        return self.black
    
    def possible_dest_finder(self, board_array, orig_coords):
        possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1

        for x in range(1, 8):
            x = x * player_factor
            if orig_coords[X] + x >= 0 and orig_coords[X] + x <= 7:
                is_not_none = board_array[orig_coords[X] + x][orig_coords[Y]] is not None
                if is_not_none and board_array[orig_coords[X] + x][orig_coords[Y]].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] + x, orig_coords[Y]))
                    if is_not_none and board_array[orig_coords[X] + x][orig_coords[Y]].is_black() != self.black:
                        break

        for x in range(1, 8):
            x = x * player_factor
            if orig_coords[X] - x >= 0 and orig_coords[X] - x <= 7:
                is_not_none = board_array[orig_coords[X] - x][orig_coords[Y]] is not None
                if is_not_none and board_array[orig_coords[X] - x][orig_coords[Y]].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] - x, orig_coords[Y]))
                    if is_not_none and board_array[orig_coords[X] - x][orig_coords[Y]].is_black() != self.black:
                        break        

        for y in range(1, 8):
            y = y * player_factor
            if orig_coords[Y] + y >= 0 and orig_coords[Y] + y <= 7:
                is_not_none = board_array[orig_coords[X]][orig_coords[Y] + y] is not None
                if is_not_none and board_array[orig_coords[X]][orig_coords[Y] + y].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X], orig_coords[Y] + y))
                    if is_not_none and board_array[orig_coords[X]][orig_coords[Y] + y].is_black() != self.black:
                        break

        for y in range(1, 8):
            y = y * player_factor
            if orig_coords[Y] - y >= 0 and orig_coords[Y] - y <= 7:
                is_not_none = board_array[orig_coords[X]][orig_coords[Y] - y] is not None
                if is_not_none and board_array[orig_coords[X]][orig_coords[Y] - y].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X], orig_coords[Y] - y))
                    if is_not_none and board_array[orig_coords[X]][orig_coords[Y] - y].is_black() != self.black:
                        break
        
        for i in range(1, 8):
            i = i * player_factor
            if orig_coords[X] + i >= 0 and orig_coords[X] + i <= 7 and orig_coords[Y] + i >= 0 and orig_coords[Y] + i <= 7:
                is_not_none = board_array[orig_coords[X] + i][orig_coords[Y] + i] is not None
                if is_not_none and board_array[orig_coords[X] + i][orig_coords[Y] + i].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] + i, orig_coords[Y] + i))
                    if is_not_none and board_array[orig_coords[X] + i][orig_coords[Y] + i].is_black() != self.black:
                        break
        
        for i in range(1, 8):
            i = i * player_factor
            if orig_coords[X] - i >= 0 and orig_coords[X] - i <= 7 and orig_coords[Y] - i >= 0 and orig_coords[Y] - i <= 7:
                is_not_none = board_array[orig_coords[X] - i][orig_coords[Y] - i] is not None
                if is_not_none and board_array[orig_coords[X] - i][orig_coords[Y] - i].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] - i, orig_coords[Y] - i))
                    if is_not_none and board_array[orig_coords[X] - i][orig_coords[Y] - i].is_black() != self.black:
                        break

        for i in range(1, 8):
            i = i * player_factor
            if orig_coords[X] + i >= 0 and orig_coords[X] + i <= 7 and orig_coords[Y] - i >= 0 and orig_coords[Y] - i <= 7:
                is_not_none = board_array[orig_coords[X] + i][orig_coords[Y] - i] is not None
                if is_not_none and board_array[orig_coords[X] + i][orig_coords[Y] - i].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] + i, orig_coords[Y] - i))
                    if is_not_none and board_array[orig_coords[X] + i][orig_coords[Y] - i].is_black() != self.black:
                        break

        for i in range(1, 8):
            i = i * player_factor
            if orig_coords[X] - i >= 0 and orig_coords[X] - i <= 7 and orig_coords[Y] + i >= 0 and orig_coords[Y] + i <= 7:
                is_not_none = board_array[orig_coords[X] - i][orig_coords[Y] + i] is not None
                if is_not_none and board_array[orig_coords[X] - i][orig_coords[Y] + i].is_black() == self.black:
                    break
                else:
                    possible_dest.append((orig_coords[X] - i, orig_coords[Y] + i))
                    if is_not_none and board_array[orig_coords[X] - i][orig_coords[Y] + i].is_black() != self.black:
                        break
        
        return possible_dest

########################################################################################################################################

class King:
    def __init__(self, black, surface):
        self.black = black
        self.surface = surface

    def draw(self, pos):
        if self.black:
            image = pygame.image.load(B_KING)
        else:
            image = pygame.image.load(W_KING)
        self.surface.blit(pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2))),
                          (pos[0] * SQUARE + 30, pos[1] * SQUARE + 52))
    def is_black(self):
        return self.black
    
    def possible_dest_finder(self, board_array, orig_coords):
        possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1
        y_dest = orig_coords[Y] + 2 * player_factor
        if (y_dest >= 0 and y_dest <= 7) and board_array[orig_coords[X]][y_dest] is None:
            possible_dest.append((orig_coords[X], y_dest))
        y_dest = orig_coords[Y] + 1 * player_factor
        if (y_dest >= 0 and y_dest <= 7) and board_array[orig_coords[X]][y_dest] is None:
            possible_dest.append((orig_coords[X], y_dest))
        x_dest = orig_coords[X] + 1 * player_factor
        if (x_dest >= 0 and x_dest <= 7) and board_array[x_dest][y_dest] is not None and board_array[x_dest][y_dest].is_black() != self.black:
            possible_dest.append((x_dest, y_dest))
        x_dest = orig_coords[X] - 1 * player_factor
        if (x_dest >= 0 and x_dest <= 7) and board_array[x_dest][y_dest] is not None and board_array[x_dest][y_dest].is_black() != self.black:
            possible_dest.append((x_dest, y_dest))    

        return possible_dest

########################################################################################################################################
########################################################################################################################################

class Board:
    def __init__(self, surface):
        black = True
        self.surface = surface
        self.board = [[None]*8, [None]*8, [None]*8, [None]*8, [None]*8, [None]*8, [None]*8, [None]*8]
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

    def print_board_white(self):
        board_img = pygame.image.load("resources/board.jpg")
        self.surface.blit(pygame.transform.scale(board_img, (960, 960)), (0, 50))
        for j in range(8):
            for i in range(8):
                if self.board[i][j] is not None:
                    self.board[i][j].draw((i, j))
        pygame.display.update()

    def print_board_black(self):
        board_img = pygame.image.load("resources/board.jpg")
        self.surface.blit(pygame.transform.scale(board_img, (960, 960)), (0, 50))
        for j in range(8):
            for i in range(8):
                if self.board[i][j] is not None:
                    self.board[i][j].draw((7 - i, 7 - j))
        pygame.display.update()

########################################################################################################################################

class Move:
    
    def __init__(self, surface, board, black_turn):
        self.surface = surface
        self.board = board
        self.board_array = self.board.get_board()
        self.black_turn =  black_turn
        self.possible_dest = []

    def validation(self):
        valid = False
        while not valid:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if pygame.mouse.get_pressed()[POS]:
                    self.mouse_pos = pygame.mouse.get_pos()
                    if self.mouse_pos[Y] >= SCREEN_SIZE[1] - 960:
                        self.x = self.mouse_pos[X]//SQUARE
                        self.y = (self.mouse_pos[Y] - 50)//SQUARE
                        if self.black_turn:
                            self.x = 7 - self.x
                            self.y = 7 - self.y
                        square_non_empty = self.board_array[self.x][self.y] is not None
                        if  square_non_empty and self.board_array[self.x][self.y].is_black() == self.black_turn:
                            self.possible_dest = self.board_array[self.x][self.y].possible_dest_finder(self.board_array, (self.x, self.y))
                            valid = True 

    def revalidation(self):
        valid = False
        self.mouse_pos = pygame.mouse.get_pos()
        while not valid:
            self.x = self.mouse_pos[X]//SQUARE
            self.y = (self.mouse_pos[Y] - 50)//SQUARE
            if self.black_turn:
                self.x = 7 - self.x
                self.y = 7 - self.y
            square_non_empty = self.board_array[self.x][self.y] is not None
            if  square_non_empty and self.board_array[self.x][self.y].is_black() == self.black_turn:
                self.possible_dest = self.board_array[self.x][self.y].possible_dest_finder(self.board_array, (self.x, self.y))
                valid = True 


    def execution(self, black_score, white_score):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if pygame.mouse.get_pressed()[POS]:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[Y] >= SCREEN_SIZE[1] - 960:
                        if self.black_turn:
                            dest = (7 - mouse_pos[X]//SQUARE, 7 - (mouse_pos[Y] - 50)//SQUARE)
                        else:
                            dest = (mouse_pos[X]//SQUARE, (mouse_pos[Y] - 50)//SQUARE)
                        if dest in self.possible_dest:
                            if type(self.board_array[self.x][self.y]) is Pawn:
                                self.board_array[self.x][self.y].has_moved()
                            self.board_array[dest[X]][dest[Y]] = self.board_array[self.x][self.y]
                            self.board_array[self.x][self.y] = None
                            return True
                        elif self.board_array[dest[X]][dest[Y]] is not None and self.board_array[dest[X]][dest[Y]].is_black() == self.black_turn:
                            if self.black_turn:
                                self.board.print_board_black()
                            else:
                                self.board.print_board_white()
                            pygame.display.update()
                            return False
                            
    def print_possible_moves(self):
        if self.black_turn:
            x = 7 - self.x
            y = 7 - self.y
        else:
            x = self.x
            y = self.y
        pygame.draw.rect(self.surface, OUTLINE_COL, (x * SQUARE , y * SQUARE + 48, SQUARE, SQUARE + 2), 4)
        for dest in self.possible_dest:
            dest_x = dest[X]
            dest_y = dest[Y]
            b_dest_x = 7 - dest_x
            b_dest_y = 7 - dest_y
            if self.board_array[dest_x][dest_y] is None and not self.black_turn:
                pygame.draw.circle(self.surface, DOT_COL, (dest_x * SQUARE + SQUARE/2 , dest_y * SQUARE + SQUARE/2 + 50), 20, 0)
            elif self.board_array[dest_x][dest_y] is not None and not self.black_turn:
                pygame.draw.circle(self.surface, KILL_COL, (dest_x * SQUARE + SQUARE/2 , dest_y * SQUARE + SQUARE/2 + 50), 20, 0)
            elif self.board_array[7 - b_dest_x][7 - b_dest_y] is None and self.black_turn:
                pygame.draw.circle(self.surface, DOT_COL, (b_dest_x * SQUARE + SQUARE/2 , b_dest_y * SQUARE + SQUARE/2 + 50), 20, 0)
            else:
                print(type(self.board_array[b_dest_x + dest_x][b_dest_y + dest_y]))
                pygame.draw.circle(self.surface, KILL_COL, (b_dest_x * SQUARE + SQUARE/2 , b_dest_y * SQUARE + SQUARE/2 + 50), 20, 0)
        pygame.display.update() 

########################################################################################################################################

class Score:

    def __init__(self):
        self.score = 0

    def update(self, points):
        self.score += points

    def print():
        pass

########################################################################################################################################

class Game:

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(SCREEN_SIZE)

    def in_menu(self):
        in_menu = True
        self.draw_menu()
        while in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_menu = False
                if pygame.mouse.get_pressed()[POS]:
                    mouse_pos = pygame.mouse.get_pos()
                    if colision(PLAY_BUTTON[POS], mouse_pos):
                        in_menu = self.in_game()
                    elif colision(QUIT_BUTTON[POS], mouse_pos):
                        in_menu = False

    def in_game(self):
        in_game = True
        in_menu = True
        black_turn = False
        changed = False
        self.surface.fill(BG_COL)
        black_score = Score()
        white_score = Score()
        board = Board(self.surface)
        while in_game:
            move_done = False
            if black_turn:
                board.print_board_black()
            else:
                board.print_board_white()
            pygame.display.update()
            while not move_done:
                move = Move(self.surface, board, black_turn)
                if not changed:
                    move.validation()
                else:
                    move.revalidation()
                move.print_possible_moves()
                move_done = move.execution(black_score, white_score)  
                changed = not move_done            
            if black_turn:
                board.print_board_black()
            else:
                board.print_board_white()
            pygame.display.update()
            black_turn = not black_turn
            time.sleep(1)
        return in_menu

    def draw_menu(self):
        # TODO: complete piece list
        font = pygame.font.SysFont(None, 100)
        title_font = pygame.font.SysFont(None, 150)
        self.surface.fill(BG_COL)
        pygame.draw.rect(self.surface, PLAY_BUTTON[COL], PLAY_BUTTON[POS], 0)
        pygame.draw.rect(self.surface, QUIT_BUTTON[COL], QUIT_BUTTON[POS], 0)
        title = title_font.render("PYCHESS", True, FONT_COLOR)
        play_txt = font.render("Play", True, FONT_COLOR)
        quit_txt = font.render("Quit", True, FONT_COLOR)
        self.surface.blit(title, (SCREEN_SIZE[0] / 2 - 250, 75))
        self.surface.blit(play_txt, (PLAY_BUTTON[POS][X] + 120, PLAY_BUTTON[POS][Y] + 40))
        self.surface.blit(quit_txt, (QUIT_BUTTON[POS][X] + 120, QUIT_BUTTON[POS][Y] + 40))
        image = pygame.image.load(random.choice(PIECES))
        self.surface.blit(image, (SCREEN_SIZE[0] / 2 - 65, 220))
        pygame.display.update()

########################################################################################################################################

def colision(object, mouse_pos):
        x_axis_col = mouse_pos[0] >= object[0] and mouse_pos[0] <= object[0] + object[2]
        y_axis_col = mouse_pos[1] >= object[1] and mouse_pos[1] <= object[1] + object[3]
        return x_axis_col and y_axis_col

def quit():
    pygame.quit()
    exit(0)

game = Game()
game.in_menu()
pygame.quit()
exit(0)
