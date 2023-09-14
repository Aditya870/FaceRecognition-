from tkinter import *
from tkinter import messagebox

import cv2
import os
import numpy as np
import sqlite3 as sq

face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0);
samplenum=0

class AddStudent(Toplevel):

    def submit_data(self):
        answer= messagebox.askquestion("confirm","Do you really want to submit")
        if(answer=='yes'):

                Id=self.rollentry.get()
                Namee=self.nameentry.get()
                Agee=(self.ageentry.get())
                Gendere=self.genderentry.get()
                Departmente=self.departmententry.get()
                Id=Id.upper()
                conn = sq.connect("FaceAttendance.db")
                cmd = "SELECT * FROM Student WHERE ID=" + "\"" + Id + "\""
                cursor = conn.execute(cmd)
                isRecordExist = 0
                for row in cursor:
                    isRecordExist = 1
                if (isRecordExist == 1):
                    cmd = "UPDATE Student SET Name=" + "\"" + Namee + "\"" + " WHERE ID=" + "\"" + Id + "\""
                else:
                    cmd = "INSERT INTO Student(ID,Name,Age,Gender,Department) Values(" + "\"" + Id + "\"" + "," + "\"" + Namee + "\"" + "," + str(
                        Agee) + "," + "\"" + Gendere + "\"" + "," + "\"" + Departmente + "\"" + ") "

                conn.execute(cmd)
                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Data Entered Successfully")
                self.destroy()


    def create_dataset(self):
        Id=self.rollentry.get()
        Id.upper()
        d = {1: 'IT', 2: 'EC', 3: 'ME', 4: 'LT', 5: 'EE', 6: 'C'}
        if 'LE' in Id:
            Id = Id.replace("LE", '1')
            for k, v in d.items():
                if v in Id:
                    Id = Id.replace(v, str(k))
        else:
            for k, v in d.items():
                if v in Id:
                    Id = Id.replace(v, "0" + str(k))

        face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0);
        samplenum = 0
        while (cam.isOpened()):
            ret, img = cam.read();
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_haar_cascade.detectMultiScale(gray, 1.3, 5);
            for (x, y, w, h) in faces:
                samplenum += 1;
                cv2.imwrite("dataSet/User." + Id + "." + str(samplenum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.waitKey(100);
            cv2.imshow("Face", img);
            cv2.waitKey(1);
            if (samplenum > 80):
                break;

        cam.release()
        cv2.destroyAllWindows()


    def __init__(self):
        Toplevel.__init__(self)

        self.geometry("800x650+350+10")
        self.title("Add Student")
        self.resizable(False, False)

        # frames
        self.top = Frame(self, height=150, bg='#ffffff')
        self.top.pack(fill=X)

        self.bottom = Frame(self, height=450, bg='white')
        self.bottom.pack(fill=X)
        self.bottominner = Frame(self.bottom, height=440,width=680, bg='#ffa600')
        self.bottominner.place(x=60,y=10)


        self.developer = Frame(self, height=50, bg='#101036')
        self.developer.pack(fill=X)

        # Top Frame Design
        self.top_image = PhotoImage(file='newicons/stud.png')
        self.top_image_label = Label(self.top, image=self.top_image, bg='white')
        self.top_image_label.place(x=100, y=20)

        self.heading = Label(self.top, text=" New Student DataSet ", font='arial 15 bold', bg='white',
                             fg='#45daff')
        self.heading.place(x=350, y=90)

        # footer label
        self.foo = Label(self.developer, text="Developed by MIT 2K16(IT)", font='arial 15 bold', bg='#101036',
                         fg='white')
        self.foo.place(x=250, y=9)

        self.km = Label(self.bottominner, text="      ", width=20, font=("bold", 10), bg='#ffa600')
        self.km.grid(row=0, padx=10, pady=10)

        self.roll = Label(self.bottominner,text="Enter Student Roll No.   ",width=20,font=("bold",10),bg='#ffa600')
        self.roll.grid(row=1,padx=10,pady=10)

        self.name = Label(self.bottominner, text="Enter Student Name      ", width=20, font=("bold", 10),bg='#ffa600')
        self.name.grid(row=2,padx=10,pady=10)

        self.age = Label(self.bottominner, text="Enter Student Age        ", width=20, font=("bold", 10),bg='#ffa600')
        self.age.grid(row=3,padx=10,pady=10)

        self.gender = Label(self.bottominner, text="Enter Student Gender    ", width=20, font=("bold", 10),bg='#ffa600')
        self.gender.grid(row=4,padx=10,pady=10)

        self.department = Label(self.bottominner, text="  Enter Student Department", width=20, font=("bold", 10),bg='#ffa600')
        self.department.grid(row=5,padx=10,pady=10)

        self.rollentry=Entry(self.bottominner,width=80)
        self.rollentry.grid(row=1,column=1,padx=5,pady=10,ipady=3)

        self.nameentry = Entry(self.bottominner, width=80)
        self.nameentry.grid(row=2, column=1, padx=5, pady=10, ipady=3)

        self.ageentry = Entry(self.bottominner, width=80)
        self.ageentry.grid(row=3, column=1, padx=5, pady=10, ipady=3)

        self.genderentry = Entry(self.bottominner, width=80)
        self.genderentry.grid(row=4, column=1, padx=5, pady=10, ipady=3)

        self.departmententry = Entry(self.bottominner, width=80)
        self.departmententry.grid(row=5, column=1, padx=5, pady=10, ipady=3)

        self.databutton=Button(self.bottominner,text='Create Dataset',width=35,bg='red',fg='white',font=("bold", 10),command=self.create_dataset)
        self.databutton.grid(row=6,columnspan=2,padx=10,pady=10)

        self.submitbutton = Button(self.bottominner, text='Submit', width=80, bg='green', fg='white',
                                 font=("bold", 10),command=self.submit_data)
        self.submitbutton.grid(row=8, columnspan=2, padx=10, pady=10)

        #extra material
        self.kj = Label(self.bottominner, text="      ", width=20, font=("bold", 10), bg='#ffa600')
        self.kj.grid(row=10, padx=10, pady=10)







