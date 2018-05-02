from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk



class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Picture_Data:

    def __init__(self):
        self.data = {"File Path": "", "GT File Path": "" , "GT Data": ""}


class myUI(Frame, metaclass=Singleton):

    def __init__(self):
        Frame.__init__(self)
        
        #variables
        self.gt_text_label = StringVar()
        self.folder_picture_data = []

        

        ###### define Window properties ######
        self.master.title("Projekt-Verkehrsschildererkennung")
        self.master.minsize(width=1000, height = 765)
        self.master.configure(background ="white")
        self.grid_rowconfigure(0, minsize=20)
        self.grid_rowconfigure(2, minsize=20)
        self.grid_rowconfigure(4, minsize=20)
        self.grid_rowconfigure(6, minsize=20)
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
        self.FileMenu.add_command(label = "Open File", command=self.openFile)
        self.FileMenu.add_command(label = "Open Folder")

        self.EditMenu = Menu(self.top_menu)
        self.top_menu.add_cascade(label = "Edit", menu=self.EditMenu)
        self.EditMenu.add_command(label = "Find Signs")



       
        
        #Labels
        self.original_picture_Label = Label(self.master, image = PhotoImage(file="gray.png"))
        self.original_picture_Label.grid(row=1,column=1,sticky=W)

        self.edited_picture_Label = Label(self.master, image = PhotoImage(file="gray.png"))
        self.edited_picture_Label.grid(row=1,column=3)

        self.gt_picture_Label = Label(self.master, image = PhotoImage(file="gray.png"))
        self.gt_picture_Label.grid(row=1,column=5,sticky=E)

        self.row0_label = Label(self.master, background="white")
        self.row0_label.grid(row=0,column=0)
        self.row2_label = Label(self.master, background="white")
        self.row2_label.grid(row=2,column=0)
        self.column0_label = Label(self.master, background="white")
        self.column0_label.grid(row=1,column=0)
        self.column2_label = Label(self.master, background="white")
        self.column2_label.grid(row=1,column=2)
        self.column4_label = Label(self.master, background="white")
        self.column4_label.grid(row=1,column=4)
        self.column6_label = Label(self.master, background="white")
        self.column6_label.grid(row=1,column=6)


        self.gt_text_label = Label(self.master, text="",background = "white")
        self.gt_text_label.grid(row = 3, column=5)

        

    def openFile(self):
        self.fileName = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
        path = self.fileName


        if self.fileName.endswith("_gt.png"):
            image_gt = Image.open(self.fileName)
            image_gt.thumbnail((400,301), Image.ANTIALIAS)
            image_gt = ImageTk.PhotoImage(image_gt)

            path = path.rpartition("/")[0].rpartition("/")[0]+"/png/"+path.rpartition("/")[2][:5]+".png"
            image = Image.open(path)
            image.thumbnail((400,301), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
        else:
            
            image = Image.open(self.fileName)
            image.thumbnail((400,301), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)

            #get filename of the Ground Truth Image
            path = path.rpartition("/")
            folder_path_gt = path[0] + "_gt/"
            path_gt = path[2].rpartition(".")
            file_path_gt= folder_path_gt + path_gt[0] + "_gt.png"
            image_gt = Image.open(file_path_gt)
            image_gt.thumbnail((400,301), Image.ANTIALIAS)
            image_gt = ImageTk.PhotoImage(image_gt)
       
        self.original_picture2 = Canvas(self.master, width=400,height=301)
        self.original_picture2.create_image(0, 0, anchor=NW, image=image)
        self.original_picture2.image = image
        self.original_picture2.grid(row=1,column=1,sticky=W)

        #draw Ground Truth Image
        self.gt_picture2 = Canvas(self.master, width=400,height=301)
        self.gt_picture2.create_image(0, 0, anchor=NW, image=image_gt)
        self.gt_picture2.image = image_gt
        self.gt_picture2.grid(row=1,column=5,sticky=W)

        #get the Ground Truth Data of the Image
        gt_data = ""
        fobj = open(path.rpartition("/")[0].rpartition("/")[0]+"/gt_train.txt")
        for line in fobj:
            if line.startswith(path.rpartition("/")[2][:9]):
                gt_data = gt_data + "Bounding Box: " + line[10:].rpartition(";")[0] + "\n Klasse: " + line[10:].rpartition(";")[2] + "\n"     
        fobj.close()

        #draw label that shows the ground truth data
        
        self.gt_text_label.configure(text="Ground Truth Data :\n"+gt_data)
    
    