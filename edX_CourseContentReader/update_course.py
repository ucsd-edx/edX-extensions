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
            sys.exit('\033[91m ERROR: Please make sure the README.md file has the right format.\n [Section] should starts with "*"\n [Subsection] should starts with "\\t*"\n [Unit] should starts with "\\t\\t*"\n [Problem] should starts with "\\t\\t\\t*"\033[0m')
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
            sys.exit("\033[91m ERROR: Course structure can only be either a dictionary or a list of tuples.\033[0m")
    
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
        sys.exit("\033[91m ERROR: Input course structure need to be a tuple.\033[0m") 
    
     
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
        for pro in from_struct:
            if pro not in new_struct:
                #print('removing problem', pro)
                remove_files(top_file, pro, new_dir)
    elif isinstance(from_struct, dict) and isinstance(new_struct, dict):
        for k in from_struct:
            from_s = from_struct[k][1]
            if k in new_struct:
                new_s = new_struct[k][1]
                check_remove(from_s, new_s, new_dir, from_struct[k][0])
            else:
                remove_files(top_file, from_struct[k], new_dir)
    else:
        sys.exit('\033[91m ERROR: Input structures need to be both of type dictionary or both of type list.\033[0m')

    


# In[17]:
def find_top_file(file_obj, new_dir):
    """
    Find parent file and previous link of file_obj from new_dir.
    Input:
        [file_obj]: A tuple of file name and a dictionary or a tuple of file name and problem type. The file object that we want to find.
        [new_dir]: the name of the course directory where we want to find the file object.
    Output:
        The top file to add link to the file object and a link id which we will insert the file object link after.
    """
    new_file = read_file(new_dir+'_description.md')
    print new_dir+'_description.md'
    new_course_file = new_file[0].split('[')[1].split(']')[0]
    new_struct, _ = parse_level(0, new_file[1:], 0)

    prev_id = ""
    top_file = ""
    if file_obj[0].startswith('sequential'):
        for chap_key in new_struct.keys():
            for sec_key in new_struct[chap_key][1].keys():
                if file_obj == new_struct[chap_key][1][sec_key]:
                    top_file = new_struct[chap_key][0]
                    prev_id = prev_id.split('/')[-1].replace('.xml', '')
                    return top_file, prev_id
                else:
                    prev_id = new_struct[chap_key][1][sec_key][0]
    elif file_obj[0].startswith('vertical'):
        for chap_key in new_struct.keys():
            for sec_key in new_struct[chap_key][1].keys():
                for subsec_key in new_struct[chap_key][1][sec_key][1].keys():
                    if file_obj == new_struct[chap_key][1][sec_key][1][subsec_key]:
                        top_file = new_struct[chap_key][1][sec_key][0]
                        prev_id = prev_id.split('/')[-1].replace('.xml', '')
                        return top_file, prev_id
                    else:
                        prev_id = new_struct[chap_key][1][sec_key][1][subsec_key][0]
    elif isinstance(file_obj[1], str):
        for chap_key in new_struct.keys():
            for sec_key in new_struct[chap_key][1].keys():
                for subsec_key in new_struct[chap_key][1][sec_key][1].keys():
                    for pro_tuple in new_struct[chap_key][1][sec_key][1][subsec_key][1]:
                        if file_obj == pro_tuple:
                            top_file = new_struct[chap_key][1][sec_key][1][subsec_key][0]
                            prev_id = prev_id.split('/')[-1].replace('.xml', '')
                            return top_file, prev_id
                        else:
                            prev_id = pro_tuple[0]


def add_files_recursively(file_obj, from_dir, to_dir, ori_dir):
    """
    Add files based on the passed in dictionary of the course structure.
    Input:
        [file_obj]: a dictionary describing sections, subsections, and units, or a list describing problems.
        [from_dir]: the course directory that we want to copy files from.
        [to_dir]: the course directory that we want to copy files to.
        [ori_dir]: the course directory which is the base of the new directory.
    """
    if os.path.isfile(to_dir+'/'+file_obj[0]):
        # adding duplicate files
        print("\033[91m ERROR: Adding files with duplicate file ID {}".format(to_dir+'/'+file_obj[0]))
        sys.exit("Please make sure to add files that are not already in the course.\033[0m")
    elif not os.path.isfile(from_dir+'/'+file_obj[0]):
        # adding files not from from_dir
        # check to see whether this file is in ori_dir
        if os.path.isfile(ori_dir+'/'+file_obj[0]):
            print('found in ori')
            print file_obj
            ## find top file
            top_file, prev_id = find_top_file(file_obj, to_dir)
            add_files(top_file, file_obj, ori_dir, to_dir, ori_dir, prev_id)
    else:
        shutil.copyfile(from_dir+'/'+file_obj[0], to_dir+'/'+file_obj[0])
        if isinstance(file_obj[1], list):
            for fi, fi_type in file_obj[1]:
                shutil.copyfile(from_dir+'/'+fi, to_dir+'/'+fi)
        elif isinstance(file_obj[1], dict):
            for v in file_obj[1].values():
                add_files_recursively(v, from_dir, to_dir, ori_dir)
        else:
            if not isinstance(file_obj[1], str):
                sys.exit("\033[91m ERROR: Course structure can only be either a dictionary or a list of tuples.\033[0m")
    

def add_files(to_top_file, new_obj, from_dir, to_dir, ori_dir, pre_link):
    """
    Edit top file by adding the link to new files.
    Copy all files in the in the new_obj from from_dir to to_dir.
    Input:
        [to_top_file]: parent file of the course structure where we can copy new link into.
        [new_obj]: a tuple of file name and dictionary/list indicating files to be added.
        [from_dir]: the course directory that we want to copy files from.
        [to_dir]: the course directory that we want to copy files to.
        [ori_dir]: the course directory which is the base of the new directory.
        [pre_link]: Previous link in the top_file. When adding new link in top_file, we will add it right after pre_link. It's an indication of where to add the new link in the top_file.
    """
    if isinstance(new_obj, tuple):

        ### Copy files
        add_files_recursively(new_obj, from_dir, to_dir, ori_dir)
        
        ### Edit top file
        top_to_lines = open(to_dir+'/'+to_top_file, 'r').readlines()
        add_link = new_obj[0].split('/')[-1].replace('.xml', '')
        
        # add new line to file
        new_f_lines = []
        allow_tag = ['chapter', 'sequential', 'vertical', 'video', 'html', 'problem']
        for l in top_to_lines:
            tag = l.split()[0].replace('<', '')
            if 'url_name' in l and tag in allow_tag:
                current_url = l.split('url_name="')[1].split('"')[0]
                if pre_link == '':
                    new_line = l.replace(current_url, add_link)
                    if isinstance(new_obj[1], str):
                        new_line = new_line.replace(tag, new_obj[1])
                    new_f_lines.append(new_line)
                    new_f_lines.append(l)
                    pre_link = 'added'
                elif current_url == pre_link:
                    new_f_lines.append(l)
                    new_line = l.replace(current_url, add_link)
                    if isinstance(new_obj[1], str):
                        new_line = new_line.replace(tag, new_obj[1])
                    new_f_lines.append(new_line)
                    pre_link = 'added'
                else:
                    new_f_lines.append(l)
            else:
                new_f_lines.append(l)
        open(to_dir+'/'+to_top_file, 'w').writelines(new_f_lines)
        
    else:
        sys.exit("\033[91m ERROR: Input course structure should be a tuple.\033[0m")
        
    
    
def check_new(new_struct, to_struct, from_dir, to_dir, ori_dir, to_top_file):
    """
    Recursively check to see whether there are files that needed to be added.
    Input:
        [new_struct]: a dictionary or list that represent the new course structure.
        [to_struct]: a dictionary or list that represent the old course structure where we want to add files to.
        [from_dir]: directory where we want to copy files from.
        [to_dir]: directory where we want to copy files to.
        [ori_dir]: directory which is the base of the new directory.
        [to_top_file]: parent file of the course structure where we can copy new link into.

    """

    if isinstance(new_struct, list) and isinstance(to_struct, list):
        pre_pro = ''
        pro_count = 0
        for pro in new_struct:
            if pro in to_struct:
                if pro != to_struct[pro_count]:
                    sys.exit('\033[91m ERROR: new unit {} is already in list, can\'t add duplicate unit or new unit with duplicate name. Skipping.'.format(pro))
                else:
                    pro_count += 1
            else: #pro not in to_struct:
                #print('adding problem:', pro)
                add_files(to_top_file, pro, from_dir, to_dir, ori_dir, pre_pro)
            pre_pro = pro[0].split('/')[-1].split('.xml')[0]
    elif isinstance(new_struct, dict) and isinstance(to_struct, dict):
        pre_key = ''
        key_count = 0
        for k in new_struct:
            new_s = new_struct[k][1]
            if k in to_struct.keys():                    
                if k != to_struct.keys()[key_count]:
                    sys.exit('\033[91m ERROR: section {} is already in course, but in the wrong order Please check to see whether you are adding a section that already exist.\033[0m'.format(k))
                else:
                    key_count += 1
                to_s = to_struct[k][1]
                check_new(new_s, to_s, from_dir, to_dir, ori_dir, to_struct[k][0])
            else:
                #print('adding course structure', new_struct[k])
                add_files(to_top_file, new_struct[k], from_dir, to_dir, ori_dir, pre_key)
            pre_key = new_struct[k][0].split('/')[-1].split('.xml')[0]
    else:
        sys.exit('\033[91m ERROR: Input structures need to be both of type dictionary or both of type list.\033[0m')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("\033[91m Please pass in the name of the original course folder and the name of the incoming course folder.\033[0m")
    else:
        orig_course_name = sys.argv[1]
        incoming_course_name = sys.argv[2]

    orig_course_folder = orig_course_name
    incoming_course_folder =incoming_course_name
    new_course_folder = 'new_' + orig_course_folder

    print('Generating the new course by copying {} to {} ...'.format(orig_course_folder, new_course_folder))
    if os.path.isdir(new_course_folder):
        sys.exit("\033[91m ERROR: {} already exists, please remove it and rerun.\033[0m".format(new_course_folder))
    shutil.copytree(orig_course_folder, new_course_folder)


    ### Read in struct
    orig_file = read_file(orig_course_folder+'_description.md')
    # check file unchanged
    check_orig_file = read_file(orig_course_folder+'/README.md')
    if orig_file != check_orig_file:
        sys.exit("\033[91m ERROR: {0}_description.md is changed. Please only edit the {1}_description.md file. Rerun pre_update.py to regenerate {0}_description.md.\033[0m".format(orig_course_folder, new_course_folder))
    orig_course_file = orig_file[0].split('[')[1].split(']')[0]
    orig_struct, _ = parse_level(0, orig_file[1:], 0)

    incoming_file = read_file(incoming_course_folder+'_description.md')
    # check file unchanged
    check_incoming_file = read_file(incoming_course_folder+'/README.md')
    if incoming_file != check_incoming_file:
        sys.exit("\033[91m ERROR: {0}_description.md is changed. Please only edit the {1}_description.md file. Rerun pre_update.py to regenerate {0}_description.md.\033[0m".format(incoming_course_folder, new_course_folder))
    incoming_course_file = incoming_file[0].split('[')[1].split(']')[0]

    new_file = read_file(new_course_folder+'_description.md')
    new_course_file = new_file[0].split('[')[1].split(']')[0]
    new_struct, _ = parse_level(0, new_file[1:], 0)

    print("Checking unwanted files ...")
    check_remove(orig_struct, new_struct, new_course_folder, new_course_file)

    print("Rendering new README.md file in {} ...".format(new_course_folder))
    cmd = 'makeDoc.py {}'.format(new_course_folder)
    os.system(cmd)
    orig_file = read_file(new_course_folder+'/README.md')
    orig_struct, _ = parse_level(0, orig_file[1:], 0)

    print("Checking new files ...")
    check_new(new_struct, orig_struct, incoming_course_folder, new_course_folder, orig_course_folder, new_course_file)

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
        sys.exit("\033[91m ERROR: The new course doesn't match the {}. Double check your description files to make sure that the format is correct and rerun.\033[0m".format(new_course_folder+'_description.md'))


