# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 01:29:12 2021

@author: whdyd
"""

from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter
import cv2
import os
import sys
from tkinter import filedialog
import numpy as np
import tkinter as tk
import tkinter.messagebox
from xdwlib import xdwopen
import xdwlib as xd
import hashlib
import sqlite3

def current_path(dir_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, dir_path)
    return os.path.join(".", dir_path)

class abcd():
    def __init__(self, key= None):
       self.root = tk.Tk()
       self.root.title("Sub File")  
       self.root.resizable(False,False)
       self.strvar = ""
       self.current =""
       self.new = ""
       self.textb = tk.Entry(self.root,width=15,textvariable=self.strvar,show="*")
       
       self.button1 = tk.Button(self.root,
                               text="Insert",
                               command=self.inputPwd)
       self.currentPwd = tk.Entry(self.root,width=15,textvariable=self.current,show="*")
       self.newPwd = tk.Entry(self.root,width=15,textvariable=self.new,show="*")
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
        
    def inputPwd(self,event):
       self.strvar =self.textb.get().strip()
       self.c.execute("SELECT * FROM table1 WHERE id=:Id",{"Id":1})
       a = list(self.c.fetchone())
       b = hashlib.sha256(self.strvar.encode()).hexdigest()
       if b == a[1]:
           self.conn.close()
           self.root.destroy()
           app=Test()
       else:
           self.textb.delete(0,100)
           tk.messagebox.showinfo("Error", "비밀번호 확인")
           print("Password Error")
       
    def ChangePassword(self,event):
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
        
class Test():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SubFile")
        self.root.geometry("800x300+200+200")
        self.root.resizable(True,True)
        
        self.txt = tk.Label(self.root, text = " ")
        self.button1 = tk.Button(self.root,
                                text="open files",
                                command=self.openpdf)
        
        self.button2 = tk.Button(self.root,
                                 text = "run",
                                 command=self.readLabelText)
       
        
        self.filenames = []
        self.filepaths = []
        
        self.color_list=[]
        self.gray_list=[]
        self.RadioVariety = tk.IntVar() 
        self.r1 = tk.Radiobutton(self.root,text = "단면",
                                 variable=self.RadioVariety,value=1)
        self.r2 = tk.Radiobutton(self.root,text = "양면",
                                 variable=self.RadioVariety,value=2)
        
        self.button1.pack()
        self.button2.pack()
        self.r1.pack()
        self.r2.pack()
        self.txt.pack()
        self.root.mainloop()
        self.pages = 0
      
    #pdf 열기
    def openpdf(self):  
        
        self.filepaths.clear()
        self.filenames.clear()
        
        self.root.file = filedialog.askopenfilenames(
            initialdir='dir',
            title='select file',
            filetypes=(('all files','*.*'),
                       ('pdf files', '*.pdf'),
                       ('xdw files', '*.xdw')))
        
        filename = ""
        
        for i, v in enumerate(self.root.file):
            filename += v + "\n"
            self.filenames.append(self.getFileName(v))
            self.filepaths.append(v)
        self.txt.configure(text=filename)
        
    def readLabelText(self):
        if self.RadioVariety.get() == 1 or self.RadioVariety.get() == 2:
            for i, filename in enumerate(self.filenames):
                temp = os.path.splitext(filename)
                if temp[-1] == ".pdf":
                    self.filepaths[i] = self.filepaths[i].rstrip('/' + filename)
                    self.sub_pdf(self.filepaths[i], filename)
                    self.classify(self.filepaths[i], filename)
                elif temp[-1] ==".xdw" :
                    self.filepaths[i] = self.filepaths[i].rstrip('/' + filename)
                    self.classify_xdw(self.filepaths[i],filename,temp[0])
                else :
                    tk.messagebox.showinfo("Error","파일 확인")
            
            tk.messagebox.showinfo("Complete","분류 완료")
        else :
            tk.messagebox.showinfo("Error","단면 or 양면 선택")
        
    def getFileName(self, path):
        str = path.split('/')
        return str[len(str)-1]
    
    def sub_pdf(self, pdfpath, file_name):
        self.gray_list.clear()
        self.color_list.clear()
        os.environ["PATH"] += os.pathsep + \
        os.pathsep.join([current_path("poppler")])
        
        self.pages = convert_from_path(pdfpath + "\\" + file_name)

        if self.RadioVariety.get() == 1:
            for i, page in enumerate(self.pages):
                page.save(pdfpath + "\\" + file_name+str(i)+".jpg", "JPEG")
            
                if isgray(pdfpath + "\\" + file_name+str(i)+".jpg") :
                    self.gray_list.append(i)
                else :
                    self.color_list.append(i)
                
        elif self.RadioVariety.get() == 2:

            for i, page in enumerate(self.pages):
                page.save(pdfpath + "\\" + file_name+str(i)+".jpg", "JPEG")
            
            
            for i in range(0, len(self.pages), 2):
                if i == len(self.pages)-1:
                    if isgray(pdfpath +"\\" + file_name+str(len(self.pages)-1)+".jpg"):
                        self.gray_list.append(len(self.pages)-1)
                    else:
                        self.color_list.append(len(self.pages)-1)
                    break
                if isgray(pdfpath +"\\" + file_name+str(i)+".jpg") and isgray(pdfpath +"\\" + file_name+str(i+1)+".jpg"):
                    self.gray_list.append(i)
                    self.gray_list.append(i+1)
                else :
                    self.color_list.append(i)
                    self.color_list.append(i+1)
                
    def classify_xdw(self, imgpath1, file_name, file_name2):
        try:    
            doc = xdwopen(imgpath1+"\\"+file_name)
            colorpage = xd.PageCollection()
            greypage = xd.PageCollection()
            
            if self.RadioVariety.get() == 1: #단면
                for j in range(doc.pages):
                    if doc.page(j).is_color:
                        colorpage += doc.page(j)
                    else:
                        greypage += doc.page(j)
                        
            elif self.RadioVariety.get() == 2: #양면
                for j in range(0,doc.pages,2):
                    if j == doc.pages -1:
                        if doc.page(j).is_color:
                            colorpage += doc.page(j)
                        else :
                            greypage += doc.page(j)
                    elif not doc.page(j).is_color and not doc.page(j+1).is_color:
                        greypage += doc.page(j)
                        greypage += doc.page(j+1)
                    else :
                        colorpage += doc.page(j)
                        colorpage += doc.page(j+1)
                        
            outputpath = imgpath1 +"\\"+file_name2+"_color.xdw"
            outputpath2 = imgpath1 +"\\"+file_name2+"_grey.xdw"
            colorpage.export(str(outputpath),True)
            greypage.export(str(outputpath2), True)
            doc.close()
        except :
            doc.close()
                
    def classify(self, imgpath1,file_name):
        pdf = PdfFileReader(open(imgpath1 +"\\" + file_name,'rb'), strict= False)
        numberPages = pdf.getNumPages()
        pdf_writer_gray = PdfFileWriter()
        pdf_writer_color = PdfFileWriter()
        for page in self.gray_list:
            pdf_writer_gray.addPage(pdf.getPage(page))
        
        output_name = file_name + "_grey.pdf"
        save_path = os.path.join(imgpath1, output_name)
        
        with open(save_path, 'wb') as f:
            pdf_writer_gray.write(f)    
            
        for page in self.color_list:
            pdf_writer_color.addPage(pdf.getPage(page))
                
        output_name = file_name + "_color.pdf"
        save_path = os.path.join(imgpath1+"", output_name)
       
        with open(save_path, 'wb') as f:
            pdf_writer_color.write(f)
            
        for i in range(numberPages):
            os.remove(imgpath1+"\\"+file_name+str(i)+".jpg")

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
        
def  imread_hangul_path(imgpath):
    with open(imgpath, "rb") as fp:
        bytes = bytearray(fp.read())
        numpy_array = np.asarray(bytes, dtype=np.uint8)
    return cv2.imdecode(numpy_array, cv2.IMREAD_UNCHANGED)
        
def isgray(imgpath):
   img = imread_hangul_path(imgpath)
   img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   lower_scale = (0,10,0)
   upper_scale = (180,220,255)
        
   if cv2.inRange(img_hsv, lower_scale,upper_scale).any() :
       return False
   else : 
       return True
    
def createNewFoler(pdfpath,file_name):
    createFolder(pdfpath+"\\"+file_name+"_sub")
    createFolder(pdfpath+"\\"+file_name+"_sub\\color")
    createFolder(pdfpath+"\\"+file_name+"_sub\\gray")

app = abcd()