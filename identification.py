import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import os
import numpy as np


def identify(imagelist, folder_path):
    for image in imagelist:
        img = cv2.imread(image.data["File Path"])
        image_edit=img.copy()
        image_edit[850:len(image_edit), 0:len(image_edit[0])] = 0

        # apply gamma correction and show the images
        image_edit = adjust_gamma(image_edit, gamma=5.0)

        image_hsv = cv2.cvtColor(image_edit, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 15, 15])
        upper_red = np.array([15, 255, 255])
        mask_red1 = cv2.inRange(image_hsv, lower_red, upper_red)

        lower_red2 = np.array([160, 15, 15])
        upper_red2 = np.array([179, 255, 255])
        mask_red2 = cv2.inRange(image_hsv, lower_red2, upper_red2)

        lower_blue = np.array([105, 25, 25])
        upper_blue = np.array([130, 255, 255])
        mask_blue = cv2.inRange(image_hsv, lower_blue, upper_blue)

        lower_yellow = np.array([25, 30, 30])
        upper_yellow = np.array([35, 255, 255])
        mask_yellow = cv2.inRange(image_hsv, lower_yellow, upper_yellow)

        mask = cv2.bitwise_or(mask_red1, mask_red2)
        mask = cv2.bitwise_or(mask, mask_blue)
        mask = cv2.bitwise_or(mask, mask_yellow)

        result = cv2.bitwise_and(image_edit,image_edit, mask= mask)
        mask_smooth = cv2.bilateralFilter(mask, 9, 75, 75)
        mask_edge = cv2.Canny(mask_smooth, 50, 200)

        # finde Konturen in der Maske, die nur noch zeigt, wo gelbe Pixel sind:
        #_, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # suche die größte Kontur heraus (diese ist höchst wahrscheinlich der Tennisball)
        # dazu nehmen wir die Fläche der Kontur:
        # if len(contours) > 0:
        #    schild = max(contours, key=cv2.contourArea)

        # zeichne die Bounding box des Tennisballs in das Video-Bild ein:
        #x, y, w, h = cv2.boundingRect(schild)
        #cv2.rectangle(image_edit, (x, y), (x+w, y+h), (0, 255, 0), thickness=3)

        

        template = cv2.imread('kreis.jpg', 0)
        w, h = template.shape[::-1]
        template = cv2.Canny(template, 50, 200)

        result = cv2.matchTemplate(mask, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img, top_left, bottom_right, 255, 2)

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
