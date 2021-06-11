from tkinter import *
import os
import re
import win32api
from tkinter import scrolledtext
import asyncio
import threading

window = Tk()
window.title("File Merger")
window.geometry('600x700')


def clicked():
    # res = "Searching " + search_file.get() + "..."
    # status_text.configure(text= res)
    find_file_in_all_drives(search_file.get())


def find_file(root_folder, file_name):
    for root,dirs,files in os.walk(root_folder):
        for f in files:
            # search_logs.insert(INSERT, os.path.join(root, f)+ '\n')
            if file_name == f:
                print(os.path.join(root, f))
                return

def find_file_in_all_drives(file_name):
    dir_list = win32api.GetLogicalDriveStrings().split('\000')[:-1]
    for drive in dir_list:
        return find_file(drive, file_name)

Label(window, text='\n').grid(column=0, row=0)          #Empty row

lbl = Label(window, text="Find", font=('Calibri', 14))
lbl.grid(column=0, row=2, padx=5)

search_file = Entry(window,width=25, font=('Calibri', 15))
search_file.grid(column=1, row=2, padx=5)

btn = Button(window, text="SEARCH", command=clicked, font=('Calibri', 11, "bold"))
btn.grid(column=2, row=2, padx=5)

Label(window, text='\n').grid(column=0, row=3)          #Empty row

lst = [('',1,'Raj'),
       ('',2,'Aaryan'),
       ('',3,'Vaishnavi'),
       ('',4,'Rachna'),
       ('',5,'Shubham')]
   
total_rows = len(lst)
total_columns = len(lst[0])

for i in range(total_rows):
    for j in range(total_columns):
        e = Entry(window, width=25, font=('Calibri', 12))
        e.grid(row=i+4, column=j)
        e.insert(END, lst[i][j])

window.mainloop()