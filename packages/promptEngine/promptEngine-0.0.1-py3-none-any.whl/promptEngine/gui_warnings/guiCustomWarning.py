import tkinter
from tkinter import *
from PIL import ImageTk, Image as im
import os

class Prompt(object):

    def selectButton1():
        global chosen
        chosen = button1txt
        box.quit()

    def selectButton2():
        global chosen
        chosen = button2txt
        box.quit()

    def prompt(button1Text = "YES", button2Text = "NO", windowTitle = "Select...", explain = "This or that???", iconPath = os.getcwd().replace("\\", "/") + "/icon.ico", picturePath = "warning.png"):
        
        global box

        box = Tk()
        box.title(windowTitle)
        box.iconbitmap(iconPath)
        box.geometry("544x140")

        global button1
        global button2

        global button1txt
        global button2txt

        button2txt = button2Text
        button1txt = button1Text

        button1 = Button(box, text = button1Text, command=Prompt.selectButton1)
        button2 = Button(box, text = button2Text, command=Prompt.selectButton2)

        image = ImageTk.PhotoImage(im.open(picturePath))
        imageContainer = Label(box, image = image)

        explainLbl = Label(box, text=explain)

        imageContainer.grid(row=0, column=0)
        button1.grid(row=1, column=2)
        button2.grid(row=1, column=3)
        explainLbl.grid(row=0, column=2)

        box.mainloop()

