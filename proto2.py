from tkinter import *
import os
import re
import win32api
from tkinter import scrolledtext
import asyncio
from threading import *

root = Tk()
root.title("File Merger")
root.geometry('600x700')

tool_frame = Frame(root)
tool_frame.pack()

def start_search():
    find_file_in_all_drives(search_file.get())

def find_file(root_folder, file_name):
    for root,dirs,files in os.walk(root_folder):
        for f in files:
            search_logs.insert(INSERT, os.path.join(root, f)+ '\n')
            search_logs.see("end")
            if file_name == f:
                show_table()
                return

def show_table():
    lst = [('x', 'Filename', 'C:/dsdf/dfdf/dffd/')]
    total_rows = len(lst)
    total_columns = len(lst[0])

    for i in range(total_rows):
        for j in range(total_columns):
            e = Entry(tableframe, width=25, font=('Calibri', 12))
            e.grid(row=i, column=j)
            e.insert(END, lst[i][j])

def find_file_in_all_drives(file_name):
    dir_list = win32api.GetLogicalDriveStrings().split('\000')[:-1]
    for drive in dir_list:
        return find_file(drive, file_name)


def clicked():
    t1=Thread(target=start_search)
    t1.start()

is_terminate = False

lbl = Label(tool_frame, text="Find", font=('Calibri', 13))
lbl.pack(side = LEFT)

search_file = Entry(tool_frame,width=25, font=('Calibri', 13))
search_file.pack(side = LEFT)

btn = Button(tool_frame, text="SEARCH", command=clicked, font=('Calibri'))
btn.pack(side = LEFT)

log_frame = Frame(root)
log_frame.pack()

Label(log_frame, text="Details", font=('Calibri', 11))
search_logs = scrolledtext.ScrolledText(log_frame,width=600,height=10, font=('Calibri', 9))
search_logs.pack(side = LEFT)

tableframe = Frame(root)
tableframe.pack()

# lst = []

# if len(lst) != 0:
#     total_rows = len(lst)
#     total_columns = len(lst[0])

#     for i in range(total_rows):
#         for j in range(total_columns):
#             e = Entry(tableframe, width=25, font=('Calibri', 12))
#             e.grid(row=i, column=j)
#             e.insert(END, lst[i][j])

root.mainloop()