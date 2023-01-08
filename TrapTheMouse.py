import pygame, numpy as np, sys, math, random
from hexagon import Hexagon

pygame.init()

BACKGROUND = (21,76,121)
TILE = (56,93,56)
HIGHLIGHTEDTILE = (82,97,82)
DESTROYEDTILE = (0,0,0)
WINTEXT = (178,151,0)
LOSETEXT = (238,75,43)
ENDGAMETEXTBCK = (200,200,200)
SCREENWIDTH = 750
SCREENHEIGHT = 700
BOARDSHAPE = (11,11)
HEXRADIUS = 30
HEXMINIMALDISTANCE = HEXRADIUS / 2 * math.sqrt(3)

def get_index_of_neighbours(index):
    left = index - 1
    right = index + 1
    if index % 22 < 11:
        up_left = index - 12
        up_right = index - 11
        down_left = index + 10
        down_right = index + 11
    else:
        up_left = index - 11
        up_right = index - 10
        down_left = index + 11
        down_right = index + 12
    
    if index < 11 or index % 22 == 0:
        up_left = -2
    if index < 11 or index % 22 == 21:
        up_right = -2
    if index % 11 == 0:
        left = -2
    if index % 11 == 10:
        right = -2
    if index > 109 or index % 22 == 0:
        down_left = -2
    if index > 109 or index % 22 == 21:
        down_right = -2
    
    return up_left, left, down_left, down_right, right, up_right

def get_moves(board, index):
    moves = list(get_index_of_neighbours(index))
    
    for index in range(6):
        if moves[index] > -1:
            if board[moves[index]].destroyed == 1:
                moves[index] = -1 
    return moves            
    

def initialize_board(board):
    for index1 in  range(11):
        for index2 in range(11):
            if index1 % 2 == 0:
                board.append(Hexagon(100 + index2 * HEXMINIMALDISTANCE * 2, 100 + index1 * 1.5 * HEXRADIUS, 0))
            else:
                board.append(Hexagon(100 + HEXMINIMALDISTANCE + index2 * HEXMINIMALDISTANCE * 2, 100 + 1.5 * HEXRADIUS + (index1 - 1) * 1.5 * HEXRADIUS, 0))

def initialize_broken_tiles(board):
    broken_tiles_nr = random.randint(5,15)
    for index in range(broken_tiles_nr):
        tile = random.randint(0, 120)
        if tile != 60:
            board[tile].destroy_hex()
            
def render(board, screen):
    clock.tick(60)

    screen.fill(BACKGROUND)
    for hex in board:
        hex.update_highlight(coursor_x, coursor_y)
        hex.render(screen)
    
    screen.blit( mouse_image, mouse_position )
    
    pygame.display.update()

def lose_game():
    global font
    text = font.render('You lost', True, LOSETEXT, ENDGAMETEXTBCK)
    textRect = text.get_rect()
    textRect.center = (375, 350)
    screen.blit(text, textRect)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    quit()

def win_game():
    global font
    text = font.render('You win!', True, WINTEXT, ENDGAMETEXTBCK)
    textRect = text.get_rect()
    textRect.center = (375, 350)
    screen.blit(text, textRect)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    quit()

def move_by_player(board, moves):
    asd

def move_by_c1(moves):
    move_to = moves[random.randint(0,5)]
    while move_to == -1:
        move_to = moves[random.randint(0,5)]
        
    return move_to

def move_by_c2(board, moves):
    asd

def move_by_c3(board, moves):
    asd
            
def move_mouse(board, game_mode):
    global mouse_index
    global mouse_position
    moves = get_moves(board, mouse_index)
    possible_moves = 0
    
    for move in moves:
        if move == -2:
            lose_game()
        elif move != -1:
            possible_moves = possible_moves + 1
    if possible_moves == 0:
        win_game()
    
    if game_mode == 0:
        move_to = move_by_player(board, moves)
    elif game_mode == 1:
        move_to = move_by_c1(moves)
    elif game_mode == 2:
        move_to = move_by_c2(board, moves)
    else:
        move_to = move_by_c3(board, moves)
        
    board[mouse_index].has_mouse = 0
    board[move_to].has_mouse = 1
    mouse_position = (board[move_to].center[0] - 20, board[move_to].center[1] - 20)
    mouse_index = move_to
    

GameRunning = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Trap the Mouse')
font = pygame.font.SysFont('arial', 64)

argument = sys.argv[1]
if argument == "human":
    game_mode = 0
elif argument == "computer1":
    game_mode = 1
elif argument == "computer2":
    game_mode = 2
elif argument == "computer3":
    game_mode = 3
else:
    print("Argument in not adequate; try human for a human opponent, or computer1-3 for an AI opponent.")
    quit()

board = []
initialize_board(board)
initialize_broken_tiles(board)

mouse_image = pygame.image.load("Assets/mouse.png").convert_alpha()
mouse_position = (board[60].center[0] - 20, board[60].center[1] - 20)
mouse_index = 60
board[mouse_index].has_mouse = 1

while GameRunning:
    coursor_x, coursor_y = pygame.mouse.get_pos()
    player_turn = 1
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            GameRunning = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for hex in board:
                if hex.inside_point(coursor_x, coursor_y) and hex.has_mouse == 0 and hex.destroyed == 0:
                    hex.destroy_hex()
                    player_turn = 0

    if player_turn == 0:
        move_mouse(board)

    render(board, screen)    
