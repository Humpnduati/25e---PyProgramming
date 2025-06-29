#!/usr/bin/env python3
# -*-coding:UTF-8 -*

from tkinter import *
from tkinter.ttk import Treeview

def frame_vertical_scrollbar(window:Tk, canvas:Canvas, frame):
    """It adds and returns a scroll bar to a frame included in a canvas of a windows"""
    vsb = Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(fill="y", side="right",)
    canvas.pack()
    canvas.create_window(500, 0, window=frame, anchor=CENTER)
    frame.bind("<Configure>", lambda event, canvas=canvas: on_frame_configure(canvas))
    return vsb

def input_window(window:Tk, parent, Str:str):
    """It prints a given string on a parent object of a window of a program and takes and returns as input the answer of the user"""
    text = Label(parent, text=Str)
    text.pack()
    input = StringVar()
    entry = Entry(parent, textvariable=input)
    entry.pack()
    next_button(window, parent)
    return input.get()

def leave_window(window:Tk, parent, text:str = 'Quitter'):
    """It produces in a parent object, a leave button for a window with a description text which by default is 'Quitter'"""
    leave = Button(parent, text=text, command=window.destroy)
    leave.pack()
    window.mainloop()

def next_button(window:Tk, parent, text:str = '⇩'):
    """It creates and puts on a parent object of a window of a program, a next button, with a description string which is by default ⇩"""
    next = Button(parent, text=text, command=window.quit)
    next.pack()
    window.mainloop()

def on_frame_configure(canvas):
    '''It resets the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def print_table_windows(parent, Heading, Datas):
    """It takes as input a 2-dimension table 'Datas' and prints its elts on a parent object of a windows of a program with the headings taken in 'Headings'"""
    Table = Treeview(parent, columns=Heading)
    for head in Heading:
        Table.heading(head, text=str(head))
    Table['show'] = 'headings' #useful not to have a tree display
    for Data in Datas:
        Table.insert('', 'end', iid=Data[0], values=Data)
    Table.pack()

def print_window(parent, Str:str):
    """It prints a given string on a parent objet of a window of a program"""
    text = Label(parent, text=Str)
    text.pack()

if __name__ == "__main__":
    import func
    print("'tkinter_kit' is a module full of functions and objects, varied and very practical in order to ease the use of the Tkinder module. Here are some detailed help:")      
    help(func)
    input("Glad to have served you! Press 'Enter' to quit.")