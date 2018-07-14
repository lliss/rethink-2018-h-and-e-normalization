# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 13:49:01 2018

@author: LaurenceLiss
 
Creates a simple GUI for summing two numbers.
"""
 
import tkinter
from tkinter import ttk, Canvas, PhotoImage
from math import sin
 
class Demo(ttk.Frame):
    test = ''
    
    """The adders gui and functions."""
    def __init__(self, parent, image_map=None, color_map=None,  *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()
        self.test = 'Hello'
 
    def on_quit(self):
        """Exits program."""
        quit()
 
    def calculate(self):
        """Calculates the sum of the two inputted numbers."""
        num1 = int(self.num1_entry.get())
        num2 = int(self.num2_entry.get())
        num3 = num1 + num2
        self.answer_label['text'] = num3
 
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
 

        #self.img = 
        WIDTH, HEIGHT = 100, 100

        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, bg="#0000ff")
        self.canvas.grid(column=0, row=0)
        self.img = PhotoImage(width=WIDTH, height=HEIGHT)
        self.canvas.create_image((int(WIDTH/2), int(HEIGHT/2)), image=self.img, state="normal")

        data = ("{red}")
        #self.img.put(data, to=(0,640, 0,480))
        #self.img.put(data, to=(0, 0, int(WIDTH), int(HEIGHT)))
        
        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.img.put("#00ff00", (x, y, x+1, y+1))                     
        '''
        WIDTH, HEIGHT = 640, 480

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

for x in range(4 * WIDTH):
    y = int(HEIGHT/2 + HEIGHT/4 * sin(x/80.0))
    img.put("#ffffff", (x//4,y))
        '''
    
        #self.num1_entry = ttk.Entry(self, width=5)
        #self.num1_entry.grid(column=1, row = 2)
 
        #self.num2_entry = ttk.Entry(self, width=5)
        #self.num2_entry.grid(column=3, row=2)
 
        #self.calc_button = ttk.Button(self, text='Calculate',
        #        command=self.calculate)
        #self.calc_button.grid(column=0, row=3, columnspan=4)
 
        #self.answer_frame = ttk.LabelFrame(self, text='Answer',
        #        height=100)
        #self.answer_frame.grid(column=0, row=4, columnspan=4, sticky='nesw')
 
        #self.answer_label = ttk.Label(self.answer_frame, text='')
        #self.answer_label.grid(column=0, row=0)
 
        # Labels that remain constant throughout execution.
        #ttk.Label(self, text='Number Adder').grid(column=0, row=1,
        #        columnspan=4)
        #ttk.Label(self, text='Number one').grid(column=0, row=2,
        #        sticky='w')
        #ttk.Label(self, text='Number two').grid(column=2, row=2,
        #        sticky='w')
 
        #ttk.Separator(self, orient='horizontal').grid(column=0,
        #        row=1, columnspan=4, sticky='ew')
 
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
 
if __name__ == '__main__':
    root = tkinter.Tk()
    Demo(root)
    root.mainloop()