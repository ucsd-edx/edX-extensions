from glob import glob
import re
pat1=re.compile(r'<problem ([^>]+)>')
pat2 = re.compile(r'(\S+)="([^"]+)"')
for filename in glob('problem/*'):
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
                
            