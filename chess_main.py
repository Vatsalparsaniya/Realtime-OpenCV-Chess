###################################################################################
## Import Libraries
###################################################################################
import os
import chess
import chess.engine
import cv2
import numpy as np

###################################################################################
## Import files
###################################################################################
# from design import design
from detect_points import get_points
from read_warp_img import get_warp_img
from black_player import player_position
from color_calibration import color_calibration

###################################################################################
## Define Main Variables
###################################################################################
points = []    # contains chess board corners points
lower__w = []   # contains lower value for HSV of white player
upper__w = []   # contains upper  value for HSV of white player
lower__b = []   # contains lower value for HSV of black player
upper__b = []   # contains upper value for HSV of black player
boxes = np.zeros((8,8,4),dtype=int)    # contains top-left and bottom-right point of chessboard boxes
fen_line = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR' # fen line of chess board
board = chess.Board(fen=fen_line) # object of chess board
dir_path = os.path.dirname(os.path.realpath(__file__))+"/numpy_saved" # path of current directory
device = cv2.VideoCapture(1) # set devidce for read image (1: for tacking input from usb-webcam)
img_resize = (800,800) # set o/p image size
image = []
engine = chess.engine.SimpleEngine.popen_uci("stockfish-10-win\Windows\stockfish_10_x64.exe") # stockfish engine
chess_board = []   # it will store chess board matrix
player_bool_position =[]
bool_position = np.zeros((8,8),dtype=int)
number_to_position_map = []

###################################################################################
## Code For Run Program
###################################################################################
print("Enter Code for Special Run : ")
code = str(input())
dir_path += "/"+code
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

###################################################################################
## Define Functions
###################################################################################

## map function for map values for (0,0)-> (8,a) , (0,1)-> (8,b).... so on 
def map_function():
    map_position = {}
    x,y=0,0
    for i in "87654321":
        for j in "abcdefgh":
            map_position[j+i] = [x,y]
            y = (y+1)%8
        x = (x+1)%8
    np.savez(dir_path+"/map_position.npz",**map_position)
map_function()
map_position =np.load(dir_path+"/map_position.npz")   # map move values for (0,0)-> (8,a) , (0,1)-> (8,b).... so on


def fen2board(fen_line):
    chess_board = [] 
    current_player_bool_position = []
    for row in fen_line.split(' ')[0].split('/'):
        bool_row = []
        chess_row = []
        for cell in list(row):
            if cell.isnumeric():
                for i in range(int(cell)):
                    chess_row.append(str(1))
                    bool_row.append(0)
            else:
                chess_row.append(cell)
                bool_row.append(1)
        chess_board.append(chess_row)
        current_player_bool_position.append(bool_row)
    chess_board = np.array(chess_board)
    current_player_bool_position = np.array(current_player_bool_position)
    return chess_board,current_player_bool_position

 
def board2fen(chess_board):
    board_array = chess_board
    fen_line = ''
    count = 0
    for i in range(8):
        empty = 0
        for j in range(8):
            if board_array[i][j].isnumeric():
                empty+=1
            else:
                if empty != 0:
                    fen_line+= str(empty)+ str(board_array[i][j])
                    empty = 0
                else:
                    fen_line += str(board_array[i][j])
        if empty != 0:
            fen_line += str(empty)
        if count != 7:
            fen_line += str('/')
            count +=1
    fen_line += " w KQkq - 0 1"
    return fen_line

def map_function_for_number_2_position():
    str1 = "87654321"
    str2 = "abcdefgh"
    for i in range(8):
        temp=[]
        for j in range(8):
            temp.append(str(str2[j]+str1[i]))
        number_to_position_map.append(temp)
map_function_for_number_2_position()            

def rectContains(rect,mid_point):
    logic = rect[0]<mid_point[0]<rect[2] and rect[1]<mid_point[1]<rect[3]
    return logic

def nothing(X):
    pass
def thresold_calibreation(img):
    cv2.namedWindow("thresold_calibration")
    cv2.createTrackbar("thresold", "thresold_calibration", 0, 255, nothing)
    while True:
        t =  cv2.getTrackbarPos("thresold", "thresold_calibration")
        matrix,thresold = cv2.threshold(img,t,255,cv2.THRESH_BINARY_INV)
        cv2.imshow("thresold",thresold)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return t
            
###################################################################################
## camara position calibration
###################################################################################
while True:
    print("Do you want to set camara Position[y/n] : ",end=" ")
    answer = str(input())
    if answer == "y" or answer == "Y":
        print("Press q for exit : ")
        while True:
            ## show frame from camera and set positon by moving camera
            flag , img = device.read()
            img = cv2.resize(img,img_resize)
            if flag:
                cv2.imshow("Set camera position",img)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    cv2.destroyAllWindows()
                    break
        break
    elif answer == "n" or answer == "N":
        print("\nHope that camera position already set...\n")
        break
    else:
        print("Invalid Input ")



###################################################################################
## Image warp_presnpective
###################################################################################
while True:
    print("DO you want to warp prespective image[y/n] :",end=" ")
    answer = str(input())
    ret , img = device.read()
    img =   cv2.resize(img,(800,800))
    width,height = 800,800
    if answer == "y" or answer == "Y":
        warp_points = get_points(img,4)
        pts1 = np.float32([[warp_points[0][0],warp_points[0][1]],
                        [warp_points[1][0],warp_points[1][1]],
                        [warp_points[3][0],warp_points[3][1]],
                        [warp_points[2][0],warp_points[2][1]]])
        pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
        np.savez(dir_path+"/chess_board_warp_prespective.npz",pts1=pts1,pts2=pts2)
        result = get_warp_img(img,dir_path,img_resize)
        cv2.imshow("result",result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break
    elif answer == "n" or answer == "N":
        result = get_warp_img(img,dir_path,img_resize)
        cv2.imshow("result",result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break
    else:
        print("Enter valid input")


###################################################################################
## calibrate points for chess corners
###################################################################################
while True:
        print("do you want to calibrate new Points for corners [y/n]:",end=" ")
        ans = str(input())
        if ans == "y" or ans == "Y":
            ret , img = device.read()
            img =   cv2.resize(img,(800,800))
            img = get_warp_img(img,dir_path,img_resize)
            points = []
            for i in range(9):
                pt = get_points(img,9)
                points.append(pt)
            np.savez(dir_path+"/chess_board_points.npz",points=points)
            break
        elif ans == "n" or ans == "N":
            # do some work
            points = np.load(dir_path+'/chess_board_points.npz')['points']
            print("points Load successfully")
            break
        else:
            print("something wrong input")


###################################################################################
## Define Boxes
###################################################################################
for i in range(8):
    for j in range(8):
        boxes[i][j][0] = points[i][j][0]
        boxes[i][j][1] = points[i][j][1]
        boxes[i][j][2] = points[i+1][j+1][0]
        boxes[i][j][3] = points[i+1][j+1][1]

np.savez(dir_path+"/chess_board_Box.npz",boxes=boxes)

###################################################################################
## View Boxes
###################################################################################
while True:
    print("Do you want to see Boxex on Chess board [y/n]:",end=" ")
    ans = str(input())
    if ans == 'y' or ans == "Y":
        # show boxes
        ret , img = device.read()
        img =   cv2.resize(img,(800,800))
        img = get_warp_img(img,dir_path,img_resize)
        img_box = img.copy()
        for i in range(8):
            for j in range(8):
                box1 = boxes[i,j]
                cv2.rectangle(img_box, (int(box1[0]), int(box1[1])), (int(box1[2]), int(box1[3])), (255,0,0), 2)
                cv2.putText(img_box,"({},{})".format(i,j),(int(box1[2])-70, int(box1[3])-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
                cv2.imshow("img",img_box)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break
    elif ans == 'N' or ans == "n":
        print("ok, got it you don't want ot see boxes")
        break
    else:
        print("Enter valid input")


###################################################################################
## calibration thresold
###################################################################################

print("calibrate thresold :")
ret , img = device.read()
img =   cv2.resize(img,(800,800))
img = get_warp_img(img,dir_path,img_resize)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
thresold_value = thresold_calibreation(gray)
cv2.destroyAllWindows()
###################################################################################
## calibration color
###################################################################################
# while True:
#     print("Do you want to calibrate color [y/n] :",end=" ")
#     ans = str(input())
#     if ans == "y" or ans == "Y":
#         print("calibration for white :")
#         color_calibration(img,"w",dir_path)
#         lower__w =  np.load(dir_path+"/chess_w_color_points.npz")['lower']
#         upper__w = np.load(dir_path+"/chess_w_color_points.npz")['upper']
#         print("Done calibration for white")
#         print("calibration for black :")
#         color_calibration(img,"b",dir_path)
#         lower__b =  np.load(dir_path+"/chess_b_color_points.npz")['lower']
#         upper__b = np.load(dir_path+"/chess_b_color_points.npz")['upper']
#         print("Done calibration for black")
#         break
#     if ans == "n" or ans == "N":
#         lower__w =  np.load(dir_path+"/chess_w_color_points.npz")['lower']
#         upper__w = np.load(dir_path+"/chess_w_color_points.npz")['upper']
#         lower__b =  np.load(dir_path+"/chess_b_color_points.npz")['lower']
#         upper__b = np.load(dir_path+"/chess_b_color_points.npz")['upper']
#         print("color calibration successfully")
#         break
#     else:
#         print("something wrong input")

###################################################################################
## Start Game
###################################################################################
print ("New Game Start")

while not board.is_game_over():

    ## white turn 
    if board.turn:
        ret , img = device.read()
        img =   cv2.resize(img,(800,800))
        img = get_warp_img(img,dir_path,img_resize)

        chess_board,player_bool_position = fen2board(board.fen())
        result = engine.play(board, chess.engine.Limit(time=0.500))

        position1 = str(result.move)[0:2]
        position2 = str(result.move)[2:4]

        box_1_cordinate = map_position[position1]
        box_2_cordinate = map_position[position2]
        # print("box cordinate ",box_1_cordinate,box_2_cordinate)
        # print(chess_board)
        position1_box = boxes[box_1_cordinate[0]][box_1_cordinate[1]]
        position2_box = boxes[box_2_cordinate[0]][box_2_cordinate[1]]

        draw_img = img.copy()
        cv2.rectangle(draw_img,(position1_box[0],position1_box[1]),(position1_box[2],position1_box[3]),(0,0,255),3)
        cv2.rectangle(draw_img,(position2_box[0],position2_box[1]),(position2_box[2],position2_box[3]),(0,255,0),3)
        
        cv2.imshow("Game",draw_img)
        # print("player :",chess_board[box_1_cordinate[0]][box_1_cordinate[1]],"\nmoves from : ",position1,"\nmoves to : ",position2)
        board.push(result.move)
        print("press 'w' when player moved ")
        while True:
            if cv2.waitKey(1) == ord('w'):
                break
        print("Done White")
    ## black turn
    else:
        past_bool_position = np.zeros((8,8),dtype=int)
        current_bool_position = np.zeros((8,8),dtype=int)
        chess_board,bool_position = fen2board(board.fen())
        # result = engine.play(board, chess.engine.Limit(time=0.500))
        # board.push(result.move)
        # print(result.move)

        ret , img = device.read()
        img =   cv2.resize(img,(800,800))
        img = get_warp_img(img,dir_path,img_resize)
        cv2.imshow("Game",img)
        past_bool_position = player_position(img,thresold_value,boxes)

        print("Player time to move : ")
        print("press 'q' when player moved ")
        while True:
            if cv2.waitKey(1) == ord('q'):
                break

        ret , img = device.read()
        
        img =   cv2.resize(img,(800,800))
        img = get_warp_img(img,dir_path,img_resize)
        cv2.imshow("Game",img)
        current_bool_position = player_position(img,thresold_value,boxes)
        cv2.waitKey(0)

        difference_matrix = current_bool_position-past_bool_position
        position_of_negative = np.where(difference_matrix == -1)
        position_of_positive = np.where(difference_matrix == 1)
        print("Position of positive ",position_of_positive)
        print("Position of negative ",position_of_negative)

        if len(position_of_negative[0])==0:
            ## no changes
            print("there is no changes detacts  ")
        elif len(position_of_negative[0])==1:
            ## move 1 player
            player_moved = chess_board[position_of_negative[0][0]][position_of_negative[1][0]]
            chess_board[position_of_negative]=1
            chess_board[position_of_positive]=player_moved
            move_word = number_to_position_map[int(position_of_negative[0][0])][int(position_of_negative[1][0])]
            move_word+= number_to_position_map[int(position_of_positive[0][0])][int(position_of_positive[1][0])]
            print(move_word)
            position1 = str(move_word)[0:2]
            position2 = str(move_word)[2:4]

            box_1_cordinate = map_position[position1]
            box_2_cordinate = map_position[position2]
            position1_box = boxes[box_1_cordinate[0]][box_1_cordinate[1]]
            position2_box = boxes[box_2_cordinate[0]][box_2_cordinate[1]]

            draw_img = img.copy()
            cv2.rectangle(draw_img,(position1_box[0],position1_box[1]),(position1_box[2],position1_box[3]),(0,0,255),3)
            cv2.rectangle(draw_img,(position2_box[0],position2_box[1]),(position2_box[2],position2_box[3]),(0,255,0),3)
        
            cv2.imshow("Game",draw_img)
            cv2.waitKey(0)
            print(move_word)
            board.push(chess.Move.from_uci(str(move_word)))
            print("Done Black")
        else:
            #more then 1 player moved detected
            print("More then 1 playre detected")
            print("set player to this postion")
            print(board)



        # cv2.imshow("Game",img)
        # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # matrix,thresold = cv2.threshold(gray,32,255,cv2.THRESH_BINARY_INV)
        # contours,_= cv2.findContours(thresold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # required_contoures = []
        # required_contoures_mid_point = []
        # cnt_rectangle = []
        # for cnt in contours:
        #     area = cv2.contourArea(cnt)
        #     if(area > 800):
        #         (x, y, w, h) = cv2.boundingRect(cnt)
        #         required_contoures.append(cnt)
        #         required_contoures_mid_point.append([x+int(w/2),y+int(h/2)])
        #         cnt_rectangle.append([x,y,w,h])
        #         cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

        
        # for i in range(8):
        #     for j in range(8):
        #         for mid_point in required_contoures_mid_point:
        #             if(rectContains(boxes[i][j],mid_point)):
        #                 bool_position[i][j] = 1

        # chess_board,past_bool_position = fen2board(board.fen())
        # current_bool_position = bool_position
        # print(past_bool_position)
        # print(current_bool_position)
        # cv2.waitKey(0)
