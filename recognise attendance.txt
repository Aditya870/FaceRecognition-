import os
import cv2
import numpy as np
from PIL import Image
from tkinter import messagebox
from tkinter import *
import datetime
import sqlite3 as sq


class RecogniseAttendance():
    def __init__(self):
        answer = messagebox.askquestion("confirm", "Do you really want to take Attendance")
        if (answer == 'yes'):
            face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            cam = cv2.VideoCapture(0);

            roc = cv2.face.LBPHFaceRecognizer_create();
            roc.read("recognizer/trainingData.yml")

            id = 0
            font = cv2.FONT_HERSHEY_SIMPLEX

            def find(id):
                x = id
                l = []
                while (x != 0):
                    z = x % 10
                    l.append(z)
                    x = x // 10
                l.reverse()
                d = {1: 'IT', 2: 'EC', 3: 'ME', 4: 'LT', 5: 'EE', 6: 'C'}
                if (l[2] == 0):
                    l.pop(2)
                    l[2] = d[l[2]]

                elif (l[2] == 1):
                    l[2] = 'LE'
                    l[3] = d[l[3]]

                stri = ''
                for x1 in l:
                    stri = stri + str(x1)
                return (stri)

            def getProfile(id):
                conn = sq.connect("FaceAttendance.db")
                cmd = "SELECT * FROM Student WHERE ID=" + "\"" + (id) + "\""
                cursor = conn.execute(cmd)
                profile = None
                for row in cursor:
                    profile = row
                conn.close()
                return profile

            def dateTimeWork(Id, date, time):
                conn = sq.connect("FaceAttendance.db")
                cmd = "SELECT ID,Date FROM Attendance WHERE ID=" + "\"" + Id + "\"" + " AND Date=" + "\"" + date + "\""
                cursor = conn.execute(cmd)
                isRecordExist = 0
                for row in cursor:
                    isRecordExist = 1
                if (isRecordExist == 1):
                    pass
                else:
                    cmd = "INSERT INTO Attendance(ID,Date,Time) Values(" + "\"" + Id + "\"" + "," + "\"" + date + "\"" + "," + "\"" + time + "\"" + ") "
                    conn.execute(cmd)
                conn.commit()
                conn.close()

            while (cam.isOpened()):
                ret, img = cam.read()
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_haar_cascade.detectMultiScale(gray_img, 1.3, 5);
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    id, conf = roc.predict(gray_img[y:y + h, x:x + w])

                    v = datetime.datetime.now()
                    v = "" + str(v.astimezone())
                    date = v.split(" ")[0]
                    time = v.split(" ")[1].split('.')[0]

                    id = find(id)

                    dateTimeWork(id, date, time)
                    profile = getProfile(id)
                    if (profile != None):
                        cv2.putText(img, "Name: " + profile[1], (x, y + h + 30), font, 0.5, (0, 0, 255), 1)
                        cv2.putText(img, "Age: " + str(profile[2]), (x, y + h + 60), font, 0.5, (0, 0, 255), 1)
                        cv2.putText(img, "Gender: " + profile[3], (x, y + h + 90), font, 0.5, (0, 0, 255), 1)
                        cv2.putText(img, "Department: " + profile[4], (x, y + h + 120), font, 0.5, (0, 0, 255), 1)
                    # cv2.putText(img, profile[4], (x, y + h + 150), font, 2, (0, 0, 255), 2)
                cv2.imshow("Face", img);
                if (cv2.waitKey(1) == ord('q')):
                    break;

            cam.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Success", "Attendance Entered Successfully")



