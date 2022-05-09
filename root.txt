from tkinter import *
from add_student import AddStudent
import os
import cv2
import numpy as np
from PIL import Image
from tkinter import messagebox
from Recognise_Attendance import RecogniseAttendance
from attendance_sheet import AttendanceSheet

class Application(object):
    def __init__(self,master):
        self.master=master

        #frames
        self.top=Frame(master,height=150,bg='#ffffff')
        self.top.pack(fill=X)

        self.bottom=Frame(master,height=450,bg='#45daff')
        self.bottom.pack(fill=X)

        self.developer = Frame(master, height=50, bg='#101036')
        self.developer.pack(fill=X)

        #Top Frame Design
        self.top_image=PhotoImage(file='newicons/face-recognition3.png')
        self.top_image_label=Label(self.top,image=self.top_image,bg='white')
        self.top_image_label.place(x=100,y=20)

        self.heading=Label(self.top,text="My Intelligent Attendance APP",font='arial 15 bold',bg='white',fg='#ebb434')
        self.heading.place(x=300,y=70)


        #footer label
        self.foo = Label(self.developer, text="Developed by MIT 2K16(IT)", font='arial 15 bold',bg='#101036',
                             fg='white')
        self.foo.place(x=250, y=9)

        #button 1
        self.add_student=Button(self.bottom,text="                    Add New Student                    ",font="arial 12 bold",bg='#030303',fg='white',command=self.add_Student).place(x=250,y=60)
        #button 2
        self.train_dataset=Button(self.bottom,text="                    Train Dataset                            ",font="arial 12 bold", bg='#030303', fg='white',command=self.train_me).place(x=250, y=110)
        # button 3
        self.recognise_attendance = Button(self.bottom, text="                    Recognize + Attendance       ",font="arial 12 bold", bg='#030303', fg='white',command=self.recognise_me).place(x=250, y=160)
        # button 4
        self.report = Button(self.bottom, text="                    Attendance Sheet                    ",
                                  font="arial 12 bold", bg='#030303',command=self.show_attendance, fg='white').place(x=250, y=210)
        # button 5
        self.details = Button(self.bottom, text="                    Developers                                ",
                                  font="arial 12 bold", bg='#030303',command=self.show_developer, fg='white').place(x=250, y=260)
        # button 6
        self.exit = Button(self.bottom, text="                    Exit                                               ",
                                  font="arial 12 bold", bg='#030303',command=self.exitapp, fg='white').place(x=250, y=310)

    def add_Student(self):
        student=AddStudent()

    def train_me(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        path = 'dataSet'

        def getImagesWithID(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faces = []
            IDs = []
            for imagePath in imagePaths:
                faceImg = Image.open(imagePath).convert('L');
                faceNp = np.array(faceImg, 'uint8')
                ID = int(os.path.split(imagePath)[-1].split('.')[1])
                faces.append(faceNp)
                print(ID)
                IDs.append(ID)
                cv2.imshow("training", faceNp)
                cv2.waitKey(10)
            return IDs, faces

        Ids, faces = getImagesWithID(path)
        recognizer.train(faces, np.array(Ids))
        recognizer.save('recognizer/trainingData.yml')
        cv2.destroyAllWindows()
        messagebox.showinfo("Success", "Training Successfull")

    def recognise_me(self):
        attend=RecogniseAttendance()

    def show_attendance(self):
        sheet=AttendanceSheet()

    def show_developer(self):
        cttt='''We are the developers from Mitian Group
         contact=xxxxxxxxxx
         email=abc@gmail.com
                        Thank You.'''
        messagebox.showinfo("Developer", cttt)

    def exitapp(self):
        answerexit = messagebox.askquestion("confirm", "Do you really want to exit")
        if (answerexit == 'yes'):
            messagebox.showinfo("Success", "Closing the Application")
            self.master.destroy()
        else:pass



def main():
    root=Tk()
    app=Application(root)
    root.title("Face Recognition Based Attendance Monitoring System")
    root.geometry("800x650+250+10")
    root.resizable(False,False)
    root.mainloop()



if __name__=='__main__':
    main()
