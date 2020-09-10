import cv2
import numpy as np

def fen2board_black(fen_line):
    black_player_bool_position = []
    for row in fen_line.split(' ')[0].split('/'):
        bool_row = []
        for cell in list(row):
            if cell.isnumeric():
                for i in range(int(cell)):
                    bool_row.append(0)
            else:
                if cell.islower():
                    bool_row.append(1)
                else:
                    bool_row.append(0)
        black_player_bool_position.append(bool_row)
    black_player_bool_position = np.array(black_player_bool_position)
    return black_player_bool_position

def rectContains(rect,mid_point):
    logic = rect[0]<mid_point[0]<rect[2] and rect[1]<mid_point[1]<rect[3]
    return logic

def find_current_past_position(img_1,img_2,boxes,bool_position,FEN_line,chess_board,number_to_position_map,map_position):
    past_bool_position = bool_position
    current_bool_position = bool_position
    diff_position = np.zeros((8,8),dtype=int)
    past_black_bool_position = fen2board_black(FEN_line)

    image_diff = cv2.absdiff(img_1,img_2)
    # cv2.imshow("diff",image_diff)
    image_diff_gray = cv2.cvtColor(image_diff,cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray",image_diff_gray)
    matrix,thresold = cv2.threshold(image_diff_gray,10,255,cv2.THRESH_BINARY)
    # cv2.imshow("thre",thresold)
    cnts,_ = cv2.findContours(thresold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) >= 2:
        required_contoures_mid_point = []
        for c in cnts:
            area = cv2.contourArea(c)
            if area> 500:
                (x, y, w, h) = cv2.boundingRect(c)
                required_contoures_mid_point.append([x+int(w/2),y+int(h/2)])
                # cv2.rectangle(diff, (x, y), (x + w, y + h), (0, 0, 255), 2)

        flag = np.zeros((8,8),dtype=int)
        for i in range(8):
                for j in range(8):
                    for mid_point in required_contoures_mid_point:
                        if(rectContains(boxes[i][j],mid_point)) and flag[i][j]==0:
                            diff_position[i][j] = 2
                            flag[i][j]=1

        
        temp_matrix = past_black_bool_position - diff_position
        print(temp_matrix)
        position_of_past_black = np.where(temp_matrix == -1)
        position_of_new_black = np.where(temp_matrix == -2)

        player_moved = chess_board[position_of_past_black[0][0]][position_of_past_black[1][0]]
        chess_board[position_of_past_black]=1
        chess_board[position_of_new_black]=player_moved

        move_word = number_to_position_map[int(position_of_past_black[0][0])][int(position_of_past_black[1][0])]
        move_word+= number_to_position_map[int(position_of_new_black[0][0])][int(position_of_new_black[1][0])]

        position1 = str(move_word)[0:2]
        position2 = str(move_word)[2:4]

        box_1_cordinate = map_position[position1]
        box_2_cordinate = map_position[position2]
        
        position1_box = boxes[box_1_cordinate[0]][box_1_cordinate[1]]
        position2_box = boxes[box_2_cordinate[0]][box_2_cordinate[1]]

        draw_img = img_2.copy()
        cv2.rectangle(draw_img,(position1_box[0],position1_box[1]),(position1_box[2],position1_box[3]),(0,0,255),3)
        cv2.rectangle(draw_img,(position2_box[0],position2_box[1]),(position2_box[2],position2_box[3]),(0,255,0),3)

        return move_word,draw_img,1
    else:
        return " ",img_2,0

