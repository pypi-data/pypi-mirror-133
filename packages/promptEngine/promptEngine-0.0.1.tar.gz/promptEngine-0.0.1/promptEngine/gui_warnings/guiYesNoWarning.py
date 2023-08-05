

import tkinter
import os

from tkinter import *




class Prompt(object):
    global box
    box = Tk()
    box.geometry('444x244')
    box.iconbitmap(os.getcwd().replace("\\", "/") + "/icon.ico")
    
    global sel
    sel = Listbox(box, width=444)
    
    

    
    def select():
        global chosen
        chosen = sel.get(ANCHOR)
        global result
        result = None
        if chosen == "YES":
            result = True
        elif chosen == "NO":
            result = False
        box.destroy()
        
        
        

    selectButton = Button(box, text="Select", command=select, background="blue", foreground="white")

    def prompt(title='Select...', warning='Select an item...'):
        box.title(title)

        expl = Label(box, text=warning)
        expl.pack(pady=4,padx=4)

        sel.pack(pady=4)
        
        for item in ["YES", "NO"]:
            sel.insert(END, item)
            
        
        Prompt.selectButton.pack()
        
        
        
        
        
        chosen = sel.curselection()

        
        box.mainloop()
        
    

