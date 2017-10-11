#!/usr/bin/env python

from pathlib import Path
from collections import defaultdict
import re

class Doc:
    '''
    Create a detail documentation for the course file exported from edX.
    '''

    ## Path variables
    path = Path('.')
    course_path = path / 'course'
    chapter_path = path / 'chapter'
    seq_path = path / 'sequential'
    vert_path = path / 'vertical'

    draft_path = path / 'drafts'
    draft_vert_path = draft_path / 'vertical'

    ## List of all chapters
    chapter_list = []

    ## Structure of sections and units
    draft_problems_struct = defaultdict(list)


    def __makeCourse(self):
        '''
        Create a list of chapters by reading course.xml
        '''
        course_path = self.course_path / 'course.xml'
        course_txt = course_path.open().readlines()[1:]
        for cline in course_txt:
            if 'chapter' in cline:
                chap_name = cline.split('"')[1]
                self.chapter_list.append(chap_name)

    def __makeDraftStruct(self):
        '''
        Create a problems to units mapping for drafts
        by reading files from folder vertical
        '''
        self.draft_problems_struct = defaultdict(list)
        for v in self.draft_vert_path.iterdir():
            if v.suffix != '.xml':
                continue
            v_txt = v.open().readlines()
            fline = v_txt[0]
            sec_name = fline[fline.index('+block@')+7:].split('"')[0]
            rank = fline[fline.index('index'):].split('"')[1]
            comp_list = [int(rank), str(v)]
            for vline in v_txt[1:]:
                if '<problem ' in vline:
                    prob = vline.split('"')[1]
                    comp_list.append(['problem',prob])
                elif '<video ' in vline:
                    prob = vline.split('"')[1]
                    comp_list.append(['video', prob])
                elif '<html ' in vline:
                    prob = vline.split('"')[1]
                    comp_list.append(['html', prob])
            self.draft_problems_struct[sec_name].append(comp_list)
        for k in self.draft_problems_struct:
            sorted_struct = sorted(self.draft_problems_struct[k], key = lambda x: x[0])
            self.draft_problems_struct[k] = [s[1:] for s in sorted_struct]


    def __init__(self):
        self.__makeCourse()
        self.__makeDraftStruct()


    def describeCourse(self):
        readme = open('README.md', 'w')
        readme.write("###Course structure - [course/course.xml](course/course.xml)\n")
        self.describeChapter(readme)
        readme.close()


    def describeChapter(self, readme):
        '''
        Write section information into readme
        '''
        for c in self.chapter_list:
            c += '.xml'
            cFile = self.chapter_path / c
            chap_txt = cFile.open().readlines()
            first_line = chap_txt[0]
            chap_name = first_line.split('"')[1]
            readme.write('* [Section] {0} - [{1}]({1})\n'.format(chap_name, str(cFile)))
            seq_list = [l.split('"')[1] for l in chap_txt if "sequential" in l]
            self.describeSequen(seq_list, readme)


    def describeSequen(self, seq, readme):
        '''
        Write subsection information into readme
        '''
        for s in seq:
            s_name = s + '.xml'
            sFile = self.seq_path / s_name
            seq_txt = sFile.open().readlines()
            first_line = seq_txt[0]
            sequ_name = first_line.split('"')[1]
            readme.write('\t* [Subsection] {0} - [{1}]({1})  \n'.format(sequ_name, str(sFile)))
            if len(seq_txt) > 2:
                unit_list = [l.split('"')[1] for l in seq_txt if "vertical" in l]
                self.describeUnit(unit_list, readme)
            else: #check draft
                self.describeDraftUnit(self.draft_problems_struct[s], readme)

    def describeUnit(self, uni, readme):
        """
        Write unit information into readme
        """
        for u in uni:
            u += '.xml'
            uFile = self.vert_path / u
            uni_txt = uFile.open().readlines()
            first_line = uni_txt[0]
            u_name = first_line.split('"')[1]
            readme.write('\t\t* [Unit] {0} - [{1}]({1})\n'.format(u_name, uFile))
            prob_list = []
            for l in uni_txt[1:]:
                if '<problem ' in l:
                    prob = l.split('"')[1]
                    prob_list.append(['problem',prob])
                elif '<video ' in l:
                    prob = l.split('"')[1]
                    prob_list.append(['video', prob])
                elif '<html ' in l:
                    prob = l.split('"')[1]
                    prob_list.append(['html', prob])
                #elif '<discussion ' in l:
                #    prob = l.split('"')[1]
                #    comp_list.append(['discussion', prob])

            self.describeProb(prob_list, readme)

    def describeProb(self, prob_list, readme):
        '''
        Write component information into readme
        '''
        pat1=re.compile(r'<problem ([^>]+)>')
        pat2 = re.compile(r'(\S+)="([^"]+)"')

        for pro in prob_list:
            pro_name = pro[1]+'.xml'
            pFile = self.path / pro[0] / pro_name
            p_txt = pFile.open().readlines()
            fline = p_txt[0]
            m = pat1.match(fline)
            if m:
                params = m.group(1)
                m2 = pat2.findall(params)
                Dict= {key:val for key,val in m2 if key!='markdown'}
                p_name = Dict['display_name']
                weight = Dict['weight']
                max_att = Dict['max_attempts']

            if pro[0] == 'problem':
                readme.write('\t\t\t* [{0}] {1} - [{2}]({2})\n\n'.format(pro[0], p_name, str(pFile)))
                readme.write('\t\t\t\t Weight: {0}, Max Attempts: {1}\n'.format(weight, max_att))
            else:
                readme.write('\t\t\t* [{0}] - [{1}]({1})\n'.format(pro[0], str(pFile)))

    def describeDraftUnit(self, unit, readme):
        '''
        Write draft unit information into readme
        '''
        for u in unit:
            uPath = Path(u[0])
            first_line = uPath.open().readlines()[0]
            u_name = first_line.split('"')[1]
            readme.write('\t\t* [Unit]\(Draft\) {0} - [{1}]({1})\n'.format(u_name, u[0]))
            self.describeDraftProb(u[1:], readme)

    
    def describeDraftProb(self, probs, readme):
        '''
        Write draft component information into readme
        '''
        for pro in probs:
            pro_name = pro[1]+'.xml'
            pFile = self.draft_path / pro[0] / pro_name
            p_txt = pFile.open().readlines()
            fline = p_txt[0]
            p_name = fline.split('"')[1]
            if pro[0] == 'problem':
                readme.write('\t\t\t* [{0}]\(Draft\) {1} - [{2}]({2})\n'.format(pro[0], p_name, str(pFile)))
            else:
                readme.write('\t\t\t* [{0}]\(Draft\) - [{1}]({1})\n'.format(pro[0], str(pFile)))



if __name__ == "__main__":
    writeDoc = Doc()
    writeDoc.describeCourse()

