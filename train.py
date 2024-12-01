from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance System")

        title_label = Label(self.root, text="Train Dataset", 
                            font=("Times New Roman", 30, "bold"), bg="white", fg="green")
        title_label.place(relx=0.5, y=0, width=1530, height=80, anchor="n")

        b1_title = Button(self.root,command=self.train_classifier, text="Train Data",cursor="hand2" ,font=("Arial", 12, "bold"), bg="blue", fg="white")
        b1_title.place(x=0, y=340, width=1350, height=40)

    def train_classifier(self):
        data_dir = ("data") 
        path =[os.path.join(data_dir,file) for file in os.listdir(data_dir)]   
        faces=[]
        ids=[]

        for image in path:
            img = Image.open(image).convert('L')
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])
            print(f"Processing image: {image} with ID: {id}")  # Debugging line
            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("training", imageNp)
            cv2.waitKey(1) == 13


        ids = np.array(ids,dtype=np.int32)    
        #train the classiifer========================
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows() 
        messagebox.showinfo("Result","Training datasets completed")



if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()
