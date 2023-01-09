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
    broken_tiles_nr = random.randint(10,15)
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
    global game_mode
    if game_mode == 0:
        text = font.render('Player 2 Wins!', True, LOSETEXT, ENDGAMETEXTBCK)
    else:
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
    global game_mode
    if game_mode == 0:
        text = font.render('Player 1 Wins!', True, WINTEXT, ENDGAMETEXTBCK)
    else:
        text = font.render('You win!', True, WINTEXT, ENDGAMETEXTBCK)
    textRect = text.get_rect()
    textRect.center = (375, 350)
    screen.blit(text, textRect)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    quit()

def move_by_player(board, moves):
    while 1:
        coursor_x, coursor_y = pygame.mouse.get_pos()
        render(board, screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for move in moves:
                    if move != -2 and move != -1:
                        if board[move].inside_point(coursor_x, coursor_y):
                            move_to = move
                            return move_to

def move_by_c1(moves):
    move_to = moves[random.randint(0,5)]
    while move_to == -1:
        move_to = moves[random.randint(0,5)]
        
    return move_to

def move_by_c2(board, mouse_index):
    moves = get_moves(board, mouse_index)
    
    global visited_nodes
    global nodes_to_visit
    
    visited_nodes.clear()
    nodes_to_visit.clear()
    
    visited_nodes.append(mouse_index)
    
    for move in moves:
        if move != -1:
            nodes_to_visit.append(move)
            
    found_exit = 0
    
    while len(nodes_to_visit) > 0 and found_exit == 0:
        moves = get_moves(board, nodes_to_visit[0])
        visited_nodes.append(nodes_to_visit[0])
        nodes_to_visit.pop(0)
        
        for move in moves:
            move_is_made = 0
            if move in visited_nodes or move in nodes_to_visit:
                move_is_made = 1
            if move == -2 and move_is_made == 0:
                found_exit = 1
                break
            if move != -1 and move_is_made == 0:
                nodes_to_visit.append(move)
    
    end_point = visited_nodes[len(visited_nodes) - 1]
    
    print(end_point)
    
    moves = get_moves(board, mouse_index)
    move_value = [0,0,0,0,0,0]
    
    
    for index in range(6):
        if moves[index] == -1:
            move_value[index] = -999
    
    end_point_x = end_point % 11 + 1
    end_point_y = (end_point - end_point % 11) // 11 + 1
    mouse_x = mouse_index % 11 + 1
    mouse_y = (mouse_index - mouse_index % 11) // 11 + 1
    
    move_value[0] = move_value[0] + ( mouse_x - end_point_x ) / 2 + ( mouse_y - end_point_y )
    move_value[2] = move_value[2] + ( mouse_x - end_point_x ) / 2 + ( end_point_y - mouse_y )
    move_value[3] = move_value[3] + ( end_point_x - mouse_x ) / 2 + ( end_point_y - mouse_y )
    move_value[5] = move_value[5] + ( end_point_x - mouse_x ) / 2 + ( mouse_y - end_point_y )
    move_value[1] = move_value[1] + ( mouse_x - end_point_x )
    move_value[4] = move_value[4] + ( end_point_x - mouse_x )
    
    print(move_value)
    print(moves[move_value.index(max(move_value))])
    return moves[move_value.index(max(move_value))]

def move_by_c3(board, mouse_index):
    moves = get_moves(board, mouse_index)
    
    global visited_nodes
    global nodes_to_visit
    
    visited_nodes.clear()
    nodes_to_visit.clear()
    
    visited_nodes.append(mouse_index)
    
    for move in moves:
        if move != -1:
            nodes_to_visit.append(move)
            
    found_exit = 0
    
    while len(nodes_to_visit) > 0 and found_exit == 0:
        moves = get_moves(board, nodes_to_visit[0])
        visited_nodes.append(nodes_to_visit[0])
        nodes_to_visit.pop(0)
        
        for move in moves:
            move_is_made = 0
            if move in visited_nodes or move in nodes_to_visit:
                move_is_made = 1
            if move == -2 and move_is_made == 0:
                found_exit = 1
                break
            if move != -1 and move_is_made == 0:
                nodes_to_visit.append(move)
    
    end_point = visited_nodes[len(visited_nodes) - 1]
    
    print(end_point)
    
    moves = get_moves(board, mouse_index)
    move_value = [0,0,0,0,0,0]
    
    for index_0 in range(6):
        if moves[index_0] != -1:
            moves_next_turn = get_moves(board, moves[index_0])
            for index in range(6):
                if moves_next_turn[index] == -1 and moves_next_turn[(index + 1) % 6] == -1 and moves_next_turn[(index + 2) % 6] == -1 and moves_next_turn[(index + 3) % 6] == -1:
                    move_value[index_0] = -999
    
    for index in range(6):
        if moves[index] == -1:
            move_value[index] = -999
    
    end_point_x = end_point % 11 + 1
    end_point_y = (end_point - end_point % 11) // 11 + 1
    mouse_x = mouse_index % 11 + 1
    mouse_y = (mouse_index - mouse_index % 11) // 11 + 1
    
    move_value[0] = move_value[0] + ( mouse_x - end_point_x ) / 2 + ( mouse_y - end_point_y )
    move_value[2] = move_value[2] + ( mouse_x - end_point_x ) / 2 + ( end_point_y - mouse_y )
    move_value[3] = move_value[3] + ( end_point_x - mouse_x ) / 2 + ( end_point_y - mouse_y )
    move_value[5] = move_value[5] + ( end_point_x - mouse_x ) / 2 + ( mouse_y - end_point_y )
    move_value[1] = move_value[1] + ( mouse_x - end_point_x )
    move_value[4] = move_value[4] + ( end_point_x - mouse_x )
    
    print(move_value)
    print(moves[move_value.index(max(move_value))])
    return moves[move_value.index(max(move_value))]
            
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
        move_to = move_by_c2(board, mouse_index)
    else:
        move_to = move_by_c3(board, mouse_index)
        
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
exits = [0,1,2,3,4,11,22,33,44,55,66,77,88,99,110,111,112,113,114,115,116,117,118,119,120,109,98,87,76,65,54,43,32,21,10,9,8,7,6,5]
visited_nodes = []
nodes_to_visit = []

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
        move_mouse(board, game_mode)

    render(board, screen)    
