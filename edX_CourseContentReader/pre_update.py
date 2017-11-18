#!/usr/bin/env python

"""
    Generates README.md in both folders
    Extracts new README.md files to working directory
    Makes a duplicate course structure based on the [orig_course_name]
    Input:
        [orig_course_name]: folder name of the base course.
        [incoming_course_name]: folder name of the incoming course.
"""


import shutil
import os, sys
from pathlib import Path
from collections import OrderedDict


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("\033[91m ERROR: Please pass in the name of the original course folder and the name of the incoming course folder.\033[0m")
    else:
        orig_course_name = sys.argv[1]
        incoming_course_name = sys.argv[2]

    for folder_name in [orig_course_name,incoming_course_name]:
        if not os.path.isfile(folder_name+'.tar.gz'):
            sys.exit("\033[91m ERROR: {} not found.\033[0m".format(folder_name+'.tar.gz'))
        if os.path.isdir(folder_name):
            sys.exit('\033[91m ERROR: {} already exists, remove it and rerun.\033[0m'.format(folder_name))
        print('unzipping %s ...'%folder_name)
        cmd = 'tar xzf %s.tar.gz'%folder_name
        print cmd; os.system(cmd)
        cmd = 'makeDoc.py {}'.format(folder_name)
        os.system(cmd)

    ### Prepare struct
    orig_course_folder = orig_course_name
    incoming_course_folder =incoming_course_name
    new_course_folder = 'new_' + orig_course_folder

    print('Generating description files ...')
    shutil.copy(orig_course_folder+'/README.md', orig_course_folder+'_description.md')
    shutil.copy(incoming_course_folder+'/README.md', incoming_course_folder+'_description.md')
    shutil.copy(orig_course_folder+'/README.md', new_course_folder+'_description.md')
    print("Success!")
    
    print("Please edit {}_description.md file and then run update_course.py {} {}".format(new_course_folder, orig_course_name, incoming_course_name))

