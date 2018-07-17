# -*- coding: utf-8 -*-

"""
Created on Fri Jul 13 13:49:01 2018

@author: LaurenceLiss

Creates a simple GUI for summing two numbers.
"""

import tkinter
from tkinter import ttk, Canvas, PhotoImage, OptionMenu, W

class Demo(ttk.Frame):

    selection = {}
    test = 'Hello'


    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.geometry('1000x1000')
        self.init_gui()


    def on_quit(self):
        """Exits program."""
        self.root.destroy()


    def done(self):
        """Complete the selection and close the GUI."""
        self.root.destroy()


    def dropdown(self):
        master = self.root
        variable = tkinter.StringVar(self.root)
        variable.set("White")
        option = OptionMenu(master, variable, "White", "Nuclei", "Stroma", "Cytyoplasm", "No Response")
        return option


    def saveSelection(self, val):
        if val != None:
            print(val)


    def makeform(self,fields):
       for i in range(len(fields)):
          tkinter.Frame(self.root)
          selected = tkinter.StringVar()
          self.square(fields[i]).grid(row=i, column=1, sticky=W, padx=5, pady=5)
          self.dropdown().grid(row=i, column=2, sticky=W, padx=5, pady=5)
          tkinter.Label(self.root, text='View').grid(row=i, column=3, sticky=W, padx=5, pady=5)
          yes = tkinter.Radiobutton(self.root, text='Yes', variable=selected, value="Yes", command=self.saveSelection(selected.get()))
          yes.grid(row=i, column=3, sticky=W, padx=5, pady=5)
          no = tkinter.Radiobutton(self.root, text='No', variable=selected, value="No", command=self.saveSelection(selected.get()))
          no.grid(row=i, column=5, sticky=W, padx=5, pady=5)


    def square(self, color):
        canvas = tkinter.Canvas(self.root)
        canvas.config(width=20, height=20)
        canvas.create_rectangle(0, 0, 20, 20, outline = color, fill=color)#, width=20)
        return canvas


    def drawImage(self):
        WIDTH, HEIGHT = 640, 480

        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, bg="#ffffff")
        self.canvas.grid(column=0, row=0)
        self.img = PhotoImage(width=WIDTH, height=HEIGHT)
        self.canvas.create_image((int(WIDTH/2), int(HEIGHT/2)), image=self.img, state="normal")
        
        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.img.put("#00ff00", (x, y, x+1, y+1))        
                             

    def init_gui(self):
        """Builds GUI."""
        self.root.title('Color Assignment')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='nsew')
        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='Exit', command=self.on_quit)
        self.menu_edit = tkinter.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menubar.add_cascade(menu=self.menu_edit, label='Edit')
        self.root.config(menu=self.menubar)
        
        self.done_button = ttk.Button(self, text='Done',
                                      command=self.done)
        self.done_button.grid(column=0, row=3, columnspan=4)


        self.drawImage()
        self.makeform(["#fb0","#cb0","#fc0","#ab0", "#ff0000"])

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


if __name__ == '__main__':
    root = tkinter.Tk()
    Demo(root)
    root.mainloop()