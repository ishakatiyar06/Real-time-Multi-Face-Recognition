from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np
from time import strftime
from datetime import datetime

class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance System")
        
        # Load and display background image
        img1 = Image.open(r"background\blog-–-462-1.webp")
        img1 = img1.resize((600, 400), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(relx=0.5, y=100, anchor="n")

        # Button for face recognition
        button = Button(self.root, command=self.face_recog, text="Recognize Face", font=("Times New Roman", 20, "bold"), bg="green", fg="white")
        button.place(relx=0.5, y=520, width=200, height=50, anchor="n")

        # Title label
        title_label = Label(self.root, text="FACE RECOGNITION", font=("Times New Roman", 30, "bold"), bg="white", fg="red")
        title_label.place(relx=0.5, y=0, width=1530, height=80, anchor="n")

    # Attendance marking function
    def mark_attendance(self, s, r, n, d):
        with open("attendance.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            name_list = [line.split(",")[0] for line in myDataList]

            if s not in name_list:
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{s},{r},{n},{d},{d1},{dtString},Present")

    # Face recognition function
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            coord = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int(100 * (1 - predict / 300))

                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="mysql@isha",
                    database="face_recognition"
                )
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT Name, Roll, Dep, Student_id FROM student WHERE Roll=%s", (id,))
                result = my_cursor.fetchone()
                
                if result:
                    n, r, d, s = result
                    n, r, d, s = str(n), str(r), str(d), str(s)
                else:
                    n, r, d, s = "Unknown", "Unknown", "Unknown", "Unknown"

                if confidence > 77:
                    cv2.putText(img, f"Id :{s}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll :{r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name :{n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Dep :{d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.mark_attendance(s, r, n, d)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                coord = [x, y, w, h]
                conn.close()
            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        if faceCascade.empty():
            print("Error loading haarcascade_frontalface_default.xml")

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
        if clf.empty():
            print("Error loading classifier.xml")

        video_cap = cv2.VideoCapture(0)
        seconds_to_run = 5
        start_time = cv2.getTickCount()

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("Error capturing video")
                break

            img = recognize(img, clf, faceCascade)
            cv2.imshow("Face Recognition", img)

            elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
            if elapsed_time > seconds_to_run:
                break

            if cv2.waitKey(1) == 13:
                break

        video_cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognition(root)
    root.mainloop()
