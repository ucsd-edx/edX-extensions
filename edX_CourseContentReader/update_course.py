#!/usr/bin/env python
# coding: utf-8

# In[1]:


import shutil
import os, sys
from pathlib import Path
from collections import OrderedDict


# In[2]:


def parse_level(level, lines, i):
    """
    Parse README.md file to a dictionary of course structure recursively.
    Input:
        [level]: the level of the course structure range from 0 to 2. Level 0 stands for section level, 1 stands for subsection, 2 stands for unit level
        [lines]: a list of lines read from the README.md file. Ideally the output from file.read().splitlines()
        [i]: current line number to indicate how far we have parsed the file
    Output:
        [dic]: a course structure dictionary parsed from README.md
        [i]: current line number to indicate how far we have parsed the file
    """
    dic = OrderedDict()
    while i < len(lines):
        l = lines[i]
        if not l.startswith('\t'*level):
            return dic, i
        elif level < 2:
            l = lines[i]
            k = l.split(']')[1].split('- [')[0]
            k = k.replace('\\(Draft\\) ', 'draft_')
            k = k.strip()
            v = l.split('](')[1].split(')')[0]
            sub_dic, i = parse_level(level+1, lines, i+1)
            ### use problem title and last 5 digits of file id as the key
            dic['('+v[-9:-4]+')'+k] = (v, sub_dic)
        elif level == 2:
            l = lines[i]
            k = l.split(']')[1].split('- [')[0]
            k = k.replace('\\(Draft\\) ', '(draft)')
            k = k.strip()
            v = l.split('](')[1].split(')')[0]
            pro_list, i = parse_pros(lines, i+1)
            ### use problem title and last 5 digits of file id as the key
            dic['('+v[-9:-4]+')'+k] = (v, pro_list)
        else:
            sys.exit('ERROR: Please make sure the README.md file has the right format.\n [Section] should starts with "*"\n [Subsection] should starts with "\\t*"\n [Unit] should starts with "\\t\\t*"\n [Problem] should starts with "\\t\\t\\t*"')
    return dic, i


def parse_pros(lines, i):
    """
    Parse problem level README.md.
    Input:
        [lines]: a list of lines read from the README.md file. Ideally the output from file.read().splitlines()
        [i]: current line number to indicate how far we have parsed the file
    Output:
        [pros]: a list of problems parsed from the README.md
        [i]: current line number to indicate how far we have parsed the file
    """
    pros = []
    while i < len(lines):
        l = lines[i]
        if not l.startswith('\t'*3):
            return pros, i
        elif l.strip()[0] != '*':
            i += 1
            continue
        else:
            k = l.split('[')[1].split(']')[0]
            v = l.split('](')[1][:-1]
            if v.startswith('draft'):
                k = '(draft)'+k
            pros.append((v,k))
            i += 1
    return pros, i

def read_file(filename):
    """
    Read the README.md file and removed the first line.
    Input:
        [filename]: name of the file
    Output:
        [description_file]: a list of lines read from the input file
    """
    description_file = open(filename, 'r').read()
    description_file = description_file.splitlines()
    description_file[0] = description_file[0].replace('###','')
    description_file = [x for x in description_file if x]
    return description_file


# In[3]:


def remove_files_recursively(file_obj, from_dir):
    """
    Remove files based on the passed in dictionary of the course structure.
    Input:
        [file_obj]: a dictionary describing sections, subsections, and units, or a list describing problems.
        [from_dir]: the course directory that we want to remove files from.
    """
    os.remove(from_dir+'/'+file_obj[0])

    if isinstance(file_obj[1], list):
        for fi, fi_type in file_obj[1]:
            os.remove(from_dir+'/'+fi)
    elif isinstance(file_obj[1], dict):
        for v in file_obj[1].values():
            remove_files_recursively(v, from_dir)
    else:
        if not isinstance(file_obj[1], str):
            sys.exit("ERROR: Course structure can only be either a dictionary or a list of tuples.")
    
def remove_files(top_file, remove_obj, from_dir):
    """
    Edit top file by removing the old link.
    Remove all files in the course structure that is passed in.
    Input:
        [top_file]: parent file of the course structure. Remove the link to the old files.
        [remove_obj]: a tuple of file name and dictionary/list indicating files to be removed.
        [from_dir]: the course directory that we want to remove files from.
    """
    if isinstance(remove_obj, tuple):
        ### remove files
        remove_files_recursively(remove_obj, from_dir)
        
        ## draft subsection doesn't link from top_file
        ## only when it is not draft subsection, edit top_file link
        if not remove_obj[0].startswith('drafts/vertical'):
            ### Edit top file
            top_f_lines = open(from_dir+'/'+top_file, 'r').readlines()
            remove_link = remove_obj[0].split('/')[-1].replace('.xml', '')
            new_f_lines = []
            for l in top_f_lines:
                if 'url_name' in l:
                    current_url = l.split('url_name="')[1].split('"')[0]
                    if current_url != remove_link:
                        new_f_lines.append(l)
                else:
                    new_f_lines.append(l)
            open(from_dir+'/'+top_file, 'w').writelines(new_f_lines) 
    else:
        sys.exit("ERROR: Input course structure need to be a tuple.") 
    
     
def check_remove(from_struct, new_struct, new_dir, top_file):
    """
    Recursively check to see whether there are files that needed to be removed.
    Input:
        [from_struct]: a dictionary or list that represent the course structure which we want to remove files from
        [new_struct]: a dictionary or list that represent the new course structure
        [new_dir]: the new directory where we want to remove files from
        [top_file]: parent file of the from_struct. Remove the link pointing to the old files.
    """
    if isinstance(from_struct, list) and isinstance(new_struct, list):
        key_count = 0
        for pro in from_struct:
            if pro not in new_struct:
                #print('removing problem', pro)
                remove_files(top_file, pro, new_dir)
            key_count += 1
    elif isinstance(from_struct, dict) and isinstance(new_struct, dict):
        key_count = 0
        for k in from_struct:
            from_s = from_struct[k][1]
            if k in new_struct:
                new_s = new_struct[k][1]
                check_remove(from_s, new_s, new_dir, from_struct[k][0])
                key_count += 1
            else:
                #print('removing course structure', from_struct[k])
                remove_files(top_file, from_struct[k], new_dir)
    else:
        sys.exit('ERROR: Input structures need to be both of type dictionary or both of type list.')

    


# In[17]:


def add_files_recursively(file_obj, from_dir, to_dir):
    """
    Add files based on the passed in dictionary of the course structure.
    Input:
        [file_obj]: a dictionary describing sections, subsections, and units, or a list describing problems.
        [from_dir]: the course directory that we want to copy files from.
        [to_dir]: the course directory that we want to copy files to.
    """

    shutil.copyfile(from_dir+'/'+file_obj[0], to_dir+'/'+file_obj[0])
    
    if isinstance(file_obj[1], list):
        for fi, fi_type in file_obj[1]:
            shutil.copyfile(from_dir+'/'+fi, to_dir+'/'+fi)
    elif isinstance(file_obj[1], dict):
        for v in file_obj[1].values():
            add_files_recursively(v, from_dir, to_dir)
    else:
        if not isinstance(file_obj[1], str):
            sys.exit("ERROR: Course structure can only be either a dictionary or a list of tuples.")
    

def add_files(from_top_file, to_top_file, new_obj, from_dir, to_dir, pre_link):
    """
    Edit top file by adding the link to new files.
    Copy all files in the in the new_obj from from_dir to to_dir.
    Input:
        [from_top_file]: parent file of the course structure where we can find the link to copy over.
        [to_top_file]: parent file of the course structure where we can copy new link into.
        [new_obj]: a tuple of file name and dictionary/list indicating files to be added.
        [from_dir]: the course directory that we want to copy files from.
        [to_dir]: the course directory that we want to copy files to.
        [pre_link]: Previous link in the top_file. When adding new link in top_file, we will add it right after pre_link. It's an indication of where to add the new link in the top_file.
    """
    if isinstance(new_obj, tuple):

        ### Copy files
        add_files_recursively(new_obj, from_dir, to_dir)
        
        ### Edit top file
        top_from_lines = open(from_dir+'/'+from_top_file, 'r').readlines()
        top_to_lines = open(to_dir+'/'+to_top_file, 'r').readlines()
        add_link = new_obj[0].split('/')[-1].replace('.xml', '')
        
        # find the line to add
        new_line=''
        for l in top_from_lines:
            if 'url_name' in l:
                current_url = l.split('url_name="')[1].split('"')[0]
                if current_url == add_link:
                    new_line = l
                    break
        if not new_line:
            sys.exit("ERROR: can't find new link of {0} from file {1}".format(add_link, from_dir+'/'+top_file))
        
        # add new line to file
        new_f_lines = []
        for l in top_to_lines:
            if 'url_name' in l:
                current_url = l.split('url_name="')[1].split('"')[0]
                if pre_link == '':
                    new_f_lines.append(new_line)
                    new_f_lines.append(l)
                    pre_link = 'go to else now'
                elif current_url == pre_link:
                    new_f_lines.append(l)
                    new_f_lines.append(new_line)
                    pre_link = 'go to else now'
                else:
                    new_f_lines.append(l)
            else:
                new_f_lines.append(l)
        open(to_dir+'/'+to_top_file, 'w').writelines(new_f_lines)
        
    else:
        sys.exit("ERROR: Input course structure should be a tuple.")
        
    
    
def check_new(new_struct, to_struct, from_dir, to_dir, from_top_file, to_top_file):
    """
    Recursively check to see whether there are files that needed to be added.
    Input:
        [new_struct]: a dictionary or list that represent the new course structure.
        [to_struct]: a dictionary or list that represent the old course structure which we want to add files to.
        [from_dir]: directory where we want to copy files from.
        [to_dir]: directory where we want to copy files to.
        [from_top_file]: parent file of the course structure where we can find the link to copy over.
        [to_top_file]: parent file of the course structure where we can copy new link into.

    """

    if isinstance(new_struct, list) and isinstance(to_struct, list):
        pre_pro = ''
        pro_count = 0
        for pro in new_struct:
            if pro in to_struct:
                if pro != to_struct[pro_count]:
                    print('new unit {} is already in list, can\'t add duplicate unit or new unit with duplicate name. Skipping.'.format(pro))
            else: #pro not in to_struct:
                #print('adding problem:', pro)
                add_files(from_top_file, to_top_file, pro, from_dir, to_dir, pre_pro)
            pre_pro = pro[0].split('/')[-1].split('.xml')[0]
            pro_count += 1
    elif isinstance(new_struct, dict) and isinstance(to_struct, dict):
        pre_key = ''
        key_count = 0
        for k in new_struct:
            from_s = new_struct[k][1]
            if k in to_struct.keys():
                if k != to_struct.keys()[key_count]:
                    print('new section {} is already in course, can\'t add duplicate section or new section with duplicate name. Skipping.'.format(k))
                to_s = to_struct[k][1]
                check_new(from_s, to_s, from_dir, to_dir, new_struct[k][0], to_struct[k][0])
            else:
                #print('adding course structure', new_struct[k])
                add_files(from_top_file, to_top_file, new_struct[k], from_dir, to_dir, pre_key)
            pre_key = new_struct[k][0].split('/')[-1].split('.xml')[0]
            key_count += 1
    else:
        sys.exit('ERROR: Input structures need to be both of type dictionary or both of type list.')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Please pass in the name of the original course folder and the name of the incoming course folder.")
    else:
        orig_course_name = sys.argv[1]
        incoming_course_name = sys.argv[2]

    orig_course_folder = orig_course_name
    incoming_course_folder =incoming_course_name
    new_course_folder = 'new_' + orig_course_folder

    print('Generating the new course by copying {} to {} ...'.format(orig_course_folder, new_course_folder))
    if os.path.isdir(new_course_folder):
        sys.exit("{} already exists, please remove it and rerun.".format(new_course_folder))
    shutil.copytree(orig_course_folder, new_course_folder)


    ### Read in struct
    orig_file = read_file(orig_course_folder+'_description.md')
    orig_course_file = orig_file[0].split('[')[1].split(']')[0]
    orig_struct, _ = parse_level(0, orig_file[1:], 0)

    incoming_file = read_file(incoming_course_folder+'_description.md')
    incoming_course_file = incoming_file[0].split('[')[1].split(']')[0]

    new_file = read_file(new_course_folder+'_description.md')
    new_course_file = new_file[0].split('[')[1].split(']')[0]
    new_struct, _ = parse_level(0, new_file[1:], 0)

    print("Checking unwanted files ...")
    check_remove(orig_struct, new_struct, new_course_folder, new_course_file)

    print("Checking new files ...")
    check_new(new_struct, orig_struct, incoming_course_folder, new_course_folder, incoming_course_file, new_course_file)

    print("Rendering new README.md file in {} ...".format(new_course_folder))
    cmd = 'makeDoc.py {}'.format(new_course_folder)
    os.system(cmd)

    print("Check whether new README.md matches the {} ...".format(new_course_folder+'_description.md'))
    ### Check readme.md
    new_readme = read_file('{}/README.md'.format(new_course_folder))
    old_readme = new_file
    check_pass = (new_readme == old_readme)

    if check_pass:
        cmd = "tar czf {0}.tar.gz {0}".format(new_course_folder)
        print(cmd)
        os.system(cmd)
        print("Success!")
    else:
        sys.exit("ERROR: The new course doesn't match the {}. Double check your description files to make sure that the format is correct and rerun".format(new_file))


