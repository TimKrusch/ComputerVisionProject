from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk
import os
import shutil

from identification import identify

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Picture_Data(object):
    def __init__(self,name,filepath,gtfilepath,gtdata,edit_filepath):
        self.data = {"Name": name, "File Path": filepath, "GT File Path": gtfilepath , "GT Data": gtdata, "Edit Img":edit_filepath}
    #data = {"Name": "", "File Path": "", "GT File Path": "" , "GT Data": ""}


class myUI(Frame, metaclass=Singleton):

    def __init__(self):
        Frame.__init__(self)

        #variables
        self.gt_text_label = StringVar()
        self.pictures_data = []
        self.currentDisplayedResult = 1

        ###### define Window properties ######
        self.master.title("Projekt-Verkehrsschildererkennung")
        self.master.minsize(width = 1500, height = 700)
        self.master.configure(background="gray80")
        self.grid_rowconfigure(0, minsize=20)
        self.grid_rowconfigure(2, minsize=20)
        self.grid_rowconfigure(4, minsize=20)
        self.grid_rowconfigure(6, minsize=20)
        self.grid_rowconfigure(8, minsize=2500)
        self.grid_columnconfigure(0, minsize=40)
        self.grid_columnconfigure(2, minsize=40)
        self.grid_columnconfigure(4, minsize=40)
        self.grid_columnconfigure(6, minsize=40)
        self.grid(sticky=W+E+N+S)


        ###### define Window objects ######

        #Menu
        self.top_menu = Menu(self.master)      
        self.master.config(menu = self.top_menu)
        self.FileMenu = Menu(self.top_menu)
        self.top_menu.add_cascade(label = "File", menu=self.FileMenu)
        self.FileMenu.add_command(label = "Add File", command=self.addFile)
        self.FileMenu.add_command(label = "Open Folder", command=self.openFolder)

        self.EditMenu = Menu(self.top_menu)
        self.top_menu.add_cascade(label = "Edit", menu=self.EditMenu)
        self.EditMenu.add_command(label = "Find Signs", command=self.identify_signs)

        self.CloseMenu = Menu(self.top_menu)
        self.top_menu.add_cascade(label = "Beenden", menu=self.CloseMenu)
        self.CloseMenu.add_command(label = "Close", command=self.closeEvent)


        #Labels
        self.original_picture_Label = Label(self.master, image = PhotoImage(file="gray.png"))
        self.original_picture_Label.grid(row=1,column=1,sticky=W)

        self.edited_picture_Label = Label(self.master, image = PhotoImage(file="gray.png"))
        self.edited_picture_Label.grid(row=1,column=3)

        self.gt_picture_Label = Label(self.master, image = PhotoImage(file="gray.png"))
        self.gt_picture_Label.grid(row=1,column=5,sticky=E)

        self.row0_label = Label(self.master, background="gray80")
        self.row0_label.grid(row=0,column=0,sticky=N+S)
        self.row2_label = Label(self.master, background="gray80")
        self.row2_label.grid(row=2,column=0,sticky=N+S)
        self.column0_label = Label(self.master, background="gray80")
        self.column0_label.grid(row=1,column=0,sticky=N+S)
        self.column2_label = Label(self.master, background="gray80")
        self.column2_label.grid(row=1,column=2,sticky=N+S)
        self.column4_label = Label(self.master, background="gray80")
        self.column4_label.grid(row=1,column=4,sticky=N+S)
        self.column6_label = Label(self.master, background="gray80")
        self.column6_label.grid(row=1,column=6,sticky=N+S)
        
        self.gt_text_label = Label(self.master, text="",background="gray80")
        self.gt_text_label.grid(row = 3, column=5)
        if len(self.pictures_data)==0:
            self.filename_label = Label(self.master, text="",background="gray80")
            self.filename_label.grid(row = 0, column=1,sticky=W+E)
            
        for x in self.pictures_data:
            print(x.data)


    def addFile(self):        
        
        self.filePath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
        edit_filepath = ""

        if self.filePath.endswith("_gt.png"):
            Name = self.filePath.rpartition("/")[2][:5] + ".png"
            FilePath = self.filePath.rpartition("/")[0][:-3] + "/"+ Name
            GTFilePath = self.filePath
            GTData = ""

            fobj = open(self.filePath.rpartition("/")[0].rpartition("/")[0] + "/gt_train.txt")
            for line in fobj:
                if line.startswith(Name):
                    GTData = GTData + line
            fobj.close()
            
            picture = Picture_Data(Name,FilePath,GTFilePath,GTData,edit_filepath)

        else:

            Name = self.filePath.rpartition("/")[2]
            FilePath = self.filePath
            GTFilePath = self.filePath.rpartition("/")[0] + "_gt/"+ Name[:-4] + "_gt.png"
            GTData = ""

            fobj = open(self.filePath.rpartition("/")[0].rpartition("/")[0] + "/gt_train.txt")
            for line in fobj:
                if line.startswith(Name):
                    GTData = GTData + line
            fobj.close()
            
            picture = Picture_Data(Name,FilePath,GTFilePath,GTData,edit_filepath)

        self.pictures_data.append(picture)

        if len(self.pictures_data) > 0:
            self.display_result(self.pictures_data[0])


    def openFolder(self):

        self.pictures_data = []
        edit_filepath = ""

        folderPath = filedialog.askdirectory()
        image_listing = os.listdir(folderPath)
        folder_pictures_data = []

        if folderPath.endswith("_gt"):
            for image in image_listing:
                Name = image[:5] + ".png"
                FilePath = folderPath[:-3] + image[:5] + ".png"
                GTFilePath = folderPath + "/" + image
                GTData = ""

                fobj = open(folderPath.rpartition("/")[0]+"/gt_train.txt")
                for line in fobj:
                    if line.startswith(Name):
                        GTData = GTData + line
                fobj.close()

                folder_pictures_data.append(Picture_Data(Name,FilePath,GTFilePath,GTData,edit_filepath))
                
        else:
            for image in image_listing:
                
                Name = image
                FilePath = folderPath + "/" + image
                GTFilePath = folderPath + "_gt/" + image[:5] + "_gt.png"
                GTData = ""

                fobj = open(folderPath.rpartition("/")[0]+"/gt_train.txt")
                for line in fobj:
                    if line.startswith(Name):
                        GTData = GTData + line
                fobj.close()

                folder_pictures_data.append(Picture_Data(Name,FilePath,GTFilePath,GTData,edit_filepath))
                

        self.pictures_data = folder_pictures_data

        if len(self.pictures_data) > 0:
            self.display_result(self.pictures_data[0])  


    def display_result(self, Img):
        #generate Image from filepath
        image = Image.open(Img.data["File Path"])
        image.thumbnail((500, 376), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)

        self.original_picture2 = Canvas(self.master, width=500,height=376)
        self.original_picture2.create_image(0, 0, anchor=NW, image=image)
        self.original_picture2.image = image
        self.original_picture2.grid(row=1,column=1,sticky=W)


        image_gt = Image.open(Img.data["GT File Path"])
        image_gt.thumbnail((500, 376), Image.ANTIALIAS)
        image_gt = ImageTk.PhotoImage(image_gt)

        #draw Ground Truth Image
        self.gt_picture2 = Canvas(self.master, width=500,height=376)
        self.gt_picture2.create_image(0, 0, anchor=NW, image=image_gt)
        self.gt_picture2.image = image_gt
        self.gt_picture2.grid(row=1,column=5,sticky=W)


        if Img.data["Edit Img"] != "" : 
            image_edit = Image.open(Img.data["Edit Img"])
            image_edit.thumbnail((500, 376), Image.ANTIALIAS)
            image_edit = ImageTk.PhotoImage(image_edit)

            self.edited_picture_Label2 = Canvas(self.master, width=500,height=376)
            self.edited_picture_Label2.create_image(0, 0, anchor=NW, image=image_edit)
            self.edited_picture_Label2.image = image_edit
            self.edited_picture_Label2.grid(row=1,column=3,sticky=W)




        #draw Ground Truth Data
        self.gt_text_label.configure(text="Ground Truth Data :\n"+Img.data["GT Data"])

        #draw Button for iteration back through the images
        if self.currentDisplayedResult > 1:
            self.back = Button(self.master, text="<", command=lambda: self.switchDisplayedImage(-1))
            self.back.grid(row=0, column=1,sticky=W)

        #draw Button for iteration forward through the images
        if self.currentDisplayedResult < len(self.pictures_data):
            self.forth = Button(self.master, text=">", command=lambda: self.switchDisplayedImage(1))
            self.forth.grid(row=0, column=1,sticky=E)

        #draw label that shows the image-name we are currently seeing
        self.filename_label.configure(text="  "+Img.data["Name"],background="grey94")
    
    def switchDisplayedImage(self, imageOffset):
        if (
                (self.currentDisplayedResult + imageOffset) <= len(self.pictures_data)
                and (self.currentDisplayedResult + imageOffset) >= 1
            ):

            self.currentDisplayedResult += imageOffset
            self.display_result(self.pictures_data[self.currentDisplayedResult-1])


    def identify_signs(self):
        
        edit_folder_path = self.pictures_data[0].data["File Path"].rpartition("/")[0].rpartition("/")[0]+"/edit_folder"
        os.mkdir(edit_folder_path)

        identify(self.pictures_data,edit_folder_path)
        
        self.display_result(self.pictures_data[self.currentDisplayedResult-1])

    def closeEvent(self):
        
        if len(self.pictures_data) > 0:
            if self.pictures_data[0].data["Edit Img"] != "": 
                result = messagebox.askquestion("Delete", "Delete the Edit-Images?", icon='warning')
                if result == 'yes':
                    shutil.rmtree(self.pictures_data[0].data["File Path"].rpartition("/")[0].rpartition("/")[0]+"/edit_folder")
        self.quit()
        self.destroy()