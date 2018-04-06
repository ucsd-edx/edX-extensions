#!/usr/bin/env python
from __future__ import print_function
from pathlib2 import Path
from collections import OrderedDict
import re
import json
import sys
import os
from anytree import Node, PreOrderIter
import xml.etree.ElementTree as ET
from shutil import copyfile, copytree, rmtree
import filecmp
import argparse
import tarfile


class DocDict:

    def __makeCourse(self):
        """
        Create a list of chapters by reading course.xml
        """
        course_file_list = list(self.course_path.iterdir())
        self.course_file = [x for x in course_file_list if x.suffix == '.xml'][0]
        course_txt = self.course_file.open().readlines()

        for cline in course_txt:
            if 'chapter' in cline:
                chap_name = cline.split('"')[1]
                self.chapter_list.append(chap_name)

    def __makeDraftStruct(self):
        """
        Create a problems to units mapping for drafts by reading files from folder vertical
        Draft problems are linked backward. When draft problems are published, it will then link from top down.
        Therefore, we need to construct the draft files ahead of time.
        """
        for v in self.draft_vert_path.iterdir():
            if v.suffix != '.xml':
                continue

            sec_xml = ET.parse(str(v)).getroot()
            sec_name = sec_xml.attrib['parent_url'].split('/')[-1].split('@')[-1]
            rank = sec_xml.attrib['index_in_children_list']

            comp_list = [int(rank), str(v)]

            for child in sec_xml:
                if child.tag in ['problem', 'video', 'html']:
                    prob = child.attrib['url_name']
                    comp_list.append([child.tag, prob])

            if sec_name not in self.draft_problems_struct.keys():
                self.draft_problems_struct[sec_name] = [comp_list]
            else:
                self.draft_problems_struct[sec_name].append(comp_list)

        for k in self.draft_problems_struct:
            sorted_struct = sorted(self.draft_problems_struct[k], key=lambda x: x[0])
            self.draft_problems_struct[k] = [s[1:] for s in sorted_struct]



    def __init__(self, start_path, duplicate=True, package=False):
        """
        Initialize the class by assigning values to path variables.
        Input:
            [start_path]: name of the course directory. The course need to be unzipped.
        """
        if not os.path.isdir(start_path):
            sys.exit("\033[91m ERROR: can't find directory {} \033[0m".format(start_path))

        ## Path variables
        self.path = Path(start_path)
        if not package:
            self.duplicate = duplicate
            self.course_path = self.path / 'course'
            self.chapter_path = self.path / 'chapter'
            self.seq_path = self.path / 'sequential'
            self.vert_path = self.path / 'vertical'

            self.draft_path = self.path / 'drafts'
            self.draft_vert_path = self.draft_path / 'vertical'
            self.draft_prob_path = self.draft_path / 'problem'


            ## List of all chapters
            self.chapter_list = []

            ## Structure of sections and units
            self.draft_problems_struct = OrderedDict()
            self.public_problems_struct = OrderedDict()
            self.all_problems_struct = OrderedDict()

            ## Make course struct
            self.__makeCourse()

            if self.draft_path.exists() and self.draft_vert_path.exists():
                self.__makeDraftStruct()


    def get_valid_filename(self,s):
        s = str(s.encode('ascii','ignore')).strip().replace(' ', '_').replace('_-_','_')
        return re.sub(r'(?u)[^-\w.]', '', s).lower()

    def createFolderStructure(self):

        folder_mapping = {}
        prefixes = []
        default_folders = ['/about', '/assets', '/course','/info','/policies','/static','/tabs']
        for node in PreOrderIter(self.course_tree):

            if node == self.course_tree.root:
                directory = os.path.dirname(node.name[1] + '/')
                for i in default_folders:
                    if os.path.exists(str(self.path) + i):
                        copytree(str(self.path) + i, directory + i)
                folder_mapping['root'] = str(self.path)
            else:
                directory = node.parent.name[1] + '/' + node.name[0]

            if node.name[0].endswith('.xml') or node.name[0].endswith('.html'):
                if os.path.exists(node.name[1]):
                    copyfile(node.name[1], directory)
                folder_mapping[directory] = node.name[1]
                prefixes.append(directory)
            elif not os.path.exists(directory):
                os.makedirs(directory)
        prefix = os.path.dirname(os.path.commonprefix(prefixes).rstrip('/'))

        for k,v in iter(folder_mapping.items()):
            folder_mapping[k] = os.path.relpath(v,prefix)
        self.save_mapping(folder_mapping, self.course_tree.root.name[1] + '/mapping.json')

        if not self.duplicate:
            print('Deleting old course folder...')
            rmtree(folder_mapping['root'])

    def packageCourse(self, destination, compress=False, validate=''):
        data = json.load(open(str(self.path) + '/mapping.json'))
        misc_paths = ['/about', '/course', '/policies', '/tabs', '/static', '/assets', '/info']

        if os.path.exists(data['root']):
            if destination:
                new_folder = destination
            else:
                postfix = 1
                while os.path.exists(data['root'] + '_' + str(postfix)):
                    postfix +=1
                new_folder = data['root'] + '_' + str(postfix)

        else:
            new_folder = data['root']

        for key, value in iter(data.items()):
            if key == 'root':
                continue
            elif new_folder != '':
                alternative_path = new_folder + '/' + value[value.find(value.split('/')[1]):]
            else:
                alternative_path = value
            if not os.path.exists(os.path.dirname(alternative_path)):
                os.makedirs(os.path.dirname(alternative_path))

            copyfile(key,alternative_path)

        for p in misc_paths:
            if os.path.exists(str(self.path) + p):
                if not os.path.exists(new_folder + p):
                    copytree(str(self.path) + p, new_folder + p)
                else:
                    print('Path  ' + new_folder + p + ' already exists. Skipping copying')

        if compress:
            print('Compressing course folder...')
            with tarfile.open(new_folder + '.tar.gz', 'w:gz') as tar:
                tar.add(new_folder, arcname=os.path.basename(new_folder))


        if validate:
            print(validate)
            self.compareCourses(new_folder, data['root'])

    def compareCourses(self, oldcourse, newcourse):
        comparison = filecmp.dircmp(newcourse,oldcourse)

        print('Files only included in ' + newcourse + ' : ' + str(comparison.left_only))
        print('Files only included in ' + oldcourse + ' : ' + str(comparison.left_only))

    def save_mapping(self, folder_mapping, path):

        with open(path, 'w') as fp:

            json.dump(folder_mapping, fp)


    def describeCourse(self, destination):
        """
        Write header to the README.md with the course name.
        """
        if not destination:
            postfix = 1
            destination = str(self.path).rstrip('/') + '_structured'
            if os.path.exists(destination):
                while os.path.exists(destination + '_' + str(postfix)):
                    postfix += 1
                destination = destination + '_' + str(postfix)
            self.course_tree = Node((str(self.path).rstrip('/'), destination))
        else:
            self.course_tree = Node((str(self.path).rstrip('/'), destination))

        Node((self.course_file.name, str(self.course_path) + '.xml'),
                 parent=self.course_tree)
        self.describeChapter()
        self.createFolderStructure()


    def describeChapter(self):
        """
        Write section information into readme
        """
        prefix = 'section_'
        count = 0
        for c in self.chapter_list:
            count+=1
            # build path
            c += '.xml'
            cFile = self.chapter_path / c

            # write to file
            chap_xml = ET.parse(str(cFile)).getroot()

            chap_name = chap_xml.attrib['display_name']
            folder = prefix + str(count)
            chapter_node = Node((folder, self.course_tree.name[1] + '/' + folder), parent=self.course_tree)
            Node((self.get_valid_filename(chap_name) + '.xml', str(cFile)), parent=chapter_node)
            # remove empty sequential item
            seq_list = [child.attrib['url_name'] for child in chap_xml]
            # pass to describe the sequence further
            pub_seq_struct, all_seq_struct = self.describeSequen(seq_list, chapter_node)

            ### public struct
            self.public_problems_struct[chap_name] = pub_seq_struct
            ### use section title + last 5 digits of file id as key
            self.all_problems_struct['(' + c[-9:-4] + ')' + chap_name] = (str(cFile), all_seq_struct)

        self.public_problems_struct = dict((k, v) for k, v in iter(self.public_problems_struct.items()) if v)

    def describeSequen(self, seq, chapter_node):
        """
        Write subsection information into readme
        Input:
            [seq]: the list of sequential file to describe further
        """
        pub_seq = OrderedDict()
        all_seq = OrderedDict()
        prefix = 'subsection_'
        count = 0
        for s in seq:
            count += 1
            unpublished = False
            s_name = s + '.xml'
            sFile = self.seq_path / s_name

            seq_xml = ET.parse(str(sFile)).getroot()
            sequ_name = seq_xml.attrib['display_name']
            folder = prefix + str(count)
            subsection_node = Node((folder, chapter_node.name[1] + '/' + folder), parent=chapter_node)
            Node((self.get_valid_filename(sequ_name) + '.xml', str(sFile)), parent=subsection_node)
            if len(seq_xml.getchildren()) > 0:
                unit_list = [child.attrib['url_name'] for child in seq_xml]
                pub_dict, all_dict = self.describeUnit(unit_list, subsection_node)
                pub_seq[sequ_name] = pub_dict

                ### check draft

                if s in self.draft_problems_struct.keys():
                    if self.draft_problems_struct[s]:
                        all_dict2 = self.describeDraftUnit(self.draft_problems_struct[s], subsection_node)
                        for d in all_dict2:
                            all_dict[d] = all_dict2[d]

                ### use subsection title + last 5 digits of file id as key
                all_seq['(' + s_name[-9:-4] + ')' + sequ_name] = (str(sFile), all_dict)

                if unpublished:
                    print(
                    '\033[93m Warning: There are unpublished changes in published problems under subsection {}. Only looking at published version.\033[0m'.format(
                        sequ_name))

            else:  # check draft

                if s not in self.draft_problems_struct.keys():
                    all_dict = OrderedDict()
                else:
                    all_dict = self.describeDraftUnit(self.draft_problems_struct[s], subsection_node)
                ### use subsection title + last 5 digits of file id as key
                all_seq['(' + s_name[-9:-4] + ')' + sequ_name] = (str(sFile), all_dict)

        pub_seq = dict((k, v) for k, v in iter(pub_seq.items()) if v)
        return pub_seq, all_seq

    def describeUnit(self, uni, subsection_node):
        """
        Write unit information into readme
        Input:
            [uni]: the list of unit files to describe further
        """
        pub_uni = OrderedDict()
        all_uni = OrderedDict()
        prefix = 'unit_'
        count = 0
        for u in uni:
            count += 1
            u += '.xml'
            uFile = self.vert_path / u
            uni_xml = ET.parse(str(uFile)).getroot()
            u_name = uni_xml.attrib['display_name']
            folder = prefix + str(count)

            unit_node = Node((folder, subsection_node.name[1] + '/' + folder), parent=subsection_node)
            Node((self.get_valid_filename(u_name) + '.xml' , str(uFile)), parent=unit_node)
            prob_list = []
            for child in uni_xml:
                if child.tag in ['problem', 'video', 'html']:
                    prob = child.attrib['url_name']
                    prob_list.append([child.tag, prob])


            pub_dict, all_dict = self.describeProb(prob_list, unit_node)
            pub_uni[u_name] = pub_dict
            ### use unti title + last 5 digits of file id as key
            all_uni['(' + u[-9:-4] + ')' + u_name] = (str(uFile), all_dict)
        pub_uni = dict((k, v) for k, v in iter(pub_uni.items()) if v)
        return pub_uni, all_uni

    def describeProb(self, prob_list, unit_node):
        """
        Write component information into readme
        Input:
            [prob_list]: the list of problems to describe further
        """
        pub_prob = OrderedDict()
        pro_list = []

        counts = {'video': 0,'html': 0, 'problem': 0}
        for pro in prob_list:
            pro_name = pro[1] + '.xml'
            pFile = self.path / pro[0] / pro_name
            pro_xml = ET.parse(str(pFile)).getroot()
            counts[pro[0]] += 1
            elements = [elem.text for elem in pro_xml.iter('choicehint')]
            if 'display_name' in pro_xml.attrib.keys():
                Dict = pro_xml.attrib
                p_name = '' if Dict['display_name'].isdigit() or pro[0] == pro_xml.attrib['display_name'].lower() else '_' + pro_xml.attrib['display_name']
                problem_name = pro[0] + str(counts[pro[0]]) + '_' + elements[0].split(':')[-1].strip(' ').strip('.') if len(elements) > 0 else pro[0] + str(counts[pro[0]])

                if 'weight' in Dict.keys():
                    if 'max_attempts' in Dict.keys():
                        pub_prob[p_name] = {'file': pro_name, 'weight': Dict['weight'],
                                            'max_attempts': Dict['max_attempts']}
                    else:
                        pub_prob[p_name] = {'file': pro_name, 'weight': Dict['weight']}
                if pro[0] == 'problem':
                    Node((self.get_valid_filename(problem_name) + '.xml', str(pFile)), parent=unit_node)
                elif pro[0] == 'html':
                    Node((self.get_valid_filename(pro[0] + str(counts[pro[0]]) +  p_name) + '.xml',  str(pFile)), parent=unit_node)
                    Node((self.get_valid_filename(pro[0] + str(counts[pro[0]]) +  p_name) + '.html',  str(pFile).rsplit('.',1)[0] + '.html'), parent=unit_node)

                else:
                    Node((self.get_valid_filename(pro[0] + str(counts[pro[0]]) +  p_name) + '.xml', str(pFile)), parent=unit_node)


            else:
                problem_name = elements[0].split(':')[-1] if len(elements) > 0 else pro[0] + str(counts[pro[0]])
                Node((self.get_valid_filename(problem_name) + '.xml', str(pFile)), parent=unit_node)
                if pro[0] == 'html':
                    Node((self.get_valid_filename(problem_name) + '.html', str(pFile).rsplit('.',1)[0] + '.html'), parent=unit_node)

            pro_list.append((str(pFile), pro[0]))

        pub_prob = dict((k, v) for k, v in iter(pub_prob.items()) if v)
        return pub_prob, pro_list

    def describeDraftUnit(self, unit, subsection_node):
        """
        Write draft unit information into readme
        Again, draft need to be handled specifically because it is linked backward.
        Input:
            [unit]: the list of unit files that need to be described further.
        """
        all_uni = OrderedDict()
        prefix = 'draft_unit_'
        count = 0
        for u in unit:
            count +=1
            uFile = Path(u[0])
            un_xml = ET.parse(str(uFile)).getroot()
            u_name = un_xml.attrib['display_name']
            folder = prefix + str(count)

            unit_node = Node((folder, subsection_node.name[1] + '/' + folder), parent=subsection_node)
            Node((self.get_valid_filename(u_name) + '.xml',  str(uFile)), parent=unit_node)
            prob_list = self.describeDraftProb(u[1:],unit_node)
            ### use unit title + last 5 digits of file id as key
            all_uni['(' + u[0][-9:-4] + ')(draft)' + u_name] = (str(uFile), prob_list)
        return all_uni

    def describeDraftProb(self, probs, unit_node):
        """
        Write draft component information into readme
        Again, draft need to be handled specifically because it is linked backward.
        Input:
            [probs]: the list of problem files that need to be described further.
        """
        prob_list = []
        counts = {'video': 0,'html': 0, 'problem': 0}

        for pro in probs:
            counts[pro[0]] += 1
            pro_name = pro[1] + '.xml'
            pFile = self.draft_path / pro[0] / pro_name
            pro_xml = ET.parse(str(pFile)).getroot()
            p_name = '' if not 'display_name' in pro_xml.attrib or pro_xml.attrib['display_name'].isdigit() else '_' + pro_xml.attrib['display_name']

            if pro[0] == 'problem':
                Node((self.get_valid_filename( 'draft_' + pro[0] + str(counts[pro[0]]) + p_name) + '.xml', str(pFile)), parent=unit_node)
            elif pro[0] == 'html':
                Node(('draft_' + pro[0] + str(counts[pro[0]]) + '.xml', str(pFile)), parent=unit_node)
                Node(('draft_' + pro[0] + str(counts[pro[0]]) + '.html', str(pFile).rsplit('.',1)[0] + '.html'), parent=unit_node)
            else:
                Node(('draft_' + pro[0] + str(counts[pro[0]]) + '.xml', str(pFile)), parent=unit_node)


            prob_list.append((str(pFile), '(draft)' + pro[0]))
        return prob_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store', dest='package',default=False)
    parser.add_argument('-c', action='store', dest='course_folder')
    parser.add_argument('-dst', action='store', dest='destination_folder')

    parser.add_argument('-cmp', action='store', dest='compress',default=False)
    parser.add_argument('-d', action='store', dest='duplicate',default=True)
    parser.add_argument('-ver', action='store', dest='verify')

    args = parser.parse_args()

    duplicate = args.duplicate
    package_course = args.package
    destination = args.destination_folder
    course_folder = args.course_folder
    compress = True if args.verify == 'True' else False
    verify_course = True if args.verify == 'True' else False

    if not course_folder:
        sys.exit("\033[91m Please pass in the name of the course folder.\033[0m")
    elif destination and os.path.exists(destination):
        sys.exit("\033[91m Destination folder already exists.\033[0m")


    writeDoc = DocDict(course_folder.rstrip('/'),package=package_course, duplicate=duplicate)

    if package_course:
        writeDoc.packageCourse(destination,compress=compress, validate=verify_course)
    else:
        writeDoc.describeCourse(destination)