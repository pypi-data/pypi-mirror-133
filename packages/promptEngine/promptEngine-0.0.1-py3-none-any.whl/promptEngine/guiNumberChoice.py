

import tkinter
import os

from tkinter import *




class Prompt(object):
    global box
    box = Tk()
    box.geometry('444x244')
    box.iconbitmap(os.getcwd().replace("\\", "/") + "/base-promptable/promptable/icon.ico")
    global notice
    notice = Label(text="Please type numbers ONLY!!!", fg="red", foreground="red")
    global sel
    sel = Entry(box, width=444)
    
    

    
    def select():
        global chosen
        try:
           chosen = int(sel.get())
           box.destroy()
        except ValueError:
            sel.config(background="red", foreground="white")
            notice.pack()
        
        
        
        

    selectButton = Button(box, text="Select", command=select, background="blue", foreground="white")

    def prompt(title='Select...', explanation='Type a number...'):
        box.title(title)
        global expl
        expl = Label(box, text=explanation)
        expl.pack(pady=4,padx=4)

        sel.pack(pady=4)
        
         
        
        Prompt.selectButton.pack()
        
        
        
        
        
        chosen = sel.get()

        
        box.mainloop()

