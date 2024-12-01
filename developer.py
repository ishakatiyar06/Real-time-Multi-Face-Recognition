from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from student import Student
import os
from train import Train
from face_recognition import FaceRecognition
from attendance import Attendance

class Developer:
    def __init__(self,root):
        self.root =root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance System")

        # Load and display background image
        img1 = Image.open(r"project_images/developer.jpeg")
        img1 = img1.resize((600, 400), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(relx=0.5, y=100, anchor="n")

        # Title label
        title_label = Label(self.root, text="DEVELOPER", font=("Times New Roman", 30, "bold"), bg="white", fg="red")
        title_label.place(relx=0.5, y=0, width=1530, height=80, anchor="n")

if __name__ =="__main__":
    root =Tk()
    obj=Developer(root)
    root.mainloop()