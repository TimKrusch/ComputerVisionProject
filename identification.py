import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import os
import numpy as np
import imutils

anzahl_A_mark=0
anzahl_V_mark=0
anzahl_S_mark=0
anzahl_G_mark=0


def identify(imagelist, folder_path):
    global anzahl_A_mark
    global anzahl_V_mark
    global anzahl_S_mark
    global anzahl_G_mark

    result_global_A, result_global_V, anzahl_A, anzahl_V, anzahl_A_B, anzahl_V_B, anzahl_A_FP, anzahl_V_FP = 0,0,0,0,0,0,0,0
    result_global_S, result_global_G, anzahl_S, anzahl_G, anzahl_S_B, anzahl_G_B, anzahl_S_FP, anzahl_G_FP = 0,0,0,0,0,0,0,0
    
    file = open(imagelist[0].data["File Path"].rpartition("/")[0][:-3] + "result_data.txt","w").close()

    
    for image in imagelist:

        ##### Image einlesen #####
        img = cv2.imread(image.data["File Path"])
        image_true = img.copy()

        
        ##### Farbkanalsspreizung #####
        img_color_spread = img.copy()
        img_color_spread[:,:,0] = cv2.equalizeHist(img[:,:,0])
        img_color_spread[:,:,1] = cv2.equalizeHist(img[:,:,1]) 
        img_color_spread[:,:,2] = cv2.equalizeHist(img[:,:,2])
       
        
        img_cut=img_color_spread[25:750, 0:1360]


        image_color_spread_bilateral = cv2.bilateralFilter(img_cut,9,80,50)

        image_s_filtered_chanels = max_rgb_filter(image_color_spread_bilateral)
        image_s_filtered_chanels_R = image_s_filtered_chanels[:,:,2]
        image_s_filtered_chanels_R[image_s_filtered_chanels_R > 50] = 255
        image_s_filtered_chanels_R[image_s_filtered_chanels_R < 255] = 0


        image_s_filtered_chanels_B = image_s_filtered_chanels[:,:,0]
        image_s_filtered_chanels_B[image_s_filtered_chanels_B > 50] = 255
        image_s_filtered_chanels_B[image_s_filtered_chanels_B < 255] = 0

      
        
        
        image_r_thresh = cv2.adaptiveThreshold(image_s_filtered_chanels_R, 255 ,cv2. ADAPTIVE_THRESH_GAUSSIAN_C ,cv2.THRESH_BINARY , 11 , 2 )    
        image_b_thresh = cv2.adaptiveThreshold(image_s_filtered_chanels_B, 255 ,cv2. ADAPTIVE_THRESH_GAUSSIAN_C ,cv2.THRESH_BINARY , 11 , 2 )
        
        ##### Template Matching #####

        image_matched,result_data_A1 = temp_match('achtung.jpg',image_true,image_r_thresh,13000000,(255, 0, 255),image.data["Name"],"A1") #pink
        image_matched,result_data_A2 = temp_match('achtung_thin.jpg',image_matched,image_r_thresh,7500000,(0, 0, 255),image.data["Name"],"A2") #rot
        image_matched,result_data_V1 = temp_match('kreis.jpg',image_matched,image_r_thresh,10000000,(255, 255, 0),image.data["Name"],"V1") #türkis
        image_matched,result_data_V2 = temp_match('kreis25423463.jpg',image_matched,image_r_thresh,15000000,(0, 255, 0),image.data["Name"],"V2") #grün
        image_matched,result_data_V3 = temp_match('kreis_thin.jpg',image_matched,image_r_thresh,7000000,(255, 0, 0),image.data["Name"],"V3") #blau 6,7
        image_matched,result_data_S = temp_match('stop.jpg',image_matched,image_r_thresh,12000000,(0, 255, 255),image.data["Name"],"S") #gelb
        image_matched,result_data_G = temp_match('vorfgew.jpg',image_matched,image_r_thresh,11500000,(0, 120, 200),image.data["Name"],"G") #orange

        
        print(image.data["Name"])
        
        ##### Write Result Data to File #####

        file = open(image.data["File Path"].rpartition("/")[0][:-3] + "result_data.txt","a+") 
        if result_data_A1 is not None: 
            file.write(result_data_A1)
            file.write("\n")
        if result_data_A2 is not None: 
            file.write(result_data_A2)
            file.write("\n")
        if result_data_V1 is not None: 
            file.write(result_data_V1)
            file.write("\n")
        if result_data_V2 is not None: 
            file.write(result_data_V2)
            file.write("\n")
        if result_data_V3 is not None: 
            file.write(result_data_V3)
            file.write("\n")
        if result_data_S is not None: 
            file.write(result_data_S)
            file.write("\n")
        if result_data_G is not None: 
            file.write(result_data_G)
            file.write("\n")
        file.close()

        ##### Evaluate Results #####

        achtung_numbers = ["11","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
        verbot_numbers = ["0","1","2","3","4","5","7","8","9","10","15","16"]
        stop_number = ["14"]
        vorfahrtgew_number = ["13"]

       
        gt_data = image.data["GT Data"]
        isA = False
        isV = False
        isS = False
        isG = False

        anzahl_A_correct_tracked, anzahl_V_correct_tracked, anzahl_S_correct_tracked,anzahl_G_correct_tracked = 0,0,0,0



        for line in gt_data.split('\n'):
            

            if line.split(";")[0] == image.data["Name"]:


                if line.split(";")[5] in achtung_numbers:
                    anzahl_A += 1
                    percentage_A1,percentage_A2 = 0,0

                    if isA is False:
                        anzahl_A_B += 1
                        isA = True

                    if result_data_A1 is not None: percentage_A1 = boundingboxes_overlap_percentage(line.split(";"),result_data_A1.split(";"))
                    #print("A1 P : " + str(percentage_A1))
                    if result_data_A2 is not None: percentage_A2 = boundingboxes_overlap_percentage(line.split(";"),result_data_A2.split(";"))
                    #print("A2 P : " + str(percentage_A2))

                    image.data["Result Data"] += str(percentage_A1) + "/n" + str(percentage_A2) + "/n"

                    if (percentage_A1>0.5) | (percentage_A2>0.5):
                        result_global_A += 1
                        if (percentage_A1>0.5): anzahl_A_correct_tracked += 1
                        if (percentage_A2>0.5): anzahl_A_correct_tracked += 1
                        

                    


                if line.split(";")[5] in verbot_numbers:
                    anzahl_V += 1
                    percentage_V1,percentage_V2,percentage_V3 = 0,0,0

                    if isV is False:
                        anzahl_V_B += 1
                        isV = True

                    if result_data_V1 is not None: percentage_V1 = boundingboxes_overlap_percentage(line.split(";"),result_data_V1.split(";"))
                    #print("V1 P : " + str(percentage_V1))
                    if result_data_V2 is not None: percentage_V2 = boundingboxes_overlap_percentage(line.split(";"),result_data_V2.split(";"))
                    #print("V2 P : " + str(percentage_V2))
                    if result_data_V3 is not None: percentage_V3 = boundingboxes_overlap_percentage(line.split(";"),result_data_V3.split(";"))
                    #print("V3 P : " + str(percentage_V3))

                    image.data["Result Data"] += str(percentage_V1) + "/n" + str(percentage_V2) + "/n"  + str(percentage_V3) + "/n"

                    if (percentage_V1>0.5) | (percentage_V2>0.5)| (percentage_V3>0.5):
                        result_global_V += 1
                        if (percentage_V1>0.5): anzahl_V_correct_tracked += 1
                        if (percentage_V2>0.5): anzahl_V_correct_tracked += 1
                        if (percentage_V3>0.5): anzahl_V_correct_tracked += 1
                    


                if line.split(";")[5] in stop_number:
                    anzahl_S += 1
                    percentage_S = 0

                    if isS is False:
                        anzahl_S_B += 1
                        isS = True

                    if result_data_S is not None: percentage_S = boundingboxes_overlap_percentage(line.split(";"),result_data_S.split(";"))
                    
                    image.data["Result Data"] += str(percentage_S) + "\n"

                    if (percentage_S>0.5):
                        result_global_S += 1
                        anzahl_S_correct_tracked += 1
                
                if line.split(";")[5] in vorfahrtgew_number:
                    anzahl_G += 1
                    percentage_G = 0

                    if isG is False:
                        anzahl_G_B += 1
                        isG = True

                    if result_data_G is not None: percentage_G = boundingboxes_overlap_percentage(line.split(";"),result_data_G.split(";"))
                    
                    image.data["Result Data"] += str(percentage_G) + "\n"

                    if (percentage_G>0.5):
                        result_global_G += 1
                        anzahl_G_correct_tracked += 1

        
        anzahl_A_FP += anzahl_A_mark - anzahl_A_correct_tracked
        anzahl_V_FP += anzahl_V_mark - anzahl_V_correct_tracked
        anzahl_S_FP += anzahl_S_mark - anzahl_S_correct_tracked
        anzahl_G_FP += anzahl_G_mark - anzahl_G_correct_tracked

        anzahl_A_mark = 0
        anzahl_V_mark = 0
        anzahl_S_mark = 0
        anzahl_G_mark = 0

        ##### Save edited Pics #####

        cv2.imwrite(
            folder_path + "/" + image.data["Name"][:-4] + "-edit.png", image_matched
        )
        image.data["Edit Img"] = folder_path + "/" + \
            image.data["Name"][:-4] + "-edit.png"
        
           

    return imagelist, result_global_A, result_global_V, anzahl_A, anzahl_V, anzahl_A_B, anzahl_V_B, anzahl_A_FP, anzahl_V_FP, result_global_S, result_global_G, anzahl_S, anzahl_G, anzahl_S_B, anzahl_G_B, anzahl_S_FP, anzahl_G_FP






##### MAX RGB Filter nach: #####
##### https://www.pyimagesearch.com/2015/09/28/implementing-the-max-rgb-filter-in-opencv/ #####


def max_rgb_filter(image):
    # split the image into its BGR components
    (B,G,R) = cv2.split(image)

   

    # find the maximum pixel intensity values for each
	# (x, y)-coordinate,, then set all pixel values less
	# than M to zero
    M = np.maximum(np.maximum(R,G),B)

    R[R==0] = 1
    G[G==0] = 1
    B[B==0] = 1

    RdG = np.divide(R,G)
    RdB = np.divide(R,B)

    GdR = np.divide(G,R)
    GdB = np.divide(G,B)

    BdR = np.divide(B,R)
    BdG = np.divide(B,G)

    
    R[R<M]=0
    R[RdG<1.3]=0
    R[RdB<1.3]=0

    G[G<M]=0
    G[GdR<1.3]=0
    G[GdB<1.3]=0

    B[B<M]=0
    B[BdR<1.3]=0
    B[BdG<1.1]=0


    # merge the channels back together and return the image
    return cv2.merge([B,G,R])


def temp_match(schild,img,img_filtered,thresh,farbe,name,id):
    global anzahl_A_mark
    global anzahl_V_mark
    global anzahl_S_mark
    global anzahl_G_mark

    found = None 
    template = cv2.imread(schild)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    (tH, tW) = template.shape[:2]

    ##### Mulitscale Template Matching #####
    #https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/

    for scale in np.linspace(0.2,1.0,5)[::1]:
        
        resized = imutils.resize(img_filtered, width = int(img_filtered.shape[1] * scale))
        r = img_filtered.shape[1] / float(resized.shape[1])
        
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        template_matched = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF)
            
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(template_matched)
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r)+25)
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r)+25)

    #print(maxVal)
   
    if maxVal > thresh :
        cv2.rectangle(img, (startX, startY), (endX, endY), farbe, 2)
        if id in ["A1","A2"]:
            anzahl_A_mark += 1
        if id in ["V1","V2","V3"]:
            anzahl_V_mark += 1
        if id in ["S"]:
            anzahl_S_mark += 1
        if id in ["G"]:
            anzahl_G_mark += 1
        
        result_data = name + ";" + str(startX) + ";" + str(startY) + ";" + str(endX) + ";" + str(endY) + ";" + id
        
        return img,result_data

    return img,None


def boundingboxes_overlap_percentage(GT_line,R_line):
    percentage = 0.0

    GT_sx,R_sx = int(GT_line[1]),int(R_line[1])
    GT_sy,R_sy = int(GT_line[2]),int(R_line[2])
    GT_ex,R_ex = int(GT_line[3]),int(R_line[3])
    GT_ey,R_ey = int(GT_line[4]),int(R_line[4])

    B_sx = max(GT_sx,R_sx)
    B_sy = max(GT_sy,R_sy)
    B_ex = min(GT_ex,R_ex)
    B_ey = min(GT_ey,R_ey)

    if (B_sx >= B_ex) | (B_sy >= B_ey):
        return 0.0

    B_area = float((B_ex - B_sx) * (B_ey - B_sy))
    GT_area = float((GT_ex - GT_sx) * (GT_ey - GT_sy))

    percentage = B_area / GT_area

    return percentage 