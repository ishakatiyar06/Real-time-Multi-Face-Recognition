from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import csv
from tkinter import filedialog

mydata=[]
class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance System")

        #===================variables======================
        self.var_atten_id = StringVar()
        self.var_atten_roll= StringVar()
        self.var_atten_name = StringVar()
        self.var_atten_dep = StringVar()
        self.var_atten_time = StringVar()
        self.var_atten_date=StringVar()
        self.var_atten_attendance = StringVar()

        img1 = Image.open(r"project_images\label_left.jpg")
        img1 = img1.resize((650, 200))
        self.photoimg1 = ImageTk.PhotoImage(img1)
        label1 = Label(self.root, image=self.photoimg1)
        label1.place(x=0, y=0, width=650, height=200)  # Place it at the top-left

        # Load and place the second image
        img2 = Image.open(r"project_images\atten_bg.jpeg")
        img2 = img2.resize((700, 200))
        self.photoimg2 = ImageTk.PhotoImage(img2)
        label2 = Label(self.root, image=self.photoimg2)
        label2.place(x=650, y=0, width=700, height=200)

        title_label = Label(self.root, text="ATTENDANCE DETAILS", 
                            font=("Times New Roman", 30, "bold"), bg="blue", fg="white")
        title_label.place(x=0, y=200, width=1530, height=40)

        main_frame = Frame(self.root, bd=2, bg="black")
        main_frame.place(x=0, y=240, width=1494, height=600)

        #left label frame
        Left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Student Attendance Details",
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=5, width=610, height=580)

        left_inside_frame = Frame(Left_frame, bd=2,relief=RIDGE)
        left_inside_frame.place(x=0, y=5, width=605, height=270)

        #labels and entry
        # Studnet Id.
        attendance_id = Label(left_inside_frame, text='Attendance Id', font=("times new roman", 12, "bold"))
        attendance_id.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        attendance_id_entry = ttk.Entry(left_inside_frame,textvariable =self.var_atten_id, width=18, font=("times new roman", 13))
        attendance_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # University Roll No.
        student_roll = Label(left_inside_frame, text='Roll No.', font=("times new roman", 12, "bold"))
        student_roll.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        student_roll_entry = ttk.Entry(left_inside_frame,textvariable=self.var_atten_roll, width=20, font=("times new roman", 13))
        student_roll_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        # Student Name
        student_name = Label(left_inside_frame, text='Student Name', font=("times new roman", 12, "bold"))
        student_name.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        student_name_entry = ttk.Entry(left_inside_frame,textvariable=self.var_atten_name ,width=18, font=("times new roman", 13))  # Adjusted width
        student_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        #department
        dep = Label(left_inside_frame, text='Department', font=("times new roman", 12, "bold"))
        dep.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        depEntry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_dep,width=18, font=("times new roman", 13))  # Adjusted width
        depEntry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        #time
        timeLabel = Label(left_inside_frame, text='Time: ', font=("times new roman", 12, "bold"))
        timeLabel.grid(row=4, column=0, padx=5, pady=5, sticky=W)
        attnTime = ttk.Entry(left_inside_frame,textvariable=self.var_atten_time,width=18, font=("times new roman", 13))  # Adjusted width
        attnTime.grid(row=4, column=1, padx=5, pady=5, sticky=W)
        
        #date
        dateLabel = Label(left_inside_frame, text='Date: ', font=("times new roman", 12, "bold"))
        dateLabel.grid(row=5, column=0, padx=5, pady=5, sticky=W)
        attnDate = ttk.Entry(left_inside_frame,textvariable=self.var_atten_date, width=18, font=("times new roman", 13))  # Adjusted width
        attnDate.grid(row=5, column=1, padx=5, pady=5, sticky=W)

        #attendance
        attenLabel = Label(left_inside_frame, text='Attendance ', font=("times new roman", 12, "bold"))
        attenLabel.grid(row=6, column=0, padx=5, pady=5, sticky=W)


        atten_combo = ttk.Combobox(left_inside_frame,textvariable=self.var_atten_attendance,font=("times new roman", 12),state="readonly",width=17)
        atten_combo["values"]= ("Status","Present","Absent" )
        atten_combo.current(0)
        atten_combo.grid(row=6,column=1,padx=2,pady=10)

        #buttons frame
        bt_frame=Frame(Left_frame,bd=2,relief=RIDGE,bg="beige")
        bt_frame.place(x=0,y=300,width=600,height=39)


        save_btn=Button(bt_frame,text="Show Attendance",command=self.importCsv,width=16,font=("times new roman",12,"bold"),bg="beige",fg="dark green")
        save_btn.grid(row=0,column=0,sticky=W)

        update_btn=Button(bt_frame,text="Export CSV",command = self.exportCsv,width=16,font=("times new roman",12,"bold"),bg="beige",fg="dark green")
        update_btn.grid(row=0,column=1,sticky=W)

        del_btn=Button(bt_frame,text="UPDATE",width=16,font=("times new roman",12,"bold"),bg="beige",fg="dark green")
        del_btn.grid(row=0,column=2,sticky=W)

        reset_btn=Button(bt_frame,command=self.reset_data,text="RESET",width=15,font=("times new roman",12,"bold"),bg="beige",fg="dark green")
        reset_btn.grid(row=0,column=3,sticky=W)







        # Right label frame
        Right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE,text="Attendance Details",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=640, y=5, width=610, height=580)

        table_frame = Frame(Right_frame,bd=2,bg="white", relief=RIDGE)
        table_frame.place(x=5,y=5,width=595,height=358)

        #==========scroll bar and table=========
        scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.AttendanceReportTable=ttk.Treeview(table_frame,columns=("Id","Roll No.","Name","Department","Time","Date","Attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("Id",text="Attendance Id")
        self.AttendanceReportTable.heading("Roll No.",text="Roll")
        self.AttendanceReportTable.heading("Name",text="Name")
        self.AttendanceReportTable.heading("Department",text="Department")
        self.AttendanceReportTable.heading("Time",text="Time")
        self.AttendanceReportTable.heading("Date",text="Date")
        self.AttendanceReportTable.heading("Attendance",text="Attendance")

        self.AttendanceReportTable["show"]="headings"
        self.AttendanceReportTable.column("Id",width=100)
        self.AttendanceReportTable.column("Roll No.",width=100)
        self.AttendanceReportTable.column("Name",width=100)
        self.AttendanceReportTable.column("Department",width=100)
        self.AttendanceReportTable.column("Time",width=100)
        self.AttendanceReportTable.column("Date",width=100)
        self.AttendanceReportTable.column("Attendance",width=100)
        self.AttendanceReportTable.pack(fill=BOTH,expand=1)

        self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)
    #====================fetch data==============

    def fetchData(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("",END,values=i)

    def importCsv(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")],parent=self.root)
        with open(fln) as myfile:
            csvread = csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)    

#==================export csv==========================

    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No data","No data found to export",parent= self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")],parent=self.root)
            with open(fln,mode="w",newline="") as myfile:
                exp_write= csv.writer(myfile,delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Data Export","Your data exported to "+os.path.basename(fln)+" successfully")    
        except Exception as es:
            messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)     
    #===============================get cdata=========
    def get_cursor(self,event=""):
        cursor_row=self.AttendanceReportTable.focus()
        content= self.AttendanceReportTable.item(cursor_row)
        rows=content['values']
        self.var_atten_id.set(rows[0])           
        self.var_atten_name.set(rows[1])           
        self.var_atten_roll.set(rows[2])                      
        self.var_atten_dep.set(rows[3])           
        self.var_atten_time.set(rows[4])           
        self.var_atten_date.set(rows[5])           
        self.var_atten_attendance.set(rows[6])           

    def reset_data(self):
        self.var_atten_id.set("")           
        self.var_atten_name.set("")           
        self.var_atten_roll.set("")                      
        self.var_atten_dep.set("")           
        self.var_atten_time.set("")           
        self.var_atten_date.set("")           
        self.var_atten_attendance.set("")


if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()        