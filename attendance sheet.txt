from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import xlsxwriter as df

import os
import numpy as np
import sqlite3 as sq



class AttendanceSheet(Toplevel):


    def __init__(self):
        Toplevel.__init__(self)
        self.flag2=0
        self.fetchkey=0
        self.datekey=0
        self.allkey=0

        self.geometry("1200x650+50+10")
        self.title("Attendance Sheet")
        self.resizable(False, False)

        # frames
        self.top = Frame(self, height=150, bg='#ffffff')
        self.top.pack(fill=X)

        self.bottom = Frame(self, height=450, bg='white')
        self.bottom.pack(fill=X)
        self.bottominner1 = Frame(self.bottom, height=440,width=640, bg='pink')
        self.bottominner1.place(x=20,y=10)
        self.bottominner2 = Frame(self.bottom, height=440, width=540, bg='#bbdd56')
        self.bottominner2.place(x=661, y=10)


        self.developer = Frame(self, height=50, bg='#101036')
        self.developer.pack(fill=X)

        # Top Frame Design
        self.top_image = PhotoImage(file='newicons/att.png')
        self.top_image_label = Label(self.top, image=self.top_image, bg='white')
        self.top_image_label.place(x=100, y=10)

        self.heading = Label(self.top, text=" Attendance Sheet ", font='arial 20 bold', bg='white',
                             fg='#45daff')
        self.heading.place(x=450, y=80)

        # footer label
        self.foo = Label(self.developer, text="Developed by MIT 2K16(IT)", font='arial 15 bold', bg='#101036',
                         fg='white')
        self.foo.place(x=450, y=9)


        #bottominner2 design
        self.combocreate()


    def combocreate(self):
        # bottominner2 design
        self.combobox = Combobox(self.bottominner2, width=44)
        items = ("---select---", "Select All", "Roll No", "Date")
        self.combobox['values'] = items
        self.combobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.onChangeValue)
        self.combobox.grid(row=5, column=1,columnspan=3,padx=10, pady=10)
        self.search = Label(self.bottominner2, text="Search By   ", width=25, font=("bold", 10), bg="#bbdd56")
        self.search.grid(row=5, column=0, padx=5, pady=10)
        self.km1 = Label(self.bottominner2, text="      ", width=20, font=("bold", 10), bg='#bbdd56')
        self.km1.grid(row=0, padx=10, pady=10)
        self.km = Label(self.bottominner2, text="      ", width=20, font=("bold", 10), bg='#bbdd56')
        self.km.grid(row=1000, padx=10, pady=10)

    def fetchByRoll(self):

        self.scroll=Scrollbar(self.bottominner1,orient=VERTICAL)
        self.listbox=Listbox(self.bottominner1,width=80,height=27)
        self.listbox.grid(row=0,column=0)
        self.scroll.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scroll.set)

        self.scroll.grid(row=0,column=1,sticky=N+S)
        Id = self.rollentry.get()

        conn = sq.connect("FaceAttendance.db")
        cmd= "SELECT * FROM Attendance WHERE ID=" + "\"" + Id + "\""
        student = conn.execute(cmd).fetchall()
        if(len(student)>0):
            count=0
            self.listbox.insert(count," ID "+"               "+" Date "+"               "+" Time "+"  ")
            count+=1
            for students in student:
                self.listbox.insert(count," "+ students[0]+" "  + "     " +" "+ students[1]+" "+ "     " + " "+ students[2]+" "+ "  ")
                count+=1
        else :
            count = 0
            self.listbox.insert(count, "Record not Exist")
        self.fetchkey=1


    def fetchByDate(self,y):
        self.scroll = Scrollbar(self.bottominner1, orient=VERTICAL)
        self.listbox = Listbox(self.bottominner1, width=80, height=27)
        self.listbox.grid(row=0, column=0)
        self.scroll.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scroll.set)

        self.scroll.grid(row=0, column=1, sticky=N + S)


        conn = sq.connect("FaceAttendance.db")
        cmd = "SELECT * FROM Attendance WHERE Date=" + "\"" + y + "\""
        student = conn.execute(cmd).fetchall()
        if (len(student) > 0):
            count = 0
            self.listbox.insert(count, " ID " + "               " + " Date " + "               " + " Time " + "  ")
            count += 1
            for students in student:
                self.listbox.insert(count, " " + students[0] + " " + "     " + " " + students[1] + " " + "     " + " " +
                                    students[2] + " " + "  ")
                count += 1
        else:
            count = 0
            self.listbox.insert(count, "Record not Exist")
        self.datekey = 1

    def fetchByAll(self):
        self.scroll = Scrollbar(self.bottominner1, orient=VERTICAL)
        self.listbox = Listbox(self.bottominner1, width=80, height=27)
        self.listbox.grid(row=0, column=0)
        self.scroll.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scroll.set)

        self.scroll.grid(row=0, column=1, sticky=N + S)


        conn = sq.connect("FaceAttendance.db")
        cmd = "SELECT * FROM Attendance "
        student = conn.execute(cmd).fetchall()
        if (len(student) > 0):
            count = 0
            self.listbox.insert(count, " ID " + "               " + " Date " + "               " + " Time " + "  ")
            count += 1
            for students in student:
                self.listbox.insert(count, " " + students[0] + " " + "     " + " " + students[1] + " " + "     " + " " +
                                    students[2] + " " + "  ")
                count += 1
        else:
            count = 0
            self.listbox.insert(count, "Record not Exist")

        self.allkey=1

    #function to excel
    def fetchByDateexcel(self, y):
        conn = sq.connect("FaceAttendance.db")
        cmd = "SELECT * FROM Attendance WHERE Date=" + "\"" + y + "\""
        student = conn.execute(cmd).fetchall()
        if (len(student) > 0):
            stm="C:\\Users\\Aditya\\PycharmProjects\\New_projectTKINTER\\"+y+".xlsx"
            w=df.Workbook(stm)
            w1=w.add_worksheet(y)
            w1.write("A1","Roll No")
            w1.write("B1", "Date")
            w1.write("C1", "Time")
            itm=1
            for students in student:
                w1.write(itm,0,students[0])
                w1.write(itm, 1, students[1])
                w1.write(itm, 2, students[2])
                itm += 1
            messagebox.showinfo("Sucess", "Excel sheet generated")
            w.close()
        else:
            messagebox.showinfo("Error!!!", "Record Not Exist, Please Enter Correct Date")
        self.datekey = 1




    def onChangeValue(self,object):
        getvalue=str(self.combobox.get())

        if(getvalue=="Select All"):
            if (self.flag2 == 2):
                list = [self.date, self.combodate, self.combomonth, self.comboyear,self.submitbutton,self.submitbuttonexcel]
                for x in list:
                    x.destroy()
            if (self.flag2 == 1):
                self.roll.destroy()
                self.rollentry.destroy()
                self.submitbutton2.destroy()
            if (self.fetchkey == 1 or self.datekey==1):
                self.listbox.destroy()
                self.datekey = 0
                self.fetchkey = 0

            self.flag2=0
            self.fetchByAll()

        if (getvalue == "Roll No"):
            if(self.flag2==2):
                list=[self.date,self.combodate,self.combomonth,self.comboyear,self.submitbutton,self.submitbuttonexcel]
                for x in list:
                    x.destroy()

            if (self.datekey== 1 or self.allkey==1):
                    self.listbox.destroy()
                    self.datekey=0
                    self.allkey=0
            if(self.flag2!=1):
                self.flag2=1
                self.roll = Label(self.bottominner2, text="     Enter Roll No   ", width=25, font=("bold", 10), bg="#bbdd56")
                self.roll.grid(row=6, column=0, padx=5, pady=10)
                self.rollentry = Entry(self.bottominner2, width=44)
                self.rollentry.grid(row=6, column=1,padx=5, pady=10, ipady=3)
                self.submitbutton2 = Button(self.bottominner2, text='Submit', width=30, bg='green', fg='white',
                                           font=("bold", 10), command=self.submit_data2)
                self.submitbutton2.grid(row=10, column=0, columnspan=2, padx=10, pady=10)



        if (getvalue == "Date"):
            if(self.flag2==1):
                self.roll.destroy()
                self.submitbutton2.destroy()
                self.rollentry.destroy()

            if (self.fetchkey == 1 or self.allkey == 1):
                self.listbox.destroy()
                self.fetchkey = 0
                self.allkey=0

            if(self.flag2!=2):
                self.flag2=2
                self.date = Label(self.bottominner2, text="Select Date   ", font=("bold", 10), bg="#bbdd56")
                self.date.grid(row=6, column=0)

                #day
                self.combodate = Combobox(self.bottominner2, width=3)
                items1 = ('01','02','03','04','05','06','07','08','09',10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
                self.combodate['values'] = items1
                self.combodate.current(0)
                self.combodate.grid(row=6, column=1)

                #Month
                self.combomonth = Combobox(self.bottominner2, width=3)
                items2 = ('01','02','03','04','05','06','07','08','09','10','11','12')
                self.combomonth['values'] = items2
                self.combomonth.current(0)
                self.combomonth.grid(row=6, column=2)


                # year
                self.comboyear = Combobox(self.bottominner2, width=6)
                items3 = (2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036,2037,2038,2039,2040)
                self.comboyear['values'] = items3
                self.comboyear.current(10)
                self.comboyear.grid(row=6,column=3)


                list1=[str(self.combodate.get()),str(self.combomonth.get()),str(self.comboyear.get())]
                y='-'.join(list1)
                print(y)

                self.submitbutton = Button(self.bottominner2, text='Submit', width=30, bg='green', fg='white',
                                           font=("bold", 10), command=self.submit_data1)
                self.submitbutton.grid(row=10,column=1, columnspan=3, padx=10, pady=10)
                #excelsheet generator button
                self.submitbuttonexcel = Button(self.bottominner2, text='Generate Excel Sheet', width=30, bg='red', fg='white',
                                           font=("bold", 10), command=self.submit_dataexcel)
                self.submitbuttonexcel.grid(row=12, column=1, columnspan=3, padx=10, pady=10)

        print(getvalue)

    def submit_data1(self):
         list1 = [str(self.comboyear.get()), str(self.combomonth.get()),str(self.combodate.get()) ]
         y = '-'.join(list1)
         self.fetchByDate(y)

    def submit_dataexcel(self):
         listexcel = [str(self.comboyear.get()), str(self.combomonth.get()),str(self.combodate.get()) ]
         y = '-'.join(listexcel)
         self.fetchByDateexcel(y)



    def submit_data2(self):
        print(self.rollentry.get().upper())
        self.fetchByRoll()
