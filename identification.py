import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os

def identify(imagelist, folder_path):
    for image in imagelist:
        image_edit = cv2.imread(image.data["File Path"])
        cv2.imwrite(
            folder_path + "/" + image.data["Name"][:-4] + "-edit.png", image_edit
            )
        image.data["Edit Img"]=folder_path + "/" + image.data["Name"][:-4] + "-edit.png"

    return imagelist
