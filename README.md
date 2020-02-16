# opencv-chess
Human vs AI (Stockfish engine)

Camera captures the image of chessboard then the imageis analyzed using imageprocessing to identify the moves made by opponent and stockfish engine calculates the best possible move.

<img src="Images/Open-cv.png" width="48"> ![opencv](https://img.shields.io/badge/CV-Open--CV-green)|<img src="Images/Python3.jpg" width="55">![python](https://img.shields.io/badge/Py-Python3-blue)
:-------------------------:|:-------------------------:

# Youtube Video
[![check out my youtube video](https://img.youtube.com/vi/v12ELMNIZVE/0.jpg)](https://www.youtube.com/watch?v=v12ELMNIZVE)|[![check out my youtube video](https://img.youtube.com/vi/e0FtXusMFTY/0.jpg)](https://www.youtube.com/watch?v=e0FtXusMFTY)
:-------------------------:|:-------------------------:

# Method of Working
## Step - 1
Image1 : Image of Chess Board befor player move piece|Image2 : Image of Chess Board after player move piece
:-------------------------:|:-------------------------:
![](Method_working/Images/2.jpg)|![](Method_working/Images/3.jpg)

## step - 2
Difference of image by using function absdiff in CV2|Change Difference_image to Gray scale image
:-------------------------:|:-------------------------:
 diff = cv2.absdiff(image1,image2)|diff_gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)|
 <img src="Method_working/Images/Difference_image.jpg" alt="Difference_image" height="400" width="400"/>|<img src="Method_working/Images/Difference_GrayScale_image.jpg" alt="Difference_image" height="400" width="400"/>


## Author

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
