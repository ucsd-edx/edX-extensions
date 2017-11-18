# Code for taking two directoris: orig_dir and incoming_dir, and a list describing 
# a new organization, and creating a new_dir that conforms to the list.
# %cd /Users/yoavfreund/academic.papers/Courses/undergrad statistics/CSE103.2017/edXUnitExchange
import re
from shutil import copytree, rmtree, copyfile
from os import mkdir, chdir,rename,remove,getcwd,system
from os.path import isdir,isfile
from pathlib import Path
from glob import glob
from sys import stdout
import argparse

orig='CSE103.10.11'
incoming='DSE210.10.11'

for DIR in [orig,incoming]:
    print DIR
    if isdir(DIR):
        print 'removing',DIR
        rmtree(DIR)
    cmd='tar xzf %s.tar.gz'%DIR
    print cmd; system(cmd)
    rename('course',DIR)
    cmd='python edX_CourseContentReader/edX_Tree.py --dir %s > %s.txt'%(DIR,DIR)
    print cmd; system(cmd)

orig_name='CSE103.10.11.txt'
orig_list=open(orig_name,'r').readlines()
updated_name='CSE103.new.txt'
updated_list=open(updated_name,'r').readlines()
incoming_name='DSE210.10.11.txt'
incoming_list=open(incoming_name,'r').readlines()

pat=re.compile(r'([\d\.]*).*\((\S+)\)')
def split_line(line):
    m=pat.search(line)
    if m:
        index,fname=m.groups()
        path=fname.split('/')
        return index,fname,path,path[-1][:-4]
    else:
        return None


orig_course_xml=re.search(r'\((\S+)\)',orig_list[0]).groups()[0]
orig_course=open(orig_course_xml,'r').readlines()

orig_dir=orig_course_xml.split('/')[0]
new_dir = orig_dir+'.new'

incoming_course_xml=re.search(r'\((\S+)\)',incoming_list[0]).groups()[0]
incoming_course=open(incoming_course_xml,'r').readlines()
incoming_dir=incoming_course_xml.split('/')[0]

if isdir(new_dir):
    rmtree(new_dir)
    print 'removed directory',new_dir
copytree(orig_dir,new_dir)
print 'copied',orig_dir,'to',new_dir
print 'orig_dir=',orig_dir,'incoming_dir=',incoming_dir,'new_dir=',new_dir

orig_tree=edX_tree(orig_dir)
incoming_tree=edX_tree(incoming_dir)

new_tree=edX_tree(new_dir)

from string import strip

for i in range(1,len(updated_list)):
    orig_index,orig_fname,_,_=split_line(orig_list[i])
    print 'updated_list=',updated_list[i]
    if len(strip(updated_list[i]))==0:
        continue
    updated_index,updated_fname,_,_=split_line(updated_list[i])
    if orig_fname != updated_fname:
        print orig_list[i],updated_list[i]
        if orig_index != updated_index:
            print 'Mismatch of indexes:"%s" != "%s"'%(orig_index,updated_index)
            break
        # remove old files.
        removal_list=new_tree.list_xml_files(new_tree.T['list'][i-1])
        print 'length of removal list=',len(removal_list)
        for f in removal_list:
            fn=new_dir+'/'+f
            if isfile(fn):
                #print 'removing',fn
                remove(fn)
        # insert new files.
        
        insertion_list=incoming_tree.list_xml_files(incoming_tree.T['list'][i-1])
    
        print 'length of insertion list=',len(insertion_list)
        for f in insertion_list:
            f_from=incoming_dir+'/'+f
            f_to=new_dir+'/'+f
            if 1==0:
                print 'cp %s, %r \n  to %s, %r'%(f_from,isfile(f_from),f_to,isfile(f_to)),
            copyfile(f_from,f_to)
            if 1==0:
                print isfile(f_to)
        # add line to new course.xml
        if orig_course[i] !=incoming_course[i]:
            print 'orig:',orig_course[i]
            print 'incoming:',incoming_course[i]
            

for path in glob(incoming_dir+'/html/*'):
    f=path.split('/')[-1]
    copyfile(path,new_dir+'/html/'+f)
              
#!ls
print new_dir
new_tree=None
new_tree=edX_tree(new_dir)
new_tree.printout(new_tree.T['list'][2]['list'][4],depth=5)