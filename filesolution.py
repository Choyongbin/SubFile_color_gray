# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:55:02 2021

2021-08-25

version 1.1

@author: 82102
"""
import cv2
import os
import shutil
import natsort
from tkinter import filedialog
import tkinter.messagebox
import tkinter as tk
import tkinter.font

import numpy as np
import xdwlib as xd
import hashlib
import sqlite3
import time
from xdwlib import xdwopen

class MainFrame():
    
    def __init__(self):
        self.root = tk.Tk()
        self.font=tk.font.Font(family="맑은 고딕", weight="bold")
        
        w = 650 #Width of Frame
        h = 300 #Height of Frame

        hs = self.root.winfo_screenheight() #Height of the screen
        
        x = 0
        y = hs - (h + 70)
        
        #main
        self.root.title("File Solution v1.1")
        self.root.geometry("%dx%d+%d+%d" % (w,h,x,y))
        self.root.resizable(False,False)

        self.frame_bottom = tk.Frame(self.root,
                                     relief="solid",
                                     bd=1)
        self.frame_bottom.pack(side="bottom", fill="both", padx=5, expand=False)
        self.ttt1label = tk.Label(self.frame_bottom,
                                  font=self.font,
                                  text="blue",
                                  )
        self.ttt1 = tk.Entry(self.frame_bottom,
                             # bg="firebrick1",
                             width=64,
                             bg="gray12",
                             font=self.font,
                             fg="white",
                             )
        self.ttt2label = tk.Label(self.frame_bottom,
                                  font=self.font,
                                  text="red",
                                  )
        self.ttt2 = tk.Entry(self.frame_bottom,
                             # bg="yellow2",
                             width=64,
                             bg="gray12",
                             font=self.font,
                             fg="white",
                             )
        self.ttt3label = tk.Label(self.frame_bottom,
                                  font=self.font,
                                  text="yellow",
                                  )
        self.ttt3 = tk.Entry(self.frame_bottom,
                             # bg="lawn green",
                             width=64,
                             bg="gray12",
                             font=self.font,
                             fg="white",
                             )
        self.ttt4label = tk.Label(self.frame_bottom,
                                  font=self.font,
                                  text="green",
                                  )
        self.ttt4 = tk.Entry(self.frame_bottom,
                             # bg="royal blue",
                             width=64,
                             bg="gray12",
                             font=self.font,
                             #text="123",
                             fg="white",
                             )
        self.ttt = tk.Label(self.frame_bottom,
                            text="무단 복제 금지",
                            width=64,
                            bg="red",
                            font=self.font,
                            fg="white"
                            )
        self.ttt1label.grid(row=0, column=0)
        self.ttt1.grid(row=0, column=1, sticky="w")
        self.ttt2label.grid(row=1, column=0)
        self.ttt2.grid(row=1, column=1, sticky="w")
        self.ttt3label.grid(row=2, column=0)
        self.ttt3.grid(row=2, column=1, sticky="w")
        self.ttt4label.grid(row=3, column=0)
        self.ttt4.grid(row=3, column=1, sticky="w")
        self.ttt.grid(row=4, column=0, sticky="w", columnspan=2)

        # self.ttt4.pack(side="bottom", fill="x", expand=False)
        # self.ttt3.pack(side="bottom", fill="x", expand=False)
        # self.ttt2.pack(side="bottom", fill="x", expand=False)
        # self.ttt1.pack(side="bottom", fill="x", expand=False)

        #converter frame
        self.frame_left = tk.LabelFrame(self.root, 
                                        text="Converter",
                                        relief="solid", 
                                        bd=1)
        
        self.frame_left.pack(side="left", fill="both",padx=5, expand=False)
        self.button1 = tk.Button(self.frame_left,
                                 width=10,
                                 bg="white",
                                 font=self.font,
                                 text="파일 선택",
                                 command=self.openFile
                                 )

        self.button2 = tk.Button(self.frame_left,
                                 bg="red",
                                 fg="white",
                                 font=self.font,
                                 width=10,
                                 text = "실행",
                                 command=self.readLabelText
                                 #command=self.thread_start
                                 )
        self.button1.grid(row = 0,column =0,padx=3,sticky="W")
        self.button2.grid(row = 0,column =1,padx=3,sticky="E")  
        
        self.RadioVariety = tk.IntVar() 
        self.r1 = tk.Radiobutton(self.frame_left,
                                 text = "단면",
                                 variable=self.RadioVariety,value=1)
        self.r2 = tk.Radiobutton(self.frame_left,
                                 text = "양면",
                                 variable=self.RadioVariety,value=2)
        self.r1.grid(row = 1,column =0,pady=1,sticky="e")
        self.r2.grid(row = 1,column =1,pady=1,sticky="w")
        
        self.rv3 = tk.BooleanVar()
        self.rv3.set(True)
        self.r3 = tk.Checkbutton(self.frame_left,
                                 text = "컬러흑백 분류",
                                 variable=self.rv3,
                                 command=self.checkbtn4
                                 )
        self.r3.grid(row = 2,column =0,sticky="e")
        
        self.rv4 = tk.BooleanVar()
        self.rv4.set(True)
        self.r4 = tk.Checkbutton(self.frame_left,
                                 text = "간지 삭제",
                                 variable=self.rv4,
                                 command=self.checkbtn4
                                 )
        self.r4.grid(row = 2,column =1,sticky="w")
        
        self.rv5 = tk.BooleanVar()
        self.rv5.set(False)
        self.r5 = tk.Checkbutton(self.frame_left,
                                 text = "컬러 페이지",
                                 variable=self.rv5,
                                 command=self.checkbtn3
                                 )
        self.r5.grid(row = 3,column =0,sticky="we")
        
        self.doc = ""
        self.filenames = [] #선택한 파일 이름
        self.filepaths = [] #선택한 파일 경로
        self.filename = ""  #선택한 파일 temp
        self.color_list=[]
        self.gray_list=[]
        self.list_yellow = []
        self.list_blue = []
        self.list_red = []
        self.list_green = []
        self.list_colorPage = []
        
        #파랑
        self.lower_scale_blue = (100,80,80)
        self.upper_scale_blue = (140,255,255)
        #노랑
        self.lower_scale_yellow = (20,140,140)
        self.upper_scale_yellow = (70,255,255)
        #빨강
        self.lower_scale_red = (-10,100,100)
        self.upper_scale_red = (10,255,255)
        #초록
        self.lower_scale_green = (50,100,100)
        self.upper_scale_green = (70,255,255)
        
        self.ext = []
        self.dirname = ""
        self.newdir= ""
        self.pages = 0
        
     
        self.txt1 = tk.Label(self.frame_left, 
                             text=" "
                             ,wraplength = 230)
        self.txt1.grid(row = 4,column =0,columnspan = 2,sticky="nwes")
        
        #directory frame
        self.frame_right = tk.LabelFrame(self.root,
                                         text ="Directory solution",
                                         relief="solid",
                                         bd=1)
        
        #self.frame_right.grid(row = 0,column =1,sticky="nwes")
        self.frame_right.pack(side="right",fill="both",padx=5,expand=False)
        self.button3 = tk.Button(self.frame_right,
                                 width=15,
                                 font=self.font,
                                 bg="white",
                                 text="폴더 선택",
                                 command=self.opendirectory
                                 )
        
        self.button4 = tk.Button(self.frame_right,
                                 bg="red",
                                 fg="white",
                                 font=self.font,
                                 width=10,
                                 text = "실행",
                                 command=self.makeup2
                                 )
        
        self.button3.grid(row = 0,column =0,sticky="w",padx=3,pady=3)
        self.button4.grid(row = 0,column =1,sticky="e",padx=3,pady=3)
        
        self.checkframe = tk.Frame(self.frame_right,
                                   relief="solid",
                                   bd=1)
        self.checkframe.grid(row=1,column=0,columnspan=2,padx=3)
        self.txt5 = tk.Label(self.checkframe,
                             text = "  하위폴더 갯수")
        self.txt5.grid(row=1,column=0,columnspan=3,sticky="w")
        self.spinbox1 = tk.Spinbox(self.checkframe,
                                 from_=0,
                                 to=9,
                                 width=2,
                                 validate='all',
                                 )
        self.spinbox1.grid(row = 1,column =2,sticky="w")
        
        self.checkv2 = tk.BooleanVar()
        self.checkv2.set(True)
        self.c2 = tk.Checkbutton(self.checkframe,
                                 text = "*.*",
                                 variable=self.checkv2,
                                 command=self.checkbtn1
                                 )
        self.c2.grid(row = 0,column =0)
        
        self.checkv3 = tk.BooleanVar()
        self.checkv3.set(True)
        self.c3 = tk.Checkbutton(self.checkframe,
                                 text = "*.pdf",
                                 variable=self.checkv3,
                                 command=self.checkbtn2)
        self.c3.grid(row = 0,column =1)
        
        self.checkv4 = tk.BooleanVar()
        self.checkv4.set(True)
        self.c4 = tk.Checkbutton(self.checkframe,
                                 text = "*.hwp",
                                 variable=self.checkv4,
                                 command=self.checkbtn2)
        self.c4.grid(row = 0,column =2)

        self.checkv8 = tk.BooleanVar()
        self.checkv8.set(True)
        self.c8 = tk.Checkbutton(self.checkframe,
                                 text="*.hwpx",
                                 variable=self.checkv8,
                                 command=self.checkbtn2)
        self.c8.grid(row=0, column=3)
        
        self.checkv5 = tk.BooleanVar()
        self.checkv5.set(True)
        self.c5 = tk.Checkbutton(self.checkframe,
                                 text = "*.doc",
                                 variable=self.checkv5, 
                                 command=self.checkbtn2)
        self.c5.grid(row = 0,column =4)
        
        self.checkv6 = tk.BooleanVar()
        self.checkv6.set(True)
        self.c6 = tk.Checkbutton(self.checkframe,
                                 text = "*.ppt",
                                 variable=self.checkv6,
                                 command=self.checkbtn2)
        self.c6.grid(row = 0,column =5)
        
        self.checkv7 = tk.BooleanVar()
        self.checkv7.set(True)
        self.c7 = tk.Checkbutton(self.checkframe,
                                 text = "*.xls",
                                 variable=self.checkv7,
                                 command=self.checkbtn2)
        self.c7.grid(row = 0,column =6)
        
       
        self.txt2 = tk.Label(self.frame_right, text = "",wraplength = 300) 
        self.txt2.grid(row = 2,column =0,columnspan = 2,sticky="nwes")
        
        self.dir_list =[]
        self.fil_list =[]
        self.numberinglist = []
        
        self.spinint = 0
        
        self.root.mainloop()
  
    
    def checkbtn1(self):
        if self.checkv2.get():
            self.c3.select()
            self.c4.select()
            self.c5.select()
            self.c6.select()
            self.c7.select()
            self.c8.select()
        else:
            self.c3.deselect()
            self.c4.deselect()
            self.c5.deselect()
            self.c6.deselect()
            self.c7.deselect()
            self.c8.deselect()
            
    def checkbtn2(self):
        if self.checkv2.get():
            self.c2.deselect()
            
    def checkbtn3(self):
        if self.rv5.get():
            self.r3.deselect()
            self.r4.deselect()
        else:
            self.r3.select()
            self.r4.select()
        
    def checkbtn4(self):
        if self.rv3.get() or self.rv4.get():
            self.r5.deselect()
            
    #pdf 열기
    def openFile(self):  
        
        self.filepaths.clear()
        self.filenames.clear()
        
        self.root.file = filedialog.askopenfilenames(
            initialdir='dir',
            title='select file',
            filetypes=(('xdw files', '*.xdw'),
                       ('all files','*.*')))
        
        self.filename = ""
        
        for i, v in enumerate(self.root.file):
            self.filename += v + "\n"
            self.filenames.append(self.getFileName(v))
            self.filepaths.append(v)
        self.txt1.configure(text=self.filename)
        
    def readLabelText(self):
        if not self.filenames:
            tk.messagebox.showinfo("Error","파일 확인")
        else:
            for i, filename in enumerate(self.filenames):
                temp = os.path.splitext(filename)
            
                if temp[-1] ==".xdw":
                    temppath = os.path.dirname(self.filepaths[i])
                    if self.rv3.get() == True: #컬러 흑백 분류
                        if self.RadioVariety.get() == 1 or self.RadioVariety.get() == 2:   
                            self.classify_xdw(temppath,filename,temp[0])
                        else:
                            tk.messagebox.showinfo("Error","단면 or 양면 선택")
                            break
                    if self.rv4.get() == True: #간지 삭제
                        if self.RadioVariety.get() == 1 or self.RadioVariety.get() == 2:
                            self.list_blue.clear()
                            self.list_red.clear()
                            self.list_yellow.clear()
                            self.list_green.clear()
                            time.sleep(0.5)
                            self.deleteNextGanzi(temppath, temp[0])
                            self.printColor()
                        else:
                            tk.messagebox.showinfo("Error","단면 or 양면 선택")
                            break
                    if self.rv5.get() == True: #컬러 번호 따오기
                        if self.RadioVariety.get() == 1 or self.RadioVariety.get() == 2:
                            self.list_colorPage.clear()
                            self.list_blue.clear()
                            self.list_red.clear()
                            self.list_yellow.clear()
                            self.list_green.clear()
                            time.sleep(0.5)
                            self.classify_xdw_printColorNum(temppath, filename, temp[0])
                            self.print_annotations(temppath, temp[0])
                            self.printColor()
                        else:
                            tk.messagebox.showinfo("Error", "단면 or 양면 선택")
                            break
                    if i == len(self.filenames) -1:
                        tk.messagebox.showinfo("Complete","분류 완료")
                else :
                    tk.messagebox.showinfo("Error","파일 확인")
                    
    def getFileName(self, path):
        str = path.split('/')
        return str[len(str)-1]
    
    def printColorNum(self):
        templist = []
        ta = 0
        tb = 0
        
        for i, v in enumerate(self.list_colorPage):
            if ta == 0 and tb == 0:
                ta = v
                tb = v
                
            elif i == len(self.list_colorPage) - 1:
                if ta == tb:
                    if tb + 1 == v:
                        templist.append(str(ta) + "-" + str(v))
                    else:    
                        templist.append(str(ta))
                        templist.append(str(v))
                        
                else:
                    if tb + 1 == v:
                        templist.append(str(ta) + "-" + str(v))
                    else:    
                        templist.append(str(ta) + "-" + str(tb))
                        templist.append(str(v))
                        
            else:
                if tb + 1 == v:
                    tb = v
                else:
                    if ta == tb:
                        templist.append(str(ta))
                        ta = v
                        tb = v
                    else:
                        templist.append(str(ta) + "-" + str(tb))
                        ta = v
                        tb = v
        print(','.join([str(_) for _ in templist]))
            
                
            
    
    def classify_xdw_printColorNum(self, imgpath1,file_name,file_name2):
        try:
            self.doc = xdwopen(imgpath1+"\\"+file_name)
            self.doc.show_annotations = False
            colorpage = xd.PageCollection()
            greypage = xd.PageCollection()
            whitepath = xd.create()
            self.docwhite = xdwopen(whitepath)
            whitepage = self.docwhite.page(0)
            if self.RadioVariety.get() == 1: #단면
                for j in range(self.doc.pages):
                    if self.doc.page(j).is_color and self.doc.page(j).annotations == 0:
                        colorpage += self.doc.page(j)
                        greypage += whitepage
                        self.list_colorPage.append(j+1)
                    else:
                        greypage += self.doc.page(j)
                        
            elif self.RadioVariety.get() == 2: #양면
                for j in range(0,self.doc.pages,2):
                    if j == self.doc.pages -1:
                        if self.doc.page(j).is_color and self.doc.page(j).annotations == 0:
                            colorpage += self.doc.page(j)
                            greypage += whitepage
                            self.list_colorPage.append(j+1)
                        else :
                            greypage += self.doc.page(j)
                    elif (self.doc.page(j).is_color or self.doc.page(j+1).is_color) and self.doc.page(j).annotations == 0 and self.doc.page(j+1).annotations == 0:
                        colorpage += self.doc.page(j)
                        colorpage += self.doc.page(j+1)
                        greypage += whitepage
                        greypage += whitepage
                        self.list_colorPage.append(j+1)
                        self.list_colorPage.append(j+2)
                    else :
                        greypage += self.doc.page(j)
                        greypage += self.doc.page(j+1)
            self.printColorNum()
            if os.path.isfile(str(imgpath1 +"\\"+file_name2+"_grey.xdw")):
                os.remove(str(imgpath1 +"\\"+file_name2+"_grey.xdw"))
                os.remove(str(imgpath1 +"\\"+file_name2+"_color.xdw"))
            outputpath = imgpath1 +"\\"+file_name2+"_color.xdw"
            outputpath2 = imgpath1 +"\\"+file_name2+"_grey.xdw"
            colorpage.export(str(outputpath),True)
            greypage.export(str(outputpath2), True)
            self.doc.close()
            self.docwhite.close()
            os.remove(whitepath)
        except :
            self.doc.close()
            self.docwhite.close()
            os.remove(whitepath)

    def classify_xdw(self, imgpath1, file_name, file_name2):
        try:
            self.doc = xdwopen(imgpath1+"\\"+file_name)
            self.doc.show_annotations = False
            colorpage = xd.PageCollection()
            greypage = xd.PageCollection()
            if self.RadioVariety.get() == 1: #단면
                for j in range(self.doc.pages):
                    if self.doc.page(j).is_color and self.doc.page(j).annotations == 0:
                        self.doc.export_image(j, dpi = 15)
                        img = cv2.imread(imgpath1+"\\"+file_name2+"_P"+str(j+1)+".xdw.bmp")
                        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                        s = img_hsv[:, :, 1]                    # 채도 추출
                        if np.all(( s == 0 ) | (s == 1)):       # 채도가 0 또는 1이면 greypage <- 이거 범위로 바꾸면 됨
                            greypage += self.doc.page(j)
                        else:
                            colorpage += self.doc.page(j)
                        os.remove(imgpath1+"\\"+file_name2+"_P"+str(j+1)+".xdw.bmp")
                    else:
                        greypage += self.doc.page(j)
                        
            elif self.RadioVariety.get() == 2: #양면
                for j in range(0,self.doc.pages,2):
                    if j == self.doc.pages -1:
                        if self.doc.page(j).is_color and self.doc.page(j).annotations == 0:
                            colorpage += self.doc.page(j)
                        else :
                            greypage += self.doc.page(j)
                    elif (self.doc.page(j).is_color or self.doc.page(j+1).is_color) and self.doc.page(j).annotations == 0 and self.doc.page(j+1).annotations == 0:
                        colorpage += self.doc.page(j)
                        colorpage += self.doc.page(j+1)
                    else :
                        greypage += self.doc.page(j)
                        greypage += self.doc.page(j+1)
            if os.path.isfile(str(imgpath1 +"\\"+file_name2+"_grey.xdw")):
                os.remove(str(imgpath1 +"\\"+file_name2+"_grey.xdw"))
                os.remove(str(imgpath1 +"\\"+file_name2+"_color.xdw"))
            outputpath = imgpath1 +"\\"+file_name2+"_color.xdw"
            outputpath2 = imgpath1 +"\\"+file_name2+"_grey.xdw"
            colorpage.export(str(outputpath),True)
            greypage.export(str(outputpath2), True)
            self.doc.close()
        except :
            self.doc.close()
            
    def print_annotations(self, imgpath1, file_name):
        try:
            self.doc = xdwopen(imgpath1+"\\"+file_name+"_grey.xdw")
            self.doc.show_annotations = True
            self.doc.editable = True
            templist = []
            
            for i in range(self.doc.pages):
                if not self.doc[i].annotations == 0:
                    templist.append(i)
            
            for j in templist:
                self.doc.export_image(j,dpi = 15)
                self.isgray(imgpath1+"\\"+file_name+"_grey_P"+str(j+1)+".xdw.bmp",j+1)
                os.remove(imgpath1+"\\"+file_name+"_grey_P"+str(j+1)+".xdw.bmp")
            self.doc.close()
        except:
            self.doc.close()
            
    def deleteNextGanzi(self, imgpath1, file_name):

        try:
            if self.rv3.get() == True: #컬러 흑백 분류 후 간지 삭제
                self.doc = xdwopen(imgpath1+"\\"+file_name+"_grey.xdw")
            else:                      #간지만 삭제
                self.doc = xdwopen(imgpath1+"\\"+file_name+".xdw")
                
            self.doc.show_annotations = True
            self.doc.editable = True
            templist = []
            for i in range(self.doc.pages):
                if not self.doc[i].annotations == 0:
                    templist.append(i)
            if self.RadioVariety.get() == 1:  #단면 간지 삭제
                for j in templist:
                    self.doc.export_image(j,dpi = 15)
                    if self.rv3.get() == True:
                        #self.isgray2(imgpath1+"\\"+file_name+"_grey_P"+str(j+1)+".xdw.JPEG",j+1)
                        self.isgray(imgpath1+"\\"+file_name+"_grey_P"+str(j+1)+".xdw.bmp",j+1)
                        os.remove(imgpath1+"\\"+file_name+"_grey_P"+str(j+1)+".xdw.bmp")
                    else:
                        #self.isgray2(imgpath1+"\\"+file_name+"_P"+str(j+1)+".xdw.JPEG",j+1)
                        self.isgray(imgpath1+"\\"+file_name+"_P"+str(j+1)+".xdw.bmp",j+1)
                        os.remove(imgpath1+"\\"+file_name+"_P"+str(j+1)+".xdw.bmp")
                        
            elif self.RadioVariety.get() == 2: #양면 간지 삭제
                temp = 0
                if templist[-1] == self.doc.pages-1:
                    print("마지막장 간지 삭제 불가")
                else:
                    for k in templist:
                        self.doc.delete(k+1-temp)
                        templist[temp] = templist[temp] - temp
                        temp += 1
                    for j in templist:
                        self.doc.export_image(j,dpi = 15)
                        if self.rv3.get() == True:
                            self.isgray(imgpath1+"\\"+file_name+"_grey_P"+str(j+1)+".xdw.bmp",j+1)
                            os.remove(imgpath1+"\\"+file_name+"_grey_P"+str(j+1)+".xdw.bmp")
                        else:
                            self.isgray(imgpath1+"\\"+file_name+"_P"+str(j+1)+".xdw.bmp",j+1)
                            os.remove(imgpath1+"\\"+file_name+"_P"+str(j+1)+".xdw.bmp")
            self.doc.save()
            self.doc.close()
        except:
            self.doc.close()
            
            
            
    def printColor(self):
        print("\n")
        if self.list_blue:
            print(" ")
            print("Blue")
            print(','.join([str(_) for _ in self.list_blue]))
            #entry_text_blue.set('blue,'.join([str(_) for _ in self.list_blue]))
            #self.ttt1.insert(0, 'blue,'.join([str(_) for _ in self.list_blue]))

            self.ttt1.config(state="normal")
            self.ttt1.delete(0, 'end')
            self.ttt1.insert(0, ','.join([str(_) for _ in self.list_blue]))
            self.ttt1.config(state="readonly",
                             readonlybackground="black")
        if self.list_red:
            print(" ")
            print("Red")
            print(','.join([str(_) for _ in self.list_red]))
            #entry_text_red.set('red,'.join([str(_) for _ in self.list_red]))
            #self.ttt2.insert(0, 'red,'.join([str(_) for _ in self.list_red]))
            self.ttt2.config(state="normal")
            self.ttt2.delete(0, 'end')
            self.ttt2.insert(0, ','.join([str(_) for _ in self.list_red]))
            self.ttt2.config(state="readonly",
                             readonlybackground="black")
        if self.list_yellow:
            print(" ")
            print("Yellow")
            print(','.join([str(_) for _ in self.list_yellow]))
            #entry_text_yellow.set('yellow,'.join([str(_) for _ in self.list_yellow]))
            #self.ttt3.insert(0, 'yellow,'.join([str(_) for _ in self.list_yellow]))
            self.ttt3.config(state="normal")
            self.ttt3.delete(0, 'end')
            self.ttt3.insert(0, ','.join([str(_) for _ in self.list_yellow]))
            self.ttt3.config(state="readonly",
                             readonlybackground="black")
        if self.list_green:
            print(" ")
            print("Green")
            print(','.join([str(_) for _ in self.list_green]))
            #entry_text_green.set('green,'.join([str(_) for _ in self.list_green]))
            #self.ttt4.insert(0, 'green,'.join([str(_) for _ in self.list_green]))
            self.ttt4.config(state="normal")
            self.ttt4.delete(0, 'end')
            self.ttt4.insert(0, ','.join([str(_) for _ in self.list_green]))
            self.ttt4.config(state="readonly",
                             readonlybackground="black")
        
        
            
    def isgray(self,imgpath, number):
        img = cv2.imread(imgpath)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img.resize(50,50)
        if cv2.inRange(img_hsv, self.lower_scale_blue,self.upper_scale_blue).any():
            self.list_blue.append(number)
        elif cv2.inRange(img_hsv,self.lower_scale_yellow, self.upper_scale_yellow).any():
            self.list_yellow.append(number)
        elif cv2.inRange(img_hsv,self.lower_scale_red, self.upper_scale_red).any():
            self.list_red.append(number)
        elif cv2.inRange(img_hsv,self.lower_scale_green, self.upper_scale_green).any():
            self.list_green.append(number)
        else:
            print("Can't convert Color")
            
            """
    def isgray2(self,imgpath, number):
        img = cv2.imread(imgpath)
        #img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #img_hsv.resize(116,82)
        #print(img_hsv[5,41])
        heigth = img.shape[0]
        width = img.shape[1]
        #print(int(heigth/20))
        #print(int(width/2))
        #print(img.shape)
        
        #print(img[int(heigth/20),int(width/4)])
        #print(img[int(heigth/20),int(width/2)])
        #print(img[int(heigth/20),int(width*3/4)])
        
        pp = []
        p1 = img[int(heigth/20),int(width/2)]
        p2 = img[int(heigth/20),int(width/4)]
        p3 = img[int(heigth/20),int(width*3/4)]
        pp.append(p1)
        pp.append(p2)
        pp.append(p3)
        
        b = [i[0] for i in pp]
        g = [i[1] for i in pp]
        r = [i[2] for i in pp]
        


        print(b)
        print(g)
        print(r)
        
        if b.any() >220 and r.any() > 220:
            print('yellow')
        elif b > 220 and r < 20 and g < 20:
            print("blue")
        elif g > 220 and b < 20 and r < 20:
            print("green")
        elif r > 220 and b< 20 and g < 20:
            print("red")
        else:
            print("Can't convert Color") 
            """

    def opendirectory(self):  
        
        self.root.directory = filedialog.askdirectory(
            initialdir='dir',
            title='select directory')
            
        self.txt2.configure(text=self.root.directory)
        
    def checkExt(self):
        self.dirname = "[정리"
        if self.checkv3.get() == True:
            self.ext.append('.pdf')
            self.dirname += ".pdf"
        if self.checkv4.get() == True:
            self.ext.append('.hwp')
            self.dirname += ".hwp"
        if self.checkv5.get() == True:
            self.ext.append('.doc')
            self.ext.append('.docx')
            self.ext.append('.docm')
            self.dirname += ".doc"
        if self.checkv6.get() == True:
            self.ext.append('.ppt')
            self.ext.append('.pptx')
            self.ext.append('.pptm')
            self.dirname += ".ppt"
        if self.checkv7.get() == True:
            self.ext.append('.xls')
            self.ext.append('.xlsx')
            self.ext.append('.xml')
            self.ext.append('.xlsm')
            self.ext.append('.xlsb')
            self.dirname += ".xls"
        if self.checkv8.get() == True:
            self.ext.append('.hwpx')
            self.dirname += ".hwpx"
        if self.checkv2.get() == True:
            self.dirname = "[정리"
        
        
    def makeup2(self):
        
        if self.txt2.cget("text") and (self.checkv2.get() or self.checkv3.get() or self.checkv4.get() or self.checkv8.get() or self.checkv5.get() or self.checkv6.get() or self.checkv7.get() ):
            self.ext.clear()
            self.checkExt()
            self.newdir = self.root.directory + self.dirname + "]"
            
            try:
                os.makedirs(self.newdir, exist_ok=False)
            except:
                shutil.rmtree(self.newdir)
                os.makedirs(self.newdir)
             
            self.spinint = int(self.spinbox1.get())
            
            if self.spinint != 0:
    
                self.numberinglist.clear()
                in_form = []
                
                for i in range(self.spinint+1):
                    self.numberinglist.append(0)
                    in_form.append('02')
                
                self.dfsmake(self.root.directory, self.spinint, in_form)
                tk.messagebox.showinfo("Complete","폴더 분류 완료")
            
            elif self.spinint == 0:
                
                self.copy_file(self.root.directory)
                tk.messagebox.showinfo("Complete","폴더 분류 완료")
        else:
            tk.messagebox.showinfo("Error","폳더 및 옵션 체크해주세요")
        
    def dfsmake(self, cur_dir, dfs_level, input_form):
        
        self.numberinglist[self.spinint] = 0
        
        if dfs_level == 0:
            numlen = int(0)
            for path, dir, files in os.walk(cur_dir):
                    
                if self.checkv2.get() == True:
                    numlen += len(files)
                else:
                    for file in files:
                        if os.path.splitext(file)[-1] in self.ext:
                            numlen += 1
                
            

            for path, dir, files in os.walk(cur_dir):
                    
                files = natsort.os_sorted(files)
                
                for filename in files:
                    if self.checkv2.get() == True:
                        self.numberinglist[self.spinint] += 1
                        form2 = input_form
                        form2[self.spinint] = self.format_num2(numlen)
                        #print(self.newname(cur_dir, filename,form2))
                        
                        shutil.copy2("%s/%s" % (path, filename), self.newdir)
                        os.rename("%s/%s" % (self.newdir, filename), self.newname(cur_dir, filename,form2))
                        
                    elif os.path.splitext(filename)[-1] in self.ext:
                        self.numberinglist[self.spinint] += 1
                        form2 = input_form
                        form2[self.spinint] = self.format_num2(numlen)
                        #print(self.newname(cur_dir, filename,form2))
                        
                        shutil.copy2("%s/%s" % (path, filename), self.newdir)
                        os.rename("%s/%s" % (self.newdir, filename), self.newname(cur_dir, filename,form2))
            return
        
        sortedlist = natsort.os_sorted(os.listdir(cur_dir))
        
        numlenf = int(0)
        if self.checkv2.get() == True:
            numlenf = len(os.walk(cur_dir).__next__()[2])
        else:
            for file in os.walk(cur_dir).__next__()[2]:
                if os.path.splitext(file)[-1] in self.ext:
                    numlenf += 1                       
        
        numlend = len(os.walk(cur_dir).__next__()[1])
        
        for filename in sortedlist:
            file_path = os.path.join(cur_dir,filename)
            if os.path.isfile(file_path):
                if self.checkv2.get() == True:
                    self.numberinglist[self.spinint] += 1
                    form2 = input_form
                    form2[self.spinint] = self.format_num2(numlenf)
                    #print(self.newname(cur_dir, filename,form2))
                    
                    shutil.copy2("%s" % file_path, self.newdir)
                    os.rename("%s/%s" % (self.newdir, filename), self.newname(cur_dir, filename,form2))
                elif os.path.splitext(filename)[-1] in self.ext:
                    self.numberinglist[self.spinint] += 1
                    form2 = input_form
                    form2[self.spinint] = self.format_num2(numlenf)
                    #print(self.newname(cur_dir, filename,form2))
                    
                    shutil.copy2("%s" % file_path, self.newdir)
                    os.rename("%s/%s" % (self.newdir, filename), self.newname(cur_dir, filename,form2))
                    
        
        for pathname in sortedlist:
            dir_path = os.path.join(cur_dir,pathname)      
            if os.path.isdir(dir_path):
                self.numberinglist[self.spinint - dfs_level] += 1
                input_form[self.spinint - dfs_level] = self.format_num2(numlend)
                outform = input_form
                if dfs_level == self.spinint:
                    for i in range(self.spinint):
                        self.numberinglist[i+1] = 0
                self.dfsmake(dir_path,dfs_level-1,outform)
    
    def newname(self, f_path , f_name , form):
        new_name = self.newdir
    
        new_name = new_name + '/'
        for i in range(len(self.numberinglist)):
            new_name = new_name + '[' + str(format(self.numberinglist[i], form[i])) + ']_'
        new_name += f_name
        
        
        return new_name
            
    def format_num(self, files):
        output = '06'
        if len(files) < 10:
            output = '02'
        elif len(files) < 100:
            output = '03'
        elif len(files) >= 100 and len(files) < 1000:
            output = '04'
        elif len(files) >= 1000 and len(files) < 10000:
            output = '05'
        return output
        
    def format_num2(self, num):
        output = '06'
        if num < 10:
            output = '02'
        elif num < 100:
            output = '03'
        elif num >= 100 and num < 1000:
            output = '04'
        elif num >= 1000 and num < 10000:
            output = '05'
        return output
        
        
    def enum_folder_only(self, dirname):
        for filename in os.listdir(dirname):
            file_path = os.path.join(dirname,filename)
            if os.path.isdir(file_path):
                self.dir_list.append(file_path)
                
    def enum_file_only(self, dirname):
        for filename in os.listdir(dirname):
            file_path = os.path.join(dirname,filename)
            
            if not os.path.isdir(file_path):
                self.fil_list.append(file_path)
                 
        
    def copy_file(self, dirname):
        numbering = int(1)
        numlen = int(0)
        for (path, dir, files) in os.walk(dirname):
            numlen += len(files)
        
        for (path, dir, files) in os.walk(dirname):
                
            files = natsort.os_sorted(files)
            
            for filename in files:
                if os.path.splitext(filename)[-1] in self.ext:
                    print("%s/%s" % (path, filename))
                    shutil.copy2("%s/%s" % (path, filename), self.newdir)
                    os.rename("%s/%s" % (self.newdir, filename), 
                              self.newdir+'/['+
                              str(format(numbering, self.format_num2(numlen)))+']_'+filename)
                    numbering += 1
    

class Login():
    def __init__(self, key= None):
       self.root = tk.Tk()
       self.root.title("Sub File")
       self.root.geometry("300x100+200+200")
       self.root.resizable(False,False)
       self.strvar = ""
       self.current =""
       self.new = ""
       self.textb = tk.Entry(self.root,width=20,textvariable=self.strvar,show="*")
       
       self.button1 = tk.Button(self.root,
                               text="Insert",
                               command=self.inputPwd)
       self.currentPwd = tk.Entry(self.root,width=20,textvariable=self.current,show="*")
       self.newPwd = tk.Entry(self.root,width=20,textvariable=self.new,show="*")
       self.button2 = tk.Button(self.root,
                               text="ChangePassword",
                               command=self.ChangePassword)
       self.txt1 = tk.Label(self.root, text ="Password : ")
       self.txt2 = tk.Label(self.root, text ="현재비밀번호 : ")
       self.txt3 = tk.Label(self.root, text ="변경후비밀번호 : ")
       
       
       self.txt1.grid(row = 0, column = 0)
       self.textb.grid(row = 0, column = 1)
       self.textb.focus()
       self.button1.grid(row = 0, column = 2)
       self.txt2.grid(row = 1, column = 0)
       self.txt3.grid(row = 2, column = 0)
       self.currentPwd.grid(row = 1, column = 1)
       self.newPwd.grid(row = 2, column = 1)
       self.button2.grid(row = 3, column = 1)
           
       
       if self.textb.focus:
           self.textb.bind('<Return>', self.inputPwd)
       if self.newPwd.focus or self.currentPwd.focus:
           self.newPwd.bind('<Return>', self.ChangePassword)
           self.currentPwd.bind('<Return>',self.ChangePassword)
       self.conn = sqlite3.connect("test.db", isolation_level=None)

       self.c= self.conn.cursor()

       self.c.execute("CREATE TABLE IF NOT EXISTS table1  \
                       (id integer PRIMARY KEY, password text)")
     
       self.root.mainloop()
        
    def inputPwd(self):
       self.strvar =self.textb.get().strip()
       self.c.execute("SELECT * FROM table1 WHERE id=:Id",{"Id":1})
       a = list(self.c.fetchone())
       b = hashlib.sha256(self.strvar.encode()).hexdigest()
       if b == a[1]:
           self.conn.close()
           self.root.destroy()
           app=MainFrame()
       else:
           self.textb.delete(0,100)
           tk.messagebox.showinfo("Error", "비밀번호 확인")
           print("Password Error")

    def ChangePassword(self):
        self.current = self.currentPwd.get().strip()
        self.new = self.newPwd.get().strip()
        self.c.execute("SELECT * FROM table1 WHERE id=:Id",{"Id":1})
        a = list(self.c.fetchone())
        b = hashlib.sha256(self.current.encode()).hexdigest()
        if b==a[1]:
            self.c.execute("UPDATE table1 SET password=? WHERE id=?", 
                      (hashlib.sha256(self.new.encode()).hexdigest(), 1))
            self.currentPwd.delete(0,100)
            self.newPwd.delete(0,100)
        elif self.current == self.new:
            tk.messagebox.showinfo("Error","비밀번호 동일")
            print("Same Password Please insert different Password")
            self.currentPwd.delete(0,100)
            self.newPwd.delete(0,100)
        else :
            tk.messagebox.showinfo("Error","비밀번호 확인")
            print("Password Error")
            self.currentPwd.delete(0,100)
            self.newPwd.delete(0,100)

app = Login()