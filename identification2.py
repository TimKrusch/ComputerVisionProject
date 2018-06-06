import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import os
import numpy as np


def identify2(imagelist, folder_path):
    for image in imagelist:
        img = cv2.imread(image.data["File Path"])
        image_edit=img.copy()
        image_edit[850:len(image_edit), 0:len(image_edit[0])] = 0

        # apply gamma correction and show the images
        image_edit = adjust_gamma(image_edit, gamma=5.0)

        image_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        image_s = image_hsv[:,:,1]

        image_s_blur = cv2.medianBlur(image_s,9)


        circles = cv2.HoughCircles(image_s_blur,cv2.HOUGH_GRADIENT,1,40,
                            param1=100,param2=40,minRadius=5,maxRadius=75)

        print(circles)

        if circles is not None:
        
            print(circles)
            #circles = np.uint64(np.around(circles))

            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)



        ret,thresh = cv2.threshold(image_s_blur,127,255,1)
        contours,h = cv2.findContours(thresh,1 ,1)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            if len(approx)==3:
                cv2.drawContours(img,[cnt],0,255,-1)


        cv2.imwrite(
            folder_path + "/" + image.data["Name"][:-4] + "-edit.png", img
        )
        image.data["Edit Img"] = folder_path + "/" + \
            image.data["Name"][:-4] + "-edit.png"

    return imagelist


def adjust_gamma(image, gamma):
    # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)
