# -*- coding: utf-8 -*-

"""
@author: Laurence Liss

Creates a GUI for manual assignment of colors to hitological structures.
"""

import tkinter
from tkinter import ttk, Canvas, PhotoImage, OptionMenu, W

class ColorPicker(ttk.Frame):

    selection = {}
    view_radios = []
    view_radio_selections = []
    selected_colors = []
    selection_dictionary = {
        'lumen': [],
        'nuclei': [],
        'stroma': [],
        'cytoplasm': []
    }

    WIDTH = 640
    HEIGHT = 480


    def __init__(self, parent, image_map=None, color_map=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.image_map = image_map
        self.color_map = [self.rgb_to_hex(rgb_row) for rgb_row in color_map]
        self.root.geometry('1000x1000')
        self.init_gui()


    def rgb_to_hex(self, rgb):
        hex_string = [self.get_hex_string(value) for value in rgb]
        return '#' + ''.join(hex_string)


    def get_hex_string(self, number):
        return str(hex(int(number))).replace('0x', '')


    def on_quit(self):
        """Close the GUI."""
        self.root.destroy()


    def done(self):
        """Complete the selection and close the GUI."""
        self.root.destroy()


    def dropdown(self):
        variable = tkinter.StringVar(self.root)
        self.selected_colors.append(variable)
        variable.set('No Response')
        menu_options = (
            'White',
            'Nuclei',
            'Stroma',
            'Cytoplasm',
            'No Response'
        )
        option = OptionMenu(self.selectionFrame, variable, *menu_options, command=self.updateStructureSelection)
        return option


    def updateStructureSelection(self, parent):
        # Clear the previously set selections.
        self.selection_dictionary['lumen'] = []
        self.selection_dictionary['nuclei'] = []
        self.selection_dictionary['stroma'] = []
        self.selection_dictionary['cytoplasm'] = []

        for index, selection in enumerate(self.selected_colors):
            choice = selection.get()
            choice = choice.lower()
            if choice == 'white':
                choice = 'lumen'
            if choice != 'no response':
                self.selection_dictionary[choice].append(index)


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
          tkinter.Label(self.selectionFrame, text='View').grid(row=i, column=2, sticky=W, padx=5, pady=5)
          yes = tkinter.Radiobutton(self.selectionFrame, text='Yes', variable=selected, value=1, command=self.updateViewSelection)
          yes.grid(row=i, column=3, sticky=W, padx=5, pady=5)
          no = tkinter.Radiobutton(self.selectionFrame, text='No', variable=selected, value=0, command=self.updateViewSelection)
          no.grid(row=i, column=4, sticky=W, padx=5, pady=5)
          self.view_radios.append(yes)
          self.view_radios.append(no)


    def square(self, color):
        canvas = tkinter.Canvas(self.selectionFrame)
        canvas.config(width=20, height=20)
        canvas.create_rectangle(0, 0, 20, 20, outline = color, fill=color)#, width=20)
        return canvas


    def drawImage(self):
        self.canvas = Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg='#ffffff')
        self.canvas.grid(column=0, row=0, rowspan=10, padx=5, pady=5)
        self.img = PhotoImage(width=self.WIDTH, height=self.HEIGHT)
        self.canvas.create_image((int(self.WIDTH/2), int(self.HEIGHT/2)), image=self.img, state='normal')

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

        self.done_button = ttk.Button(self.root, text='Done',
                                      command=self.done)
        self.done_button.grid(column=0, row=1, columnspan=2)

        self.drawImage()
        self.selectionFrame = tkinter.Frame(self.root, pady=5, width=500, height=500)
        self.selectionFrame.grid(column=1, row=0)
        self.makeform(self.color_map)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


if __name__ == '__main__':
    root = tkinter.Tk()
    ColorPicker(root)
    root.mainloop()