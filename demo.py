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
    view_radios = []
    view_radio_selections = []
    selected_colors = []
    test = 'Hello'
    WIDTH = 640
    HEIGHT = 480


    def __init__(self, parent, image_map=None, color_map=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.image_map = image_map
        self.color_map = [self.rgb_to_hex(rgb_row) for rgb_row in color_map]
        print(color_map)
        self.root.geometry('1000x1000')
        self.init_gui()


    def rgb_to_hex(self, rgb):
        hex_string = [self.get_hex_string(value) for value in rgb]
        return '#' + ''.join(hex_string)
    
    
    def get_hex_string(self, number):
        return str(hex(int(number))).replace('0x', '')


    def on_quit(self):
        """Exits program."""
        self.root.destroy()


    def done(self):
        """Complete the selection and close the GUI."""
        self.root.destroy()


    def dropdown(self):
        variable = tkinter.StringVar(self.root)
        self.selected_colors.append(variable)
        variable.set("White")
        option = OptionMenu(self.redFrame, variable, "White", "Nuclei", "Stroma", "Cytyoplasm", "No Response", command=self.updateStructureSelection)
        return option


    def updateStructureSelection(self, parent):
        for selection in self.selected_colors:
            choice = selection.get()
            print(choice)


    def updateViewSelection(self):
        for index, selection in enumerate(self.view_radio_selections):
            for x in range(self.WIDTH):
                for y in range(self.HEIGHT):
                    val = self.image_map[y][x]
                    if val == index and selection.get() == 1:                            
                        color = '#00ff00'
                        self.img.put(color, (x, y, x+1, y+1))
                    elif val == index:
                        color = self.color_map[val]
                        self.img.put(color, (x, y, x+1, y+1))
                    


    def makeform(self, fields):
       for i in range(len(fields)):
          selected = tkinter.IntVar()
          selected.set(0)
          self.view_radio_selections.append(selected)
          self.square(fields[i]).grid(row=i, column=0, sticky=W, padx=5, pady=5)
          self.dropdown().grid(row=i, column=1, sticky=W, padx=5, pady=5)
          tkinter.Label(self.redFrame, text='View').grid(row=i, column=2, sticky=W, padx=5, pady=5)
          yes = tkinter.Radiobutton(self.redFrame, text='Yes', variable=selected, value=1, command=self.updateViewSelection)
          yes.grid(row=i, column=3, sticky=W, padx=5, pady=5)
          no = tkinter.Radiobutton(self.redFrame, text='No', variable=selected, value=0, command=self.updateViewSelection)
          no.grid(row=i, column=4, sticky=W, padx=5, pady=5)
          self.view_radios.append(yes)
          self.view_radios.append(no)
          


    def square(self, color):
        canvas = tkinter.Canvas(self.redFrame)
        canvas.config(width=20, height=20)
        canvas.create_rectangle(0, 0, 20, 20, outline = color, fill=color)#, width=20)
        return canvas


    def drawImage(self):
        self.canvas = Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg="#ffffff")
        self.canvas.grid(column=0, row=0, rowspan=10, padx=5, pady=5)
        self.img = PhotoImage(width=self.WIDTH, height=self.HEIGHT)
        self.canvas.create_image((int(self.WIDTH/2), int(self.HEIGHT/2)), image=self.img, state="normal")
        
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                val = self.image_map[y][x]
                color = self.color_map[val]
                self.img.put(color, (x, y, x+1, y+1))        
                             
            
    def updateImage(self, selected):
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                val = self.image_map[y][x]
                color = self.color_map[val]
                self.img.put(color, (x, y, x+1, y+1))
        
            
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
        self.done_button.grid(column=0, row=1, columnspan=2)


        self.drawImage()
        self.redFrame = tkinter.Frame(self.root, pady=5, bg="red", width=500, height=500)
        self.redFrame.grid(column=1, row=0)
        self.makeform(self.color_map)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


if __name__ == '__main__':
    root = tkinter.Tk()
    Demo(root)
    root.mainloop()