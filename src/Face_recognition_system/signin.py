from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
import cv2

def capture():
    path = "D:\Final Year Project(final)\src\Face_recognition_system\known_faces"
    name = inputtxt.get(1.0, "end-1c")
    if(len(name) == 0):
        return
    print(name)
    _, frame = cap.read()
    cv2.imwrite(filename=f"{path}\{name}.jpg", img=frame)
    cv2.destroyAllWindows()
    root.destroy()

cap = cv2.VideoCapture(0)

root = Tk()
root['background']='#856ff8'
# Create a frame
app = Frame(root, bg="white")

app.grid()
# Create a label in the frame
lmain = Label(app)
lmain.grid()

# Capture from camera

width = int(cap.get(3))
height = int(cap.get(4)) + 150
# print(width)
s1 = f"{width}x{height}"
root.geometry(s1)   

button_font = font.Font(family='Helvitica', size=10)

user_name = Label(root,text = "Enter First Name", font=button_font)
user_name.grid(row = 1, column = 0, pady = 2)
inputtxt = Text(root,height = 1,width = 20, font=button_font)
inputtxt.grid(pady = 2)


button_font = font.Font(family='Helvitica', size=20)


printButton = Button(root,text="Capture",bg='#45b592',fg='#ffffff',bd=0,font=button_font,height=1,width=15, command = capture, pady = 1)
printButton.grid()



def video_stream():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream) 

def login():
    video_stream()
    root.mainloop()

# login()

