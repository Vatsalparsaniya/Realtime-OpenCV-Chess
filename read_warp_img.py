import cv2
import numpy as np

def get_warp_img(img,dir_path,img_resize):
    pts1 = np.load(dir_path+'/chess_board_warp_prespective.npz')['pts1']
    pts2 = np.load(dir_path+'/chess_board_warp_prespective.npz')['pts2']
    H,maks = cv2.findHomography(pts1,pts2)
    result = cv2.warpPerspective(img,H,img_resize)
    return result