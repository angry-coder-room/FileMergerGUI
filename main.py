import os
import re
import win32api

def find_file(root_folder, file_name):
    for root,dirs,files in os.walk(root_folder):
        for f in files:
            # result = rex.search(f)
            # print(os.path.join(root, f))
            print(f)
            if file_name == f:
                print(os.path.join(root, f))
                return

def find_file_in_all_drives(file_name):
    #create a regular expression for the file
    # rex = re.compile(file_name)
    dir_list = win32api.GetLogicalDriveStrings().split('\000')[:-1]
    for drive in dir_list:
        return find_file(drive, file_name)


find_file_in_all_drives('foo.txt')