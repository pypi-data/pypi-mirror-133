

import tkinter
import os
from PIL import ImageTk, Image as im
from tkinter import *




class Prompt(object):
    global box
    box = Tk()
    box.geometry('444x120')
    box.iconbitmap(os.getcwd().replace("\\", "/") + "/icon.ico")
    
   

    
    def select():
        
        box.destroy()
        
        
        

    

    def prompt(title='...', warning='Is this OK?', okButtonText = "OK", imagePath = "warning.png"):
        box.title(title)

        expl = Label(box, text=warning)
        
        global sel
        sel = Button(box, text=okButtonText, command=Prompt.select)
        
        
        global image
        image = ImageTk.PhotoImage(im.open(imagePath))

        global imgContainer
        imgContainer = Label(box, image = image)

        imgContainer.grid(column=0,row=0)
            
        
        sel.grid(column=5, row=1)
        
        expl.grid(pady=4,padx=4, row=0,column=5)
        
        
        
        
        
        
        box.mainloop()
        
    

