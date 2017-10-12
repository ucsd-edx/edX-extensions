#!/usr/bin/env python

import re
from shutil import copytree, rmtree, copyfile
from os import mkdir, chdir,rename,remove,getcwd,system
from os.path import isdir,isfile
from pathlib import Path
from glob import glob
from sys import stdout
import argparse

class edX_tree:
    """ Class for manipulating edX tree 
    """
    def expand(self,filename):
        """List the xml paths that are the children of a given xml file path
           Input: name of xml file
           output: A struct:
                   filename: the name of the file analyzed
                   name: display_name in edx
                   meta: lines that were not recornized
                   list:  a list of filenames of child xml files
        """
        link_pat = re.compile('<(\w+)\s+url_name="(\S+)"/>')
        meta_pat=re.compile(r'<(\w+)\s.*display_name="([^"]+)"')
        discussion_pat=re.compile(r'')

        with open(filename,'r') as file:
            i=0
            L=[]
            meta=[]
            _type=''
            _name='noname'
            first_line=file.readline()
            meta_m=meta_pat.search(first_line)
            if meta_m:
                _name=meta_m.group(2)
                _type=meta_m.group(1)
            else:
                #print 'No Match first line. file=%s, line=%s'%(filename,first_line)
                return None
            for line in file.readlines():
                i+=1
                link_m=link_pat.search(line)
                meta_m=meta_pat.search(line)
                if meta_m:
                    #_name=meta_m.group(2)
                    #_type=meta_m.group(1)
                    #if _type=='discussion':
                    meta.append(line)
                elif link_m:
                    L.append('%s/%s.xml'%(link_m.group(1),link_m.group(2)))
                else:
                    #print 'No Match line %d file=%s, line=%s'%(i,filename,first_line)
                    if _type!='':
                        if '</'+_type+'>' in line:
                            continue
                        meta.append(line)

        answer={'name':_name,'type':_type,'meta':meta,'filename':filename}
        if len(L)>0:
            answer['list']=L
        return answer

    def expand_all(self,filename):
        """List the xml paths that are the children of a given xml file path
           Input: name of xml file
           output: A dictionary:
                   filename: the name of the file analyzed
                   name: display_name in edx
                   meta: lines that were not recornized
                   list: a list of dictionaries corresponding (recursively) to child xml files 
        """
        D=self.expand(filename)
        #print filename,type(D)
        if type(D)==dict and 'list' in D:
            L=[]
            for f in D['list']:
                L.append(self.expand_all(f))
                D['list']=L    
        return D

    def list_problems(self,directory):
        pat1=re.compile(r'<problem ([^>]+)>')
        pat2 = re.compile(r'(\S+)="([^"]+)"')
        for filename in glob(directory+'/problem/*'):
            with open(filename,'r') as file:
                for line in file.readlines():
                    m=pat1.match(line)
                    if m:
                        print filename,
                        params=m.group(1)
                        #print params
                        m2=pat2.findall(params)
                        Dict= {key:val for key,val in m2 if key!='markdown'}
                        print Dict

    
    def __init__(self,dirname):
        root=getcwd()
        chdir(dirname)
        self.dir=dirname
        self.T=self.expand_all('course/course.xml')
        chdir(root)
    
    def printout(self,S,prefix='',depth=1, outfile='', out=None):
        """ print out the tree up to a given depth (default=1)
        """
        if out ==None:
            if outfile=='':
                out=stdout
            else:
                out=open(outfile,'w')
            
        if type(S) != dict:
            return
        out.write('%s%s:%s:(%s/%s)\n'%(prefix,S['type'],S['name'],self.dir,S['filename']))

        if depth>0 and 'list' in S:
                i=1
                for e in S['list']:
                    self.printout(e,prefix=prefix+'%d.'%i,depth=depth-1,out=out)
                    i+=1
        if outfile!='':
            out.close()
        return

    def switch_in(self,old,new):
        """ move chapters from between two courses
            old: a chapters dump file: will be used as the basis.
            new: a chapters dump file: lists the chapters to be switched in
        """
        return
    
    def list_xml_files(self,S):
        if type(S)==dict:
            L=[S['filename']]
            if 'list' in S:
                for e in S['list']:
                    L += self.list_xml_files(e)
            return L
        else:
            return []

    def split_chapters(self,T):
        chdir(self.dir)
        mkdir('chapters')
        chdir('chapters')

        dirs=[]
        for l in T['list']:
            dirs.append(l['name'][:30])
            mkdir(dirs[-1])


        for i in range(len(T['list'])):
            print dirs[i]
            xml_files=all_xml_files(T['list'][i])
            for f in xml_files:
                path=f.split('/')
                if not Path(dirs[i]+'/'+path[0]).is_dir():
                    mkdir(dirs[i]+'/'+path[0])
                try:
                    rename('../'+f,dirs[i]+'/'+f)
                except:
                    print 'could not rename ../'+f

                
if __name__=='__main__':
    # Get command-line arguments
    parser = argparse.ArgumentParser(
        description='Manipulate edX dumps')
    parser.add_argument('--dir', '-d', default='.', type=str,
                        help='Root directory of edX dump')
    parser.add_argument('--depth', '-D', default=1, type=int,
                        help='number of levels in printout')
    parser.add_argument('--root', '-r', default='',type=str,
                        help='root node to print out. second section="2", third part of first section="1.3"')
    
    args = parser.parse_args()

    home = getcwd()
    tree=edX_tree(args.dir)

    if len(args.root)>0:
        node_path=[int(x)-1 for x in args.root.split('.')]
        print node_path
        D=tree.T
        for p in node_path:
            D=D['list'][p]
    else:
        D=tree.T

    tree.printout(D,depth=args.depth)