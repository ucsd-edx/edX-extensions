
# coding: utf-8

# # Translator Class

# ## Intro
# 
# <strong> This file contains all of the code for the translator class. </strong>
# 
# Putting the code for this class in an .ipynb makes it so that we can work on this class together in real time. There could possibly be some overwrite issues if we are both working on the file at the same time. But an easy fix to that problem is to simply make a copy of this file and then to work on the copy. We should also notify each other when we are changing the main .ipynb file. Once finished, the copy can be pasted back into the main Translator Class file.
# 
# Once we have finished the translator class we can copy and paste all this stuff into a .py file for implementation.
#  
# 
# <strong style="color:#FF5733;font-size: 14pt">Idea: </strong >
# <div>We could have the class be something that people just import into a jupyter notebook. The nice thing about this is that if they create the markdown in a jupyter notebook and write their python code in a jupyter notebook. We could just make it so that they give the path an output file and then hte xml is produced their. Then they can do all their work in a single notebook. The user wont have to copy all their code into a seperate imd file and they wont have to worry about the JSON file. This would also be simpler to code.</div> 

# ## Running Code
# 
# This code <span style="color:gray">(as of now)</span> is meant to be run as a **.py** file. The default python file to use is `TransalterClass.py`. Checkout the <span style="color:lime">Main Code</span> section to learn how use this **.py** file. To convert this **.ipynb** file to a **.py** run the following line of code in your computer's **terminal**:
# 
# ```
# jupyter nbconvert --to script TranslaterClass.ipynb
# ```
# 

# # <strong style="color:fuchsia">Class</strong>  Translater <span style="color:gray">(empty)</span>

# import required packages

# In[1]:

import markdown
import json
import sys
import argparse


# The translator <font style="color:fuchsia">Class</font> translates IMD files, into other formats. The code below just proved some very basic helper functions and the the initialization function. The other functions are added in the <font style="color:blue">Function</font> sections.
# 
# Translator is initialized with the specific problem you would like to translate. The initialization variables are: 
# * JSON_filename: this provides a mapping from assignment/problem to the imd file. See JSON file for an example.
# * assign_id: The assignment number that you would like to translate.
# * prob_id: The problem number you would like to translate.

# In[2]:


class Translator:
    
    # Variable List:
    input_file   =None
    output_file  =None
    
    py_code      =None
    md_code      =None
    test_code    =None
    html_code    =None
    xml_code     =None

    
    """
    The translator class translates IMD files, into other formats.     
    """
    
    def __init__(self, assign_num, prob_num, JSON_filename="problems_mapping.json",
                input_dir="input_imd", output_dir="output_xml"):
        
        """
        On initializtion we select the problem to translate from the JSON mapping file.
        We use this mapping file to designate the input_file and the output_file.

        Here is an example of what the JSON file look like:
        {
            "Assignment1_Problem1": "imd_examples/basic_example.imd",
            "Assignment1_Problem2": "imd_examples/variables_example.imd",
            "Assignment1_Problem3": "imd_examples/checkbox_example.imd",
            "Assignment1_Problem4": "imd_examples/dropdown_example.imd"
        }

        """
        mapping = json.load(open(JSON_filename,"r"))
        mapping_key = "Assignment{0}_Problem{1}".format( str(assign_num), str(prob_num) )
        file_name = mapping[mapping_key]
        
        self.input_file  = input_dir+"/{0}".format(file_name)
        self.output_file = output_dir+"/{0}.xml".format(mapping_key) 

    """
    Private wrappers

        The following functions are all helper functions for the Translator class.
        They are used when code is being converted into the XML format.
        Basically, what these functions do is provide the correct xml format
        when converting specifics parts of the `.imd` into `.xml`
    """

    def __XML_wrapper(self, content):
        return '<problem>\n  <text>\n{0}\n  </text>\n</problem>\n'.format(content)

    def __py_wrapper(self, code):
        #XML_PY_EVAL = XML_PY_START + 'from hint import evaluate\ndef check(expect, ans):\n  return evaluate.evaluate(expect, ans)\n' + XML_PY_END
        return '    <script type="loncapa/python">\n{0}\n    </script>\n\n\n'.format(code)

    def __math_wrapper(self, sol):
        return '    <customresponse cfn="check" expect="\[${0}\]">\n      <textline/>\n    </customresponse>\n\n'.format(sol)

    def __option_wrapper(self, opt, sol):
        opt_string = '      <optioninput options="${0}" correct="${1}"/>'.format(opt, sol)
        return '    <optionresponse>\n'+opt_string+'\n    </optionresponse>\n\n'

    def __multi_choice_wrapper(self, choices):
        head = '    <choiceresponse>\n      <checkboxgroup>\n'
        end = '      </checkboxgroup>\n    </choiceresponse>\n\n'
        return head+choices+end

    def __correct_choice_wrapper(self, choice):
        return '<choice correct="true">{0}</choice>\n'.format(choice)

    def __wrong_choice_wrapper(self, choice):
        return '<choice correct="false">{0}</choice>\n'.format(choice)


    """
    Public Functions
    """
    def read_imd(self):
        f = open(self.input_file, "r")
        contents = f.readlines()
        f.close()
        return contents

    def write_xml(self):
        f = open(self.output_file, "w")
        f.write(self.xml_code)
        f.close()
           
    def toHtml(self):
        return markdown.markdown("".join(self.md_code),extensions=['markdown.extensions.tables'],output_format="HTML")


    def loadImd(self, imd_contents):
        '''
        Splits imd codes into the python portion, the test portion, and the true imd portion.
        input:
            imd codes
        output:
            python_code: python code
            md_code: markdown code
            test_code: test code
        '''

        contents = imd_contents
        
        # Read python code
        if "```python\n" in contents:
            start_index = contents.index("```python\n")
            end_index = contents.index("```\n")
            python_code = contents[start_index+1:end_index]
            python_code = "".join(python_code)
            contents = contents[:start_index] + contents[end_index+1:]
        else:
            python_code = ""

        # Read test code
        if "```test\n" in contents:
            start_index = contents.index("```test\n")
            if "```\n" in contents:
                end_index = contents.index("```\n")
            elif "```" in contents:
                end_index = contents.index("```")
            else:
                print "didn't close test section"
            test_code = contents[start_index+1:end_index]
            test_code = "".join(test_code)
            contents = contents[:start_index] + contents[end_index+1:]
        else:
            test_code = ""

        md_code = contents[:]

        inline = 0  # open or closed parantheses
        double = 0  # open or closed brackets
        inlineSub = ['\\\\\\(', '\\\\\\)']
        doubleSub = ['\\\\\\[', '\\\\\\]']

        # Read markdown line by line
        for j in xrange(len(md_code)):
            line = md_code[j]

            # trim the empty space at the front
            while line[0] == " ":
                line = line[1:]

            # trim the empty space at the end, but preserve the newline
            while len(line) > 3 and line[-2] == " ":
                line = line[:-2] + line[-1]

            # record dollar sign in $var by a safe substitute
            line = line.replace('\\$','\001')

            # substitute inline and newline math expression wrapper
            i=0
            while i < len(line):
                if line[i:i+2] == '$$':
                    line = line[:i]+doubleSub[double]+line[i+2:]
                    double = 1 - double
                    i += 4
                elif line[i] == '$':
                    line = line[:i]+inlineSub[inline]+line[i+1:]
                    inline = 1-inline
                    i += 4
                else:
                    i += 1

            # mark variables with $ sign
            line = line.replace('\001','$')
            md_code[j] = line
            
        self.py_code = python_code
        self.md_code = md_code
        self.test_code = test_code
        self.html_code = self.toHtml()



    def toXml(self):
        """
        returns the XML code that is to be pasted into EDX studio
        """
        html_code = self.html_code.splitlines()
        py_code_lines = self.py_code.splitlines()

        choice_list = ""
        updated_html_code = []
        part_id = 1
        for line in html_code:
            if '<p>[_choice]</p>' == line:
                updated_html_code += ['\n', '\n']
                for s in py_code_lines:
                    if '=' not in s:
                        continue
                    strip_start_index = s.index('=')
                    strip_s = s[:strip_start_index+1].replace(" ", "") + s[strip_start_index+1:]
                    sol_str = 'solution'+str(part_id)+"="
                    opt_str = 'option'+str(part_id)+"="
                    if sol_str in strip_s:
                        sol_index = strip_s.index(sol_str)
                        sol = strip_s[sol_index+len(sol_str):]
                        while sol[0] == ' ':
                            sol = sol[1:]
                        sol = sol.replace('\n','')
                        sol = sol.replace('"','')
                        sol = sol.replace("'", "")
                    elif opt_str in strip_s:
                        opt_index = strip_s.index(opt_str)
                        opt = strip_s[opt_index+len(opt_str):]
                        while opt[0] == ' ':
                            opt = opt[1:]
                        opt = opt.replace("\n","")

                xml_code = self.__option_wrapper(opt, sol)
                updated_html_code += xml_code
                part_id += 1

            elif '<p>[_]</p>' == line:
                xml_code = self.__math_wrapper('solution'+str(part_id))
                updated_html_code += xml_code
                part_id += 1

            elif '[ ]' in line or '[x]' in line:
                # trim <p> and </p>
                if '<p>' in line:
                    updated_html_code += ['\n', '\n']
                    choice_context = line[3:]
                if '</p>' in line:
                    end_index = line.index("</p>")
                    choice_context = line[:end_index]

                while choice_context[0] == ' ':
                    choice_context = choice_context[1:]
                while choice_context[-1] == ' ':
                    choice_context = choice_context[:-1]

                if '[ ]' in line:
                    choice_insert = self.__wrong_choice_wrapper(choice_context[3:])
                elif '[x]' in line:
                    choice_insert = self.__correct_choice_wrapper(choice_context[3:])

                choice_list += choice_insert

                if '</p>' in line:
                    updated_html_code += self.__multi_choice_wrapper(choice_list)
                    part_id += 1
                    choice_list = ""

            else:
                updated_html_code.append(line)
                updated_html_code.append("\n")

        updated_html_code = "".join(updated_html_code)
        
        """   ERROR ERROR ERROR"""
        xml_code = self.__XML_wrapper( self.__py_wrapper(self.py_code) + updated_html_code)
        self.xml_code = "".join(xml_code)

    def translate(self):  
        """
        Contains all the steps of converting from imd file to xml file.
        Includes loading imd file, converting imd code to XML code, and saving the XML code.
        """
        imd_code = self.read_imd()
        self.loadImd(imd_code)
        self.toXml()
        self.write_xml()

    def test(self):
        """
        Tests the IMD code, the code will be in 3 parts. 
            1: python code
            2: tests
            3: the markdown

        2: Tests
            A test consists of:
                set variables
                computed answers
                correct and incorrect answers

        Tests returns
            a boolean variable of correctness
            a string describing the error if it was incorrect
        """
        import traceback
        from eval_lib.evaluate import evaluate

        scope = {}
        try:
            exec self.py_code in scope
        except Exception as err:
            print "!!!Python Code Error:"
            print traceback.format_exc()
            return False

        try:
            exec self.test_code in scope
        except Exception as err:
            print "!!!Test Code Error:"
            print traceback.format_exc()
            return False

        # TODO: is it easier to have a list of solutions in the form of {0}.var
        #   or have instructor write the solutions in order.
        sol_code = self.py_code[self.py_code.index('\nsolution1'):]
        exec sol_code in scope

        part_counts = 0
        for i in scope.keys():
            if i.startswith('solution'):
                part_counts+=1

        for i in xrange(part_counts):
            sol = 'solution{0}'.format(i+1)
            s = scope[sol]
            check = 'check{0}'.format(i+1)
            for c in scope[check]:
                if evaluate(s, c[0]) != c[1]:
                    print c, " doesn't match solution ", s
                    return False
        
        return True



# # <span style="color:blue">Function: </span> Display Html

# This function displays the HTML code of the IMD file. Ideally, this function will display the code as it is seen on the EDX interface. Also, currently the function only really does anything inside a jupyter notebook.

# In[22]:

from IPython.display import display,HTML

def displayHtml(self):  
        display(HTML( self.html_code  ))
        
Translator.displayHtml = displayHtml



# ## Running Code
# 
# This is the code that runs when you call the `TranslaterClass.py` file. This code is called by opening your computer's **terminal** and running a command like the following:
# 
# ```
# python TranslaterClass.py 1 1
# ```
# 
# Note that `assignment` and `problem` are required input arguments for the code to run. To get the full list of possible inputs, runn the following:
# 
# ```
# python TranslaterClass.py -h
# ```


if __name__ == "__main__":
    
    # Setup arguments to be parsed
    ap = argparse.ArgumentParser(description = 'This python script will translate imd files into XML files, \
        which can be used in edX studio to create problems.')
    ap.add_argument('assignmentID', type=int, help='Assignment ID (integer)')
    ap.add_argument('problemID', type=int, help='Problem ID (integer)')
    ap.add_argument('-json', metavar='json_filename', default="problems_mapping.json",
        help='The filename of the mapping. (default: "problems_mapping.json")')
    ap.add_argument('-input', metavar='input_dir', default="input_imd",
        help='The folder containing all the input(imd) files. (default:"input_imd")')
    ap.add_argument('-output', metavar='output_dir', default="output_xml",
        help='The folder containing all the output(XML) files. (default:"output_xml")')
    args = ap.parse_args() #<-- For Debugging: comment out this line, and uncomment the line below
    #args = type('',(),{})();  args.assignment, args.problem, args.JSON_filename, args.input_dir, args.output_dir = 1, 1, "problems_mapping.json", "input_imd", "output_xml"
    
    # check if user supplied requried arguments
    if args.assignmentID == None or args.problemID == None:
        sys.exit("Error: missing arguments. See 'python translate.py -h' for input requirements.")
        
    print "Translating imd into xml"
    translator = Translator(args.assignmentID, args.problemID, args.json, args.input, args.output)
    translator.translate()
    
    print "  Testing XML ..."
    check = translator.test()

    if check:
        print "All tests passed. XML files saved in output_XML folder!"
    else:
        print "Please fix above errors and try again."


# **Old Code**:
# ``` python  
# if sys.argv[1] == "--help":
#     print "This file translates the imd file you wrote into an xml file"
#     print "The name of your imd file should be in the JSON mapping file"
#     print "You should use this file by running a command in your terminal that has the following format:"
#     print "python Translator2.py <assignment num> <problem num>"
#     sys.exit()
# ```
















