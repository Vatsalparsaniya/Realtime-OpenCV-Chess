import numpy as np
import chess
# send_data(512,512,512,600)

box_angle = np.zeros((64,5),dtype=int)
outside_angle = np.zeros((8,5),dtype=int)
outside_number = 0
def map_move_to_number(move):
    map_num = 0
    for i in "12345678":
        for j in "abcdefgh":
            if move == str(j)+str(i):
                return map_num
            else:
                map_num += 1

def set_arm():
    angle_1 = "512"
    angle_2 = "512"
    angle_3 = "512"
    angle_4 = "512"
    angle_5 = "512"
    print("Arm is set to main position ")

def move_robotic_arm(move,board):
    
    board = chess.Board()
    fen_line = board.fen()

    # when destination box have alreay player
    if(board.piece_at(map_move_to_number(move[2:4])) is not None):
        # print(map_move_to_number(move[2:4]))
        box_number = map_move_to_number(move[2:4])
        angle_1 = box_angle[box_number][0]
        angle_2 = box_angle[box_number][1]
        angle_3 = box_angle[box_number][2]
        angle_4 = box_angle[box_number][3]
        angle_5 = box_angle[box_number][4]

        print("Set angles for take player from box ",box_number)
        set_arm()

        angle_1 = outside_angle[outside_number][0]
        angle_2 = outside_angle[outside_number][1]
        angle_3 = outside_angle[outside_number][2]
        angle_4 = outside_angle[outside_number][3]
        angle_5 = outside_angle[outside_number][4]

        print("Player put outside ")

        box_number = map_move_to_number(move[0:2])
        angle_1 = box_angle[box_number][0]
        angle_2 = box_angle[box_number][1]
        angle_3 = box_angle[box_number][2]
        angle_4 = box_angle[box_number][3]
        angle_5 = box_angle[box_number][4]

        print("Set angles for take player from box ",box_number)
        set_arm()

        box_number = map_move_to_number(move[2:4])
        angle_1 = box_angle[box_number][0]
        angle_2 = box_angle[box_number][1]
        angle_3 = box_angle[box_number][2]
        angle_4 = box_angle[box_number][3]
        angle_5 = box_angle[box_number][4]
        print("Set angles for take player from box ",box_number)

        set_arm()

    else:
        box_number = map_move_to_number(move[0:2])
        angle_1 = box_angle[box_number][0]
        angle_2 = box_angle[box_number][1]
        angle_3 = box_angle[box_number][2]
        angle_4 = box_angle[box_number][3]
        angle_5 = box_angle[box_number][4]

        print("Set angles for take player from box ",box_number)
        set_arm()

        box_number = map_move_to_number(move[2:4])
        angle_1 = box_angle[box_number][0]
        angle_2 = box_angle[box_number][1]
        angle_3 = box_angle[box_number][2]
        angle_4 = box_angle[box_number][3]
        angle_5 = box_angle[box_number][4]
        print("Set angles for take player from box ",box_number)

        set_arm()

board = chess.Board()
move = "a1a3"
move_robotic_arm(move,board)