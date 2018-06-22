import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import os
import numpy as np

from sklearn.cluster import MiniBatchKMeans


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
        img_blur = cv2.medianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),9)


        img_color_spread = img

        img_color_spread[:,:,0] = cv2.equalizeHist(img[:,:,0])
        img_color_spread[:,:,1] = cv2.equalizeHist(img[:,:,1]) 
        img_color_spread[:,:,2] = cv2.equalizeHist(img[:,:,2])

        image_color_spread_hsv = cv2.cvtColor(img_color_spread, cv2.COLOR_BGR2HSV)

        image_color_spread_s = image_color_spread_hsv[:,:,1]

        image_color_spread_s_blur = cv2.medianBlur(image_color_spread_s,9)





        circles = cv2.HoughCircles(image_color_spread_s_blur,cv2.HOUGH_GRADIENT,1,40,
                            param1=100,param2=40,minRadius=5,maxRadius=75)

        #print(circles)

        if circles is not None: 
        
            #print(circles)
            circles = np.uint64(np.around(circles))

            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

        
        #img=temp_match('achtung.jpg',(11,11,255),img,image_s,0.7)
        #img=temp_match('achtung2.jpg',(11,11,255),img,image_s,0.73)
        #    #img=temp_match('gebot.jpg',(255,11,11),img,image_s,0.875)
        #img=temp_match('stop.jpg',(255,11,255),img,image_s,0.85)
        #    #img=temp_match('haupt.jpg',(11,255,255),img,image_s,0.8)
        #img=temp_match('Vf_g.jpg',(11,255,11),img,image_s,0.7)
        

        
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


def temp_match(schild,farbe,img,img_s,thres):
    template = cv2.imread(schild)
    template_hsv = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)

    template_s = template_hsv[:,:,1]

    #template_matched = cv2.matchTemplate(image_s,template, cv2.TM_CCOEFF)
    template_matched = cv2.matchTemplate(img_s, template_s, cv2.TM_CCORR_NORMED)

    threshold = thres
    loc = np.where( template_matched >= threshold)
    
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + 50, pt[1] + 50), farbe, 2)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(template_matched)
    #print(max_val)

    #if max_val>0.700:
    #    top_left = max_loc
    #    bottom_right = (top_left[0] + 100, top_left[1] + 100)
    #    cv2.rectangle(img, top_left, bottom_right, farbe, 4)

    return img