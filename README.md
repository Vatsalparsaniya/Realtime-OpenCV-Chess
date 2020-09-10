# Realtime-OpenCV-Chess
♔♕♗♘♙♚♛♝♞♟♖♜

---

Human vs AI (Stockfish engine)

Camera captures the image of chessboard then the images analyzed using imageprocessing to identify the moves made by opponent and stockfish engine calculates the best possible move.

<img src="https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Images/Open-cv.png" width="48"> ![opencv](https://img.shields.io/badge/CV-Open--CV-green)|<img src="https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Images/Python3.jpg" width="55">![python](https://img.shields.io/badge/Py-Python3-blue)
:-------------------------:|:-------------------------:

# Youtube Video
[![check out my youtube video](https://img.youtube.com/vi/JnpxzLM8ht0/0.jpg)](https://youtu.be/JnpxzLM8ht0)|[![check out my youtube video](https://img.youtube.com/vi/PQk7sFsqaRQ/0.jpg)](https://youtu.be/PQk7sFsqaRQ)
:-------------------------:|:-------------------------:

# Image Transformation
| ![Input-Frame](https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Images/input-frame.png) | ![warp-perspective](https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Images/warpperspective.png) | ![locate-boxes](https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Images/locate-boxes.png) |
:-------------------------:|:-------------------------:|:-------------------------:
|Input-Frame|warp-perspective|locate-boxes|

# Method of Working
## Step - 1
Image1 : Image of Chess Board befor player move piece|Image2 : Image of Chess Board after player move piece
:-------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Method_working/Images/2.jpg)|![](https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Method_working/Images/3.jpg)

## step - 2
Difference of image by using function absdiff in CV2|Change Difference_image to Gray scale image
:-------------------------:|:-------------------------:
 diff = cv2.absdiff(image1,image2)|diff_gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)|
 <img src="https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Method_working/Images/Difference_image.jpg" alt="Difference_image" height="400" width="400"/>|<img src="https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Method_working/Images/Difference_GrayScale_image.jpg" alt="Difference_image" height="400" width="400"/>


## step - 3
Apply thresholding on Grayscale image| Find Contours on threshold image
:-------------------------:|:-------------------------:
 matrix,thresold = cv2.threshold(diff_gray,value,255,cv2.THRESH_BINARY)|cnts,_ = cv2.findContours(thresold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)|
 <img src="https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Method_working/Images/Threshold_image.jpg" alt="Difference_image" height="400" width="400"/>|<img src="https://raw.githubusercontent.com/Vatsalparsaniya/Realtime-OpenCV-Chess/master/Method_working/Images/show_Contours.jpg" alt="Difference_image" height="400" width="400"/>


# Main Variables 
Variables|Explain
:-------------------------:|:-------------------------:
<b>points</b> = []  |  # contains chess board corners points|
<b>boxes = np.zeros((8,8,4),dtype=int)</b>  |  # contains top-left and bottom-right point of chessboard boxes
<b>fen_line = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'</b>| # fen line of chess board
<b>board = chess.Board(fen=fen_line)</b>| # object of chess board
<b>dir_path = os.path.dirname(os.path.realpath(__file__))+"/numpy_saved"</b>| # path of current directory
<b>device = cv2.VideoCapture(1)</b> |# set devidce for read image (1: for tacking input from usb-webcam)
<b>img_resize = (800,800)</b>| # set o/p image size
<b>engine = chess.engine.SimpleEngine.popen_uci("stockfish-10-win\Windows\stockfish_10_x64.exe")</b>| # stockfish engine
<b>chess_board = []</b>| # it will store chess board matrix
<b>bool_position = np.zeros((8,8),dtype=int)</b>| # store bool matrix of Board
<b>number_to_position_map = []</b>|  # map move values for [0,0]-> (8,a) , [0,1]-> (8,b).... so on

# Main Functions
Function Name|Explain
:-------------------------:|:-------------------------:
<b>get_points(img,n)</b>|select n points on image by double click and returns list of selected points
<b>get_warp_img(img,dir_path,img_resize)</b>|return warp prespective of image taken by camera and resize it to img_resize value
<b>map_function()</b>|makes a dictonary to map values { "a8":[0,0],"b8":[0,1],.... so on }
<b>fen2board(fen_line)</b>|retuen a 8X8 matrix of chess player piece name and bool position
<b>board2fen(chess_board)</b>|return fen line of chess board
<b>map_function_for_number_2_position()</b>|makes a list for map values [0,0]="8a", [0,1]="8b",[0,2]="8c",... so on
<b>rectContains(rectangle,mid_point)</b>| logic function for checking given mid_point is inside the rectangle or not
<b>show_game(game_img,board,player_move)</b>|This function shows all game in proper format with plane turn, opponent's last move, current chess <b>board, red and green boxes on moved piece, etc.
<b>set_legal_positions(game_image,board,boxes)</b>| if Illegal move found in chess it shows last correct state of chess board


# Author

<table>
<tr>
<td>
     <img src="https://avatars2.githubusercontent.com/u/33985480?s=400&u=2455cd8723a36084ad2b515e89127c2c03e0abd0&v=4" width="180"/>
     
     Vatsal Parsaniya

<p align="center">
<a href = "https://github.com/Vatsalparsaniya"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/vatsal-parsaniya/"><img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/></a>
</p>
</td>
</tr> 
  </table>
