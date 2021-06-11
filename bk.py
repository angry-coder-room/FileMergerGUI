from tkinter import *
import os
import re
import win32api
from tkinter import scrolledtext
from tkinter import ttk
import asyncio
from threading import *
from tkinter import filedialog
from docx import Document
from PyPDF2 import PdfFileMerger

class FileMerger:
    def __init__(self, root):
        self.root = root
        self.root.title("File Merger")
        self.win_width = '800'
        self.win_height = '720'
        self.root.geometry(self.win_width + 'x' + self.win_height)

        self.top_frame = Frame(self.root)
        self.top_frame.pack()

        self.is_terminate = self.reset_terminate()
        self.lbl = Label(self.top_frame, text="Find", font=('Calibri', 13))
        self.lbl.pack(side = LEFT)
        self.search_file = Entry(self.top_frame, width=25, font=('Calibri', 13))
        self.search_file.pack(side = LEFT)
        self.btn = Button(self.top_frame, text="SEARCH", command=self.clicked, font=('Calibri'))
        self.btn.pack(side = LEFT)
        self.btn_terminate = Button(self.top_frame, text="TERMINATE", command=self.set_is_terminate, font=('Calibri'))
        self.btn_terminate.pack(side = LEFT)

        self.log_frame = Frame(self.root)
        self.log_frame.pack()
        self.search_logs = scrolledtext.ScrolledText(self.log_frame, width=self.win_width, height=20, font=('Calibri', 9))
        self.search_logs.pack(side = LEFT)

        self.table_frame = Frame(self.root)
        self.table_frame.pack()
        self.treev = ttk.Treeview(self.table_frame, height=15)
        self.treev.pack(side = LEFT)

        self.tree_scroll_bar = ttk.Scrollbar(self.table_frame, orient ="vertical", command = self.treev.yview)
        self.tree_scroll_bar.pack(side = RIGHT, fill ='x')
        self.treev.configure(xscrollcommand = self.tree_scroll_bar.set)

        self.treev['show'] = 'headings'
        self.treev["columns"] = ("1", "2")
        self.treev.column("1", width = 200, anchor ='c')
        self.treev.column("2", width = 580, anchor ='w')
        self.treev.heading("1", text ="File")
        self.treev.heading("2", text ="Location")
        
        self.dest_frame = Frame(self.root)
        self.dest_frame.pack(side = LEFT)
        self.btn_merge = Button(self.dest_frame, text="Choose Destination", command=self.choose_destination, font=('Calibri'))
        self.btn_merge.pack(side = LEFT)
        self.dest_text = StringVar()
        self.dest_text.set("(not selected)")
        self.dest_lbl = Label(self.dest_frame, textvariable=self.dest_text)
        self.dest_lbl.pack(side = LEFT)

        self.merger_type = IntVar()
        self.radio_pdf = Radiobutton(self.root, text="Pdf", variable=self.merger_type, value=3)
        self.radio_pdf.pack(side = RIGHT)
        self.radio_docx = Radiobutton(self.root, text="Docx", variable=self.merger_type, value=2)
        self.radio_docx.pack(side = RIGHT)
        self.radio_txt = Radiobutton(self.root, text="Text", variable=self.merger_type, value=1)
        self.radio_txt.pack(side = RIGHT)

        self.merge_frame = Frame(self.root)
        self.merge_frame.pack(side = BOTTOM)
        self.btn_merge = Button(self.merge_frame, text="MERGE", command=self.merge, font=('Calibri'))
        self.btn_merge.pack()

    def choose_destination(self):
        self.root.filename = filedialog.askdirectory()
        self.dest_text.set(self.root.filename)

    def clear_forms(self):
        self.search_logs.delete('1.0', END)
        for i in self.treev.get_children():
            self.treev.delete(i)
    
    def reset_terminate(self):
        return False

    def merge(self):
        if self.merger_type.get() == 1:
            self.merge_text_file(self.get_selected_rows())
        if self.merger_type.get() == 2:
            self.merge_docx_file(self.get_selected_rows())
        if self.merger_type.get() == 3:
            self.merge_pdf_file(self.get_selected_rows())

    def merge_pdf_file(self, selected_files):
        destination_source = self.dest_lbl.cget("text") + "/Merged.pdf"
        merger = PdfFileMerger()
        for file in selected_files:
            self.add_log('Merging ' + file + ' ...\n')
            merger.append(file)
        merger.write(destination_source)
        merger.close()
        self.add_log('File has been saved successfully ...\n')
        self.add_log('Location ' + destination_source + ' \n')

    def merge_text_file(self, selected_files):
        destination_source = self.dest_lbl.cget("text") + "/Merged.txt"
        with open(destination_source, "w") as outfile:
            for file in selected_files:
                self.add_log('Merging ' + file + ' ...\n')
                with open(file) as infile:
                    outfile.write(infile.read())
        self.add_log('File has been saved successfully ...\n')
        self.add_log('Location ' + destination_source + ' \n')

    def merge_docx_file(self, selected_files):
        destination_source = self.dest_lbl.cget("text") + "/Merged.docx"
        merged_doc = Document()
        for file in selected_files:
            self.add_log('Merging ' + file + ' ...\n')
            sub_doc = Document(file)
            for element in sub_doc.element.body:
                merged_doc.element.body.append(element)
        merged_doc.save(destination_source)
        self.add_log('File has been saved successfully ...\n')
        self.add_log('Location ' + destination_source + ' \n')

    def get_selected_rows(self):
        return [self.treev.item(items)['values'][1] for items in self.treev.selection()]    

    def add_log(self, message):
        self.search_logs.insert(INSERT, message)
        self.search_logs.see("end")

    def clicked(self):
        t1=Thread(target=self.start_search)
        t1.start()

    def start_search(self):
        self.clear_forms()
        # self.find_file_in_all_drives(self.search_file.get())
        search_text = self.search_file.get()
        dir_list = self.get_drive()
        for drive in dir_list:
            return self.find_file(drive, search_text)
    
    def get_drive(self):
        #only windows
        return win32api.GetLogicalDriveStrings().split('\000')[:-1]

    def find_file_in_all_drives(self, search_text):
        dir_list = self.get_drive()
        for drive in dir_list:
            return self.find_file(drive, search_text)

    def find_file(self, root_folder, search_text):
        for _root,dirs,files in os.walk(root_folder):
            for f in files:
                if not self.is_terminate:
                    self.add_log(os.path.join(_root, f)+ '\n')
                    if search_text in f:
                        self.treev.insert("", 'end', values =(f, os.path.join(_root, f)))
                else:
                    self.is_terminate = self.reset_terminate()
                    return
    
    def set_is_terminate(self):
        self.is_terminate = True

root = Tk()
gui = FileMerger(root)
root.mainloop()