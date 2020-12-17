
import tkinter as tk
from tkinter import Message ,Text,Label
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from keras_facenet import FaceNet
from face_recognition import dictq
from face_recognition import extract_face
import matplotlib.pyplot as plt
import sqlite3
import csv

window = tk.Tk()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
some=str(screen_width)+"x"+str(screen_height)
window.geometry(some)
window.title("attendance system")
file = 'uvce_vector.png'

image = Image.open(file)

zoom =0.5
dialog_title = 'QUIT'
dialog_text = 'Are you sure?'


#window.configure(background='blue')
img = ImageTk.PhotoImage(image.resize((screen_width, screen_height))) 
label = Label(window, image=img)
label.image = img
label.pack()

def process_click(event, x, y,flags, params):
    global identity
    if event == cv2.EVENT_LBUTTONDOWN:
        if y > button[0] and y < button[1] and x > button[2] and x < button[3]:
            import pyttsx3
            engine = pyttsx3.init()
            if(unknown_yes_or_no=="yes"):
                engine.say("Good morning sorry we couldn't recognise you")
            else:
                str1="good morning "+identity+" your attendance has been recorded"
                engine.say(str1)
                conn = sqlite3.connect('face.db')
                sql = ''' INSERT INTO TEACHERS_ATTENDANCE(NAME,DATE_PRESENT,SESSION)
                VALUES(?,?,?) '''
                from datetime import date
                today1 = date.today()
                values=(identity,str(today1),"morning")
                cur = conn.cursor()
                cur.execute(sql,values)
                conn.commit()

                engine.runAndWait()



#window.grid_rowconfigure(0, weight=1)
#window.grid_columnconfigure(0, weight=1)
button = [20,60,50,250]
cv2.namedWindow('Control')
cv2.setMouseCallback('Control',process_click)
identity=""

def trackimage():
    global identity
    embedder = FaceNet()
    b=[]
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        img1=extract_face(frame)
        plt.imshow(frame)
        img1=np.expand_dims(img1,axis=0)
        if(img1.any()):
            emb=embedder.embeddings(img1)
            emb=np.transpose(emb)
            min_dist=100
            for key,value in dictq.items():
                dist=np.linalg.norm(emb-value)
                b.append(dist)
                if dist<min_dist:
                    min_dist=dist
                    identity=key
            #print(identity)  #to print the identity 
            if min_dist < 1.0:
                cv2.putText(frame, "Face : " + identity,(100,100),cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0,255), 2)
            else:
                cv2.putText(frame,'no match',(100,100),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
            cv2.imshow('face',frame)
            cv2.setMouseCallback('Control',process_click)
            control_image = np.zeros((80,300), np.uint8)
            control_image[button[0]:button[1],button[2]:button[3]] = 180
            cv2.putText(control_image, 'Yes',(100,50),cv2.FONT_HERSHEY_PLAIN, 2,(0),3)
            cv2.imshow('Control', control_image)

            if cv2.waitKey(1) & 0xFF==27:
                break

    cap.release()
    cv2.destroyAllWindows()
    



message = tk.Label(window, text="UVCE CSE",bg="Green"  ,fg="white"  ,width=30  ,height=2,font=('times',20, 'italic bold underline')) 

message.place(x=400, y=20)


def exit1():
    exit()

def getattendanceascsv():
    inputValue=textBox.get("1.0","end-1c")
    conn = sqlite3.connect('face.db')
    sql = ''' SELECT * FROM TEACHERS_ATTENDANCE WHERE date_present=? '''
    cur = conn.cursor()
    cur.execute(sql,(inputValue,))
    rows = cur.fetchall()
    name='attendance'+inputValue+'.csv'
    with open(name,'w') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['id','name','date','session'])
        for row in rows:
            newFileWriter.writerow([row[0],row[1],row[2],row[3]])
            





def process_click(event, x, y,flags, params):
    global identity
    if event == cv2.EVENT_LBUTTONDOWN:
        if y > button[0] and y < button[1] and x > button[2] and x < button[3]:
            import pyttsx3
            engine = pyttsx3.init()
            str1="good morning "+identity+" your attendance has been recorded"
            engine.say(str1)
            conn = sqlite3.connect('face.db')
            sql = ''' INSERT INTO TEACHERS_ATTENDANCE(NAME,DATE_PRESENT,SESSION)
            VALUES(?,?,?) '''
            from datetime import date,datetime
            now=datetime.now()
            current_time = now.strftime("%H:%M")
            today1 = date.today()

            values=(identity,str(today1),current_time)
            cur = conn.cursor()
            cur.execute(sql,values)
            conn.commit()

            engine.runAndWait()








textBox=tk.Text(window, height=4, width=15)
textBox.place(x=1000, y=450)
buttonCommit=tk.Button(window, height=3, width=20, text="Click here to get attendance", 
                    command=lambda: getattendanceascsv(),fg="red",bg="yellow",activebackground = "Red" ,font=('times', 13, ' bold '))
buttonCommit.place(x=750,y=450)
trackImg = tk.Button(window, text="Click here to start App",wraplength=200,justify='left',command=trackimage  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=200, y=450)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=480, y=450)
 
window.mainloop()
