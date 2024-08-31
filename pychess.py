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
PROMOTION_FRAME = (400, 0, 400, 50)
MENU_BUTTON = (840, 0, 120, 50)
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
        self.possible_dest = []
        self.points = 1
        self.black = black
        self.surface = surface
        self.moved = False
        self.double_jumped = False
        if self.black:
            self.file = B_PAWN
            self.image = pygame.image.load(self.file)
        else:
            self.file = W_PAWN
            self.image = pygame.image.load(self.file)

    def get_possible_dest(self):
        return self.possible_dest
    
    def get_points(self):
        return self.points

    def get_file(self):
        return self.file

    def draw(self, pos):
        self.surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width() / 2), int(self.image.get_height() / 2))),
                          (pos[0] * SQUARE + 30, pos[1] * SQUARE + 67))
    def is_black(self):
        return self.black
    
    def has_moved(self):
        self.moved = True

    def get_moved(self):
        return self.moved

    def set_double_jumped(self, has_db):
        self.double_jumped = has_db

    def get_double_jumped(self):
        return self.double_jumped
    
    def possible_dest_finder(self, board_array, orig, is_sim):
        self.possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1

        x_dest = orig[X]
        # checking 2 foward
        if not self.moved:
            y_dest = orig[Y] + 2 * player_factor
            if is_in_bounds(x_dest, y_dest) and board_array[x_dest][y_dest] is None and board_array[x_dest][orig[Y] + 1 * player_factor] is None:
                if is_sim or is_safe(orig, x_dest, y_dest, board_array, self.black, player_factor):
                    self.possible_dest.append((x_dest, y_dest))

        y_dest = orig[Y] + 1 * player_factor

        #check 1 foward
        if is_in_bounds(x_dest, y_dest) and board_array[x_dest][y_dest] is None:
                if is_sim or is_safe(orig, x_dest, y_dest, board_array, self.black, player_factor):
                    self.possible_dest.append((x_dest, y_dest))

        x_dest = orig[X] + 1 * player_factor

        #check sid kill 1/2
        self.check_side_kill(orig, board_array, x_dest, y_dest, is_sim, player_factor)
        
        x_dest = orig[X] - 1 * player_factor

        #check sid kill 2/2
        self.check_side_kill(orig, board_array, x_dest, y_dest, is_sim, player_factor)

        return self.possible_dest
        
    def check_side_kill(self, orig, board_array, x_dest, y_dest, is_sim, player_factor):
        if is_in_bounds(x_dest, y_dest) and (is_sim or is_safe(orig, x_dest, y_dest, board_array, self.black, player_factor)):
                if board_array[x_dest][y_dest] is not None and board_array[x_dest][y_dest].is_black() != self.black:
                    self.possible_dest.append((x_dest, y_dest))
                elif self.is_en_passant(board_array, x_dest, y_dest, player_factor):
                    self.possible_dest.append((x_dest, y_dest))

    def is_en_passant(self, board_array, x_dest, y_dest, player_factor):
        is_en_passant = False
        if type(board_array[x_dest][y_dest - 1 * player_factor]) is Pawn:
            is_en_passant = board_array[x_dest][y_dest - 1 * player_factor].is_black() != self.black and board_array[x_dest][y_dest - 1 * player_factor].get_double_jumped()
        return is_en_passant        
    
########################################################################################################################################

class Rook:
    def __init__(self, black, surface):
        self.points = 5
        self.black = black
        self.surface = surface
        self.moved = False
        if self.black:
            self.file = B_ROOK
            self.image = pygame.image.load(self.file)
        else:
            self.file = W_ROOK
            self.image = pygame.image.load(self.file)

    def get_possible_dest(self):
        return self.possible_dest

    def get_points(self):
        return self.points

    def get_moved(self):
        return self.moved
    
    def has_moved(self):
        self.moved = True

    def get_file(self):
        return self.file

    def draw(self, pos):
        self.surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width() / 2), int(self.image.get_height() / 2))),
                          (pos[0] * SQUARE + 24, pos[1] * SQUARE + 56))
        
    def is_black(self):
        return self.black
    
    def possible_dest_finder(self, board_array, orig, is_sim):
        self.possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1

        hor_1_done = False
        hor_2_done = False
        vert_1_done = False
        vert_2_done = False

        for i in range(1, 8):
            i = i * player_factor

            #checking hor 1
            x_dest = orig[X] + i
            hor_1_done = self.sonar(orig, player_factor, board_array, x_dest, orig[Y], hor_1_done, is_sim)

            #checking hor 2
            x_dest = orig[X] - i
            hor_2_done = self.sonar(orig, player_factor, board_array, x_dest, orig[Y], hor_2_done, is_sim)

            #checking vert 1
            y_dest = orig[Y] + i
            vert_1_done = self.sonar(orig, player_factor, board_array, orig[X], y_dest, vert_1_done, is_sim)

            #checking vert 2
            y_dest = orig[Y] - i
            vert_2_done = self.sonar(orig, player_factor, board_array, orig[X], y_dest, vert_2_done, is_sim)

        if is_sim:
            mock_possible_dest = self.possible_dest
            self.possible_dest = []
            return mock_possible_dest
        else:
            return self.possible_dest
     
    def sonar(self, orig, player_factor, board_array, x_dest, y_dest, done, is_sim):
        if not done and is_in_bounds(x_dest, y_dest):
                is_not_none = board_array[x_dest][y_dest] is not None
                if is_not_none and board_array[x_dest][y_dest].is_black() == self.black:
                    done = True
                elif is_sim or is_safe(orig, x_dest, y_dest, board_array, self.black, player_factor):
                    self.possible_dest.append((x_dest, y_dest))
                    if is_not_none and board_array[x_dest][y_dest].is_black() != self.black:
                        done = True
        return done

    
########################################################################################################################################

class Knight:
    def __init__(self, black, surface):
        self.points = 3
        self.black = black
        self.surface = surface
        if self.black:
            self.file = B_KNIGHT
            self.image = pygame.image.load(self.file)
        else:
            self.file = W_KNIGHT
            self.image = pygame.image.load(self.file)

    def get_possible_dest(self):
        return self.possible_dest

    def get_points(self):
        return self.points

    def get_file(self):
        return self.file

    def draw(self, pos):
        self.surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width() / 2), int(self.image.get_height() / 2))),
                          (pos[0] * SQUARE + 20, pos[1] * SQUARE + 54))
    def is_black(self):
        return self.black
    
    def possible_dest_finder(self, board_array, orig, is_sim):
        self.possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1
            
        x_dest = orig[X] - 1 * player_factor
        y_dest = orig[Y] - 2 * player_factor

        self.check_L_move(orig, board_array, x_dest, y_dest, is_sim, player_factor)

        x_dest = orig[X] + 1 * player_factor

        self.check_L_move(orig, board_array, x_dest, y_dest, is_sim, player_factor)

        x_dest = orig[X] + 2 * player_factor
        y_dest = orig[Y] - 1 * player_factor
        
        self.check_L_move(orig, board_array, x_dest, y_dest, is_sim, player_factor)

        y_dest = orig[Y] + 1 * player_factor
        
        self.check_L_move(orig, board_array, x_dest, y_dest, is_sim, player_factor)

        x_dest = orig[X] + 1 * player_factor
        y_dest = orig[Y] + 2 * player_factor
        
        self.check_L_move(orig, board_array, x_dest, y_dest, is_sim, player_factor)

        x_dest = orig[X] - 1 * player_factor
        
        self.check_L_move(orig, board_array, x_dest, y_dest, is_sim, player_factor)

        x_dest = orig[X] - 2 * player_factor
        y_dest = orig[Y] + 1 * player_factor
        
        self.check_L_move(orig, board_array, x_dest, y_dest, is_sim, player_factor)

        y_dest = orig[Y] - 1 * player_factor
        
        self.check_L_move(orig, board_array, x_dest, y_dest, is_sim, player_factor)

        return self.possible_dest
    
    def check_L_move(self, orig, board_array, x_dest, y_dest, is_sim, player_factor):
        if is_in_bounds(x_dest, y_dest)  and (is_sim or is_safe(orig, x_dest, y_dest, board_array, self.black, player_factor)):
            is_none = board_array[x_dest][y_dest] is None
            if is_none:
                self.possible_dest.append((x_dest, y_dest))
            elif board_array[x_dest][y_dest].is_black() != self.black:
                self.possible_dest.append((x_dest, y_dest))

########################################################################################################################################

class Bishop:
    def __init__(self, black, surface):
        self.points = 3
        self.black = black
        self.surface = surface
        if self.black:
            self.file = B_BISHOP
            self.image = pygame.image.load(self.file)
        else:
            self.file = W_BISHOP
            self.image = pygame.image.load(self.file)
    
    def get_possible_dest(self):
        return self.possible_dest
    
    def get_points(self):
        return self.points

    def get_file(self):
        return self.file

    def draw(self, pos):
        self.surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width() / 2), int(self.image.get_height() / 2))),
                          (pos[0] * SQUARE + 25, pos[1] * SQUARE + 56))
    def is_black(self):
        return self.black
    
    def possible_dest_finder(self, board_array, orig, is_sim):
        self.possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1

        diag_1_done = False
        diag_2_done = False
        diag_3_done = False
        diag_4_done = False

        for i in range(1, 8):
            i = i * player_factor

            #checking diag 1
            x_dest = orig[X] + i
            y_dest = orig[Y] + i
            diag_1_done = self.sonar(orig, player_factor, board_array, x_dest, y_dest, diag_1_done, is_sim)

            #checkin diag 2
            x_dest = orig[X] - i
            y_dest = orig[Y] - i
            diag_2_done = self.sonar(orig, player_factor, board_array, x_dest, y_dest, diag_2_done, is_sim)

            #checking diag 3
            x_dest = orig[X] + i
            y_dest = orig[Y] - i
            diag_3_done = self.sonar(orig, player_factor, board_array, x_dest, y_dest, diag_3_done, is_sim)

            #checking diag 4
            x_dest = orig[X] - i
            y_dest = orig[Y] + i
            diag_4_done = self.sonar(orig, player_factor, board_array, x_dest, y_dest, diag_4_done, is_sim)
        
        return self.possible_dest
    
    def sonar(self, orig, player_factor, board_array, x_dest, y_dest, done, is_sim):
        if not done and is_in_bounds(x_dest, y_dest):
            is_not_none = board_array[x_dest][y_dest] is not None
            if is_not_none and board_array[x_dest][y_dest].is_black() == self.black:
                done = True
            elif is_sim or is_safe(orig, x_dest, y_dest, board_array, self.black, player_factor):
                self.possible_dest.append((x_dest, y_dest))
                if is_not_none and board_array[x_dest][y_dest].is_black() != self.black:
                    done = True
        return done
    
    
########################################################################################################################################

class Queen:
    def __init__(self, black, surface):
        self.points = 9
        self.black = black
        self.surface = surface
        if self.black:
            self.file = B_QUEEN
            self.image = pygame.image.load(self.file)
        else:
            self.file = W_QUEEN
            self.image = pygame.image.load(self.file)

    def get_possible_dest(self):
        return self.possible_dest
    
    def get_points(self):
        return self.points
    
    def get_file(self):
        return self.file

    def draw(self, pos):
        self.surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width() / 2), int(self.image.get_height() / 2))),
                          (pos[0] * SQUARE + 30, pos[1] * SQUARE + 54))
    def is_black(self):
        return self.black
    
    def possible_dest_finder(self, board_array, orig, is_sim):
        self.possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1

        diag_1_done = False
        diag_2_done = False
        diag_3_done = False
        diag_4_done = False

        hor_1_done = False
        hor_2_done = False
        vert_1_done = False
        vert_2_done = False

        for i in range(1, 8):
            i = i * player_factor

            x_dest = orig[X] + i
            y_dest = orig[Y] + i

            #checking hor 1
            hor_1_done = self.sonar(orig, player_factor, board_array, x_dest, orig[Y], hor_1_done, is_sim)

            #checking diag 1
            diag_1_done = self.sonar(orig, player_factor, board_array, x_dest, y_dest, diag_1_done, is_sim)

            x_dest = orig[X] - i
            y_dest = orig[Y] - i

            #checking hor 2
            hor_2_done = self.sonar(orig, player_factor, board_array, x_dest, orig[Y], hor_2_done, is_sim)

            #checkin diag 2
            diag_2_done = self.sonar(orig, player_factor, board_array, x_dest, y_dest, diag_2_done, is_sim)

            x_dest = orig[X] + i
            y_dest = orig[Y] - i

            #checking vert 1
            vert_1_done = self.sonar(orig, player_factor, board_array, orig[X], y_dest, vert_1_done, is_sim)

            #checking diag 3
            diag_3_done = self.sonar(orig, player_factor, board_array, x_dest, y_dest, diag_3_done, is_sim)

            x_dest = orig[X] - i
            y_dest = orig[Y] + i

            #checking vert 2
            vert_2_done = self.sonar(orig, player_factor, board_array, orig[X], y_dest, vert_2_done, is_sim)

            #checking diag 4
            diag_4_done = self.sonar(orig, player_factor, board_array, x_dest, y_dest, diag_4_done, is_sim)
        
        return self.possible_dest

    def sonar(self, orig, player_factor, board_array, x_dest, y_dest, done, is_sim):
        if not done and is_in_bounds(x_dest, y_dest):
                is_not_none = board_array[x_dest][y_dest] is not None
                if is_not_none and board_array[x_dest][y_dest].is_black() == self.black:
                    done = True
                elif is_sim or is_safe(orig, x_dest, y_dest, board_array, self.black, player_factor):
                    self.possible_dest.append((x_dest, y_dest))
                    if is_not_none and board_array[x_dest][y_dest].is_black() != self.black:
                        done = True
        return done
    
########################################################################################################################################

class King:
    def __init__(self, black, surface):
        self.black = black
        self.surface = surface
        self.moved = False
        if self.black:
            self.image = pygame.image.load(B_KING)
        else:
            self.image = pygame.image.load(W_KING)

    def get_possible_dest(self):
        return self.possible_dest
    
    def get_moved(self):
        return self.moved
    
    def has_moved(self):
        self.moved = True

    def get_image(self):
        return self.image

    def draw(self, pos):
        self.surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width() / 2), int(self.image.get_height() / 2))),
                          (pos[0] * SQUARE + 30, pos[1] * SQUARE + 52))
    def is_black(self):
        return self.black
    
    def possible_dest_finder(self, board_array, orig, is_sim):
        self.possible_dest = []
        player_factor = -1
        if self.black:
            player_factor = 1

        x_dest = orig[X] + 1 * player_factor
        y_dest = orig[Y] + 1 * player_factor
        self.sonar(orig, player_factor, board_array, x_dest, y_dest, is_sim)

        y_dest = orig[Y]
        self.sonar(orig, player_factor, board_array, x_dest, y_dest, is_sim)

        y_dest = orig[Y] - 1 * player_factor
        self.sonar(orig, player_factor, board_array, x_dest, y_dest, is_sim)

        x_dest = orig[X]
        self.sonar(orig, player_factor, board_array, x_dest, y_dest, is_sim)

        x_dest = orig[X] - 1 * player_factor
        self.sonar(orig, player_factor, board_array, x_dest, y_dest, is_sim)

        y_dest = orig[Y]
        self.sonar(orig, player_factor, board_array, x_dest, y_dest, is_sim)

        y_dest = orig[Y] + 1 * player_factor
        self.sonar(orig, player_factor, board_array, x_dest, y_dest, is_sim)

        x_dest = orig[X]
        self.sonar(orig, player_factor, board_array, x_dest, y_dest, is_sim)

        #checking castles
        if not self.moved and not is_sim:
            #checking big castle
            begin_index = 1
            end_index = 4
            x_final_pos = 2
            self.check_castle(orig, player_factor, board_array, begin_index, end_index, x_final_pos)

            #checking small castle
            begin_index = 5
            end_index = 7
            x_final_pos = 6
            self.check_castle(orig, player_factor, board_array, begin_index, end_index, x_final_pos)

        return self.possible_dest
    
    def sonar(self, orig, player_factor, board_array, x_dest, y_dest, is_sim):
        if is_in_bounds(x_dest, y_dest) and (is_sim or is_safe(orig, x_dest, y_dest, board_array, self.black, player_factor)):
            if board_array[x_dest][y_dest] is None or board_array[x_dest][y_dest].is_black() != self.black:
                self.possible_dest.append((x_dest, y_dest))
        
    def check_castle(self, orig, player_factor, board_array, begin_index, end_index, x_final_pos):
        castle_valid = True

        if self.black:
            rook_valid = type(board_array[0][0]) is Rook and not board_array[0][0].get_moved()
            rook_y = 0
        else:
            rook_valid = type(board_array[0][7]) is Rook and not board_array[0][7].get_moved()
            rook_y = 7

        if rook_valid:
            for i in range(begin_index, end_index):
                if board_array[i][rook_y] is not None or not is_safe(orig, i, rook_y, board_array, self.black, player_factor):
                    castle_valid = False 
                    break
                
        if castle_valid:
            self.possible_dest.append((x_final_pos, rook_y))
    
########################################################################################################################################
########################################################################################################################################

class Board:
    def __init__(self, surface, black_score, white_score):
        self.balck_score = black_score
        self.white_score = white_score
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

    def print_board_white(self, is_promotion):
        black_turn = False
        self.surface.fill(BG_COL)
        font = pygame.font.SysFont(None, 30)
        esc_msg = font.render("MENU [esc]", True, FONT_COLOR)
        self.surface.blit(esc_msg, (845, 17))
        board_img = pygame.image.load("resources/board.jpg")
        self.surface.blit(pygame.transform.scale(board_img, (960, 960)), (0, 50))
        for j in range(8):
            for i in range(8):
                if self.board[i][j] is not None:
                    self.board[i][j].draw((i, j))
        if not is_promotion:
            self.balck_score.print(black_turn)
        self.white_score.print(black_turn)
        pygame.display.update()

    def print_board_black(self, is_promotion):
        black_turn = True
        self.surface.fill(BG_COL)
        font = pygame.font.SysFont(None, 30)
        esc_msg = font.render("MENU [esc]", True, FONT_COLOR)
        self.surface.blit(esc_msg, (845, 17))
        board_img = pygame.image.load("resources/board.jpg")
        self.surface.blit(pygame.transform.scale(board_img, (960, 960)), (0, 50))
        for j in range(8):
            for i in range(8):
                if self.board[i][j] is not None:
                    self.board[i][j].draw((7 - i, 7 - j))
        if not is_promotion:
            self.white_score.print(black_turn)
        self.balck_score.print(black_turn)
        pygame.display.update()

########################################################################################################################################

class Move:
    
    def __init__(self, surface, board, black_turn):
        self.x = 0
        self.y = 0
        self.mouse_pos = None
        self.surface = surface
        self.board = board
        self.board_array = self.board.get_board()
        self.black_turn =  black_turn
        self.possible_piece_dest = []
        self.possible_friendly_dest = []
        if black_turn:
            self.player_factor = 1
        else:
            self.player_factor = -1
        is_sim = False
        self.possible_friendly_dest = board_friendly_search(is_sim, self.black_turn, self.board_array)
        
    def validation(self):
        in_game = True
        valid = False
        while not valid:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        in_game = False
                        return in_game
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mouse_pos = pygame.mouse.get_pos()
                    if colision(MENU_BUTTON, self.mouse_pos):
                        in_game = False
                        return in_game
                    if self.mouse_pos[Y] >= 50 and self.mouse_pos[Y] <= 1009:
                        self.x = self.mouse_pos[X]//SQUARE
                        self.y = (self.mouse_pos[Y] - 50)//SQUARE
                        if self.black_turn:
                            self.x = 7 - self.x
                            self.y = 7 - self.y
                        square_non_empty = self.board_array[self.x][self.y] is not None
                        if square_non_empty and self.board_array[self.x][self.y].is_black() == self.black_turn:
                            self.possible_piece_dest = self.board_array[self.x][self.y].get_possible_dest()
                            valid = True
            pygame.display.update()
        return in_game

    def revalidation(self):
        self.possible_dest = []
        self.x = self.mouse_pos[X]//SQUARE
        self.y = (self.mouse_pos[Y] - 50)//SQUARE
        if self.black_turn:
            self.x = 7 - self.x
            self.y = 7 - self.y
        self.possible_piece_dest = self.board_array[self.x][self.y].get_possible_dest()

    def execution(self, score):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mouse_pos = pygame.mouse.get_pos()
                    if colision(MENU_BUTTON, self.mouse_pos):
                        return None
                    if self.mouse_pos[Y] >= 50 and self.mouse_pos[Y] <= 1009:
                        if self.black_turn:
                            dest = (7 - self.mouse_pos[X]//SQUARE, 7 - (self.mouse_pos[Y] - 50)//SQUARE)
                        else:
                            dest = (self.mouse_pos[X]//SQUARE, (self.mouse_pos[Y] - 50)//SQUARE)
                        if dest in self.possible_piece_dest:

                            if type(self.board_array[self.x][self.y]) is Rook:
                                if not self.board_array[self.x][self.y].get_moved():
                                    self.board_array[self.x][self.y].has_moved()

                            elif type(self.board_array[self.x][self.y]) is King:
                                if not self.board_array[self.x][self.y].get_moved():
                                    self.board_array[self.x][self.y].has_moved()

                                #if small castle
                                if dest[X] - self.x == 2:
                                    self.board_array[self.x + 1][self.y] = self.board_array[self.x + 3][self.y]
                                    self.board_array[self.x + 3][self.y] = None

                                #if big castle
                                elif dest[X] - self.x == -2:
                                    self.board_array[self.x - 1][self.y] = self.board_array[self.x - 4][self.y]
                                    self.board_array[self.x - 4][self.y] = None

                            elif type(self.board_array[self.x][self.y]) is Pawn:
                                if not self.board_array[self.x][self.y].get_moved():
                                    self.board_array[self.x][self.y].has_moved()

                                #if double jump
                                if dest[Y] == self.y - 2 or dest[Y] == self.y + 2:
                                    self.board_array[self.x][self.y].set_double_jumped(True)

                                #if promotion
                                if dest[Y] == 0 or dest[Y] == 7:
                                    self.promotion(self.board_array, (self.x, self.y))

                                #if en passant
                                elif type(self.board_array[dest[X]][dest[Y] - 1 * self.player_factor]) == Pawn and self.board_array[dest[X]][dest[Y] - 1 * self.player_factor].get_double_jumped():
                                    if self.board_array[dest[X]][dest[Y] - 1 * self.player_factor].is_black() != self.black_turn:
                                        score.update(self.board_array[dest[X]][dest[Y] - 1 * self.player_factor].get_points(), self.board_array[dest[X]][dest[Y] - 1 * self.player_factor].get_file())
                                        self.board_array[dest[X]][dest[Y] - 1 * self.player_factor] = None

                            #updating score:
                            if self.board_array[dest[X]][dest[Y]] is not None:
                                score.update(self.board_array[dest[X]][dest[Y]].get_points(), self.board_array[dest[X]][dest[Y]].get_file())
                            #replacing values on board
                            self.board_array[dest[X]][dest[Y]] = self.board_array[self.x][self.y]
                            self.board_array[self.x][self.y] = None

                            return True
                        elif self.board_array[dest[X]][dest[Y]] is not None and self.board_array[dest[X]][dest[Y]].is_black() == self.black_turn:
                            if self.black_turn:
                                self.board.print_board_black(False)
                            else:
                                self.board.print_board_white(False)
                            pygame.display.update()
                            return False
            pygame.display.update()
                            
    def print_possible_moves(self):
        if self.black_turn:
            x = 7 - self.x
            y = 7 - self.y
        else:
            x = self.x
            y = self.y
        pygame.draw.rect(self.surface, OUTLINE_COL, (x * SQUARE , y * SQUARE + 48, SQUARE, SQUARE + 2), 4)
        for dest in self.possible_piece_dest:
            x_dest = dest[X]
            y_dest = dest[Y]
            b_dest_x = 7 - x_dest
            b_dest_y = 7 - y_dest
            if self.board_array[x_dest][y_dest] is None and not self.black_turn:
                pygame.draw.circle(self.surface, DOT_COL, (x_dest * SQUARE + SQUARE/2 , y_dest * SQUARE + SQUARE/2 + 50), 20, 0)
            elif self.board_array[x_dest][y_dest] is not None and not self.black_turn:
                pygame.draw.circle(self.surface, KILL_COL, (x_dest * SQUARE + SQUARE/2 , y_dest * SQUARE + SQUARE/2 + 50), 20, 0)
            elif self.board_array[x_dest][y_dest] is None and self.black_turn:
                pygame.draw.circle(self.surface, DOT_COL, (b_dest_x * SQUARE + SQUARE/2 , b_dest_y * SQUARE + SQUARE/2 + 50), 20, 0)
            else:
                pygame.draw.circle(self.surface, KILL_COL, (b_dest_x * SQUARE + SQUARE/2 , b_dest_y * SQUARE + SQUARE/2 + 50), 20, 0)
        pygame.display.update() 
    
    def mate_finder(self):
        game_state = (False, False)
        king_pos = (None, None)
        is_sim = True
        possible_enemy_dest = board_enemy_search(is_sim, self.black_turn, self.board_array, self.player_factor)
        if len(self.possible_friendly_dest) == 0:
            for j in range(8):
                for i in range(8):
                    if type(self.board_array[i][j]) is King and self.board_array[i][j].is_black() == self.black_turn:
                        king_pos = (i, j)
            if king_pos in possible_enemy_dest:
                game_state = (True, False)
            else:
                game_state = (True, True)
        return game_state

    def promotion(self, board_array, orig):
        in_promotion = True
        #print the selector
        if self.black_turn:
            self.board.print_board_black(True)
            pieces = [B_QUEEN, B_BISHOP, B_ROOK, B_KNIGHT]
        else: 
            self.board.print_board_white(True)
            pieces = [W_QUEEN, W_BISHOP, W_ROOK, W_KNIGHT]
        i = 0
        for piece in pieces:
            self.image = pygame.image.load(piece)
            if piece == pieces[1] or piece == pieces[2]:
                self.surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width() / 5), int(self.image.get_height() / 5))),
                            ((400 + i*50), 7))
            else:
                self.surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width() / 5), int(self.image.get_height() / 5))),
                            ((400 + i*50), 5))
            i += 1
        #replace board[orig] with the selected piece
        pygame.display.update()
        while(in_promotion):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if colision(PROMOTION_FRAME, mouse_pos):
                        pos_x = mouse_pos[X]//50
                        if pos_x == 8:
                            board_array[self.x][self.y] = Queen(self.black_turn, self.surface)
                        elif pos_x == 9:
                            board_array[self.x][self.y] = Bishop(self.black_turn, self.surface)
                        elif pos_x == 10:
                            board_array[self.x][self.y] = Rook(self.black_turn, self.surface)
                        elif pos_x == 11:
                            board_array[self.x][self.y] = Knight(self.black_turn, self.surface)
                        in_promotion = False
            pygame.display.update()
                        



########################################################################################################################################

class Score:

    def __init__(self, surface, black):
        self.black = black
        self.surface = surface
        self.score = 0
        self.trophies = []

    def update(self, points, piece):
        self.score += points
        self.trophies.append(piece)


    def print(self, black_turn):
        if (self.black and black_turn) or (not self.black and not black_turn):
            y_score = 1012
            y_pos = 1054
        else:
            y_score = 5
            y_pos = 50

        font = pygame.font.SysFont(None, 40)
        points_msg = font.render("×" + str(self.score), True, FONT_COLOR)
        self.surface.blit(points_msg, (10, y_score + 10))
        i = 1
        for piece in self.trophies:
            self.image = pygame.image.load(piece)
            self.surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width() / 5), int(self.image.get_height() / 5))),
                            ((20 + i*40), y_pos - self.image.get_height() / 5))
            i += 1

        pygame.display.update()

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
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if colision(PLAY_BUTTON[POS], mouse_pos):
                        in_menu = self.in_game()
                        self.draw_menu()
                    elif colision(QUIT_BUTTON[POS], mouse_pos):
                        in_menu = False
            pygame.display.update()

    def in_game(self):
        in_game = True
        in_menu = True
        black_turn = False
        changed = False
        check_mate = False
        stale = False
        black_score = Score(self.surface, True)
        white_score = Score(self.surface, False)
        board = Board(self.surface, black_score, white_score)
        while in_game:
            #impression initial du tour
            move_done = False
            if black_turn:
                board.print_board_black(False)
                score = black_score
            else:
                board.print_board_white(False)
                score = white_score
            pygame.display.update()
            #sequence de mouvement
            move = Move(self.surface, board, black_turn)
            while not move_done:
                game_state = move.mate_finder()
                if game_state[0]:
                    if game_state[1]:
                        stale = True
                    else:
                        check_mate = True
                    break
                if not changed:
                    if not move.validation():
                        in_game = False
                        break
                else:
                    move.revalidation()
                move.print_possible_moves()
                move_done = move.execution(score)  
                if move_done == None:
                    in_game = False
                    break
                changed = not move_done    

            if check_mate:
                self.print_win(not black_turn, board)
                exited = False
                while not exited:
                    time.sleep(0.1)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                exited = True
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            if colision(MENU_BUTTON, mouse_pos):
                                exited = True
                    pygame.display.update()
                break
            
            if stale:
                self.print_stale(not black_turn, board)
                exited = False
                while not exited:
                    time.sleep(0.1)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                exited = True
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            if colision(MENU_BUTTON, mouse_pos):
                                exited = True
                    pygame.display.update()
                break

            #impression du movement 
            if in_game:      
                if black_turn:
                    board.print_board_black(False)
                else:
                    board.print_board_white(False)
                pygame.display.update()
                black_turn = not black_turn
                time.sleep(0.5)

        return in_menu
    
    def print_win(self, black, board):
        board_array = board.get_board()
        for j in range(8):
            for i in range (8):
                if type(board_array[i][j]) is King and board_array[i][j].is_black() != black:
                    font = pygame.font.SysFont(None, 50)
                    mate_symb = font.render("#", True, KILL_COL)
                    self.surface.blit(mate_symb, (120 * i + 90, 120 * j + 55))
                    pygame.draw.rect(self.surface, KILL_COL, (i * SQUARE , j * SQUARE + 48, SQUARE, SQUARE + 2), 4)
        pygame.display.update()

    def print_stale(self, black, board):
        board_array = board.get_board()
        for j in range(8):
            for i in range (8):
                if type(board_array[i][j]) is King and board_array[i][j].is_black() != black:
                    font = pygame.font.SysFont(None, 30)
                    mate_symb = font.render("½-½", True, KILL_COL)
                    self.surface.blit(mate_symb, (120 * i + 73, 120 * j + 55))
                    pygame.draw.rect(self.surface, KILL_COL, (i * SQUARE , j * SQUARE + 48, SQUARE, SQUARE + 2), 4)
        pygame.display.update()

    def draw_menu(self):
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

def is_in_bounds(x, y):
    return x >= 0 and x <= 7 and y >=0 and y <= 7

def board_enemy_search(is_sim, black_turn, board_array, player_factor):
    possible_dest = []
    for j in range(8):
        for i in range(8):
            if board_array[i][j] is not None and board_array[i][j].is_black() != black_turn:
                    if type(board_array[i][j]) != Pawn:
                        possible_dest += board_array[i][j].possible_dest_finder(board_array, (i, j), is_sim)
                    else:
                        possible_dest += enemy_pawn_possible_attacks(player_factor, i, j)
    return possible_dest

def board_friendly_search(is_sim, black_turn, board_array):
    possible_dest = []
    for j in range(8):
        for i in range(8):
            if board_array[i][j] is not None and board_array[i][j].is_black() == black_turn:
                possible_dest += board_array[i][j].possible_dest_finder(board_array, (i, j), is_sim)
                if type(board_array[i][j]) is Pawn and board_array[i][j].get_double_jumped():
                        board_array[i][j].set_double_jumped(False)
    return possible_dest

def enemy_pawn_possible_attacks(player_factor, i, j):
        possible_attacks = []
        x_1 = i + 1 * player_factor
        x_2 = i - 1 * player_factor
        y = j - 1 * player_factor
        if is_in_bounds(x_1, y):
            possible_attacks.append((x_1, y))
        if is_in_bounds(x_2, y):
            possible_attacks.append((x_2, y))
        return possible_attacks

def is_safe(orig, x_dest, y_dest, board_array, black_turn, player_factor):
    is_sim = True
    is_safe = True
    dest_piece = board_array[x_dest][y_dest]
    board_array[x_dest][y_dest] = board_array[orig[X]][orig[Y]]
    board_array[orig[X]][orig[Y]] = None
    possible_checks = board_enemy_search(is_sim, black_turn, board_array, player_factor)
    for dest in possible_checks:
        if type(board_array[dest[X]][dest[Y]]) is King and board_array[dest[X]][dest[Y]].is_black() == black_turn:
            is_safe = False
            break
    board_array[orig[X]][orig[Y]] = board_array[x_dest][y_dest]
    board_array[x_dest][y_dest] = dest_piece
    return is_safe

def quit():
    pygame.quit()
    exit(0)

game = Game()
game.in_menu()
pygame.quit()
exit(0)