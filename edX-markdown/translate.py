#!/usr/bin/env python

## Translator Class
import markdown
import json
import sys
import argparse

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
    
    def __init__(self, imd_filename):
        
        """
        On initializtion we give the path to the imd file that needed to be translated.
        """        
        self.input_file  = imd_filename
        self.output_file = self.input_file[:-3]+'xml'

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
        return '    <numericalresponse answer="${0}">\n      <formulaequationinput/>\n    </numericalresponse>\n\n'.format(sol)
        
    def __custom_math_wrapper(self, sol):
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

    def __factorial_replacement(self, exp):
        while '!' in exp:
            end = exp.index('!')
            front = end-1
            while exp[front:end].isdigit():
                front -= 1
            front += 1
            exp = exp[:front]+'fact('+exp[front:end]+')'+exp[end+1:]
        return exp


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
        """
        Used markdown library to translate markdown code to html code.
        Markdown library reference here -> http://pythonhosted.org/Markdown/
        """
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

        for i in xrange(len(py_code_lines)):
            l = py_code_lines[i]
            if 'solution' in l:
                if '!' in l:
                    py_code_lines[i] = self.__factorial_replacement(l)

        choice_list = ""
        updated_html_code = []
        part_id = 1
        first_ol = True
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

            elif line == "<ol>":
                if first_ol:
                    first_ol = False
                    updated_html_code.append(line)
                    updated_html_code.append('\n')
                else:
                    continue
            else:
                updated_html_code.append(line)
                updated_html_code.append('\n')

        new_html = []
        for i in xrange(len(updated_html_code)):
            l = updated_html_code[i]
            if l == '</ol>' and '</ol>' in updated_html_code[i+1:]:
                continue
            else:
                new_html.append(l)

        updated_html_code = "".join(new_html)
        updated_py_code = "\n".join(py_code_lines)
        
        xml_code = self.__XML_wrapper( self.__py_wrapper(updated_py_code) + updated_html_code)
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
        Tests python code and test code in the imd file.
        1. Try to interpret python code
        2. Try to interpret test code
        3. Run test code to see whether all tests pass.
        Returns
            a boolean variable to indicate pass or not.
        """
        import traceback
        from eval_lib.evaluate import evaluate
        from eval_lib.evaluate import evaluate_w_variables

        scope = {}
        try:
            exec self.py_code in scope
        except Exception as err:
            print "!!!Python Code Error:"
            print traceback.format_exc()
            return False
        else:
            print "     python code interpreted."

        try:
            exec self.test_code in scope
        except Exception as err:
            print "!!!Test Code Error:"
            print traceback.format_exc()
            return False
        else:
            print "     test code interpreted."


        # TODO: is it easier to have a list of solutions in the form of {0}.var
        #   or have instructor write the solutions in order.
        # Modify code below(not robust):
        #<===========
        tmp_py = self.py_code.replace(" ", "")
        sol_code = tmp_py[tmp_py.index('solution1='):]
        exec sol_code in scope

        part_counts = 0
        for i in scope.keys():
            if i.startswith('solution') and i[8:].strip().isdigit():
                part_counts+=1
        #<===========

        for i in xrange(part_counts):
            print "     testing part {0} ...".format(i+1)
            sol = 'solution{0}'.format(i+1)
            s = scope[sol]
            check = 'check{0}'.format(i+1)
            if 'variable_values' in scope.keys():
                for c in scope[check]:
                    if evaluate_w_variables(s, c[0], scope['variable_values']) != c[1]:
                        print c, " doesn't match solution ", s
                        return False
            else:
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
# This is the code that runs when you call the `translate.py` file. This code is called by opening your computer's **terminal** and running a command like the following:
# 
# ```
# python translate.py -assign 1 -prob 1
# ```
# 
# Note that `assignment` and `problem` are required input arguments for the code to run. To get the full list of possible inputs, runn the following:
# 
# ```
# python translate.py -h
# ```

if __name__ == "__main__":
    
    # Setup arguments to be parsed
    ap = argparse.ArgumentParser(description = 'This python script will translate imd files into XML files, \
        which can be used in edX studio to create problems.')
    ap.add_argument('imd_filename', default="imd_examples\\basic_example.imd",
        help='The folder containing all the input(imd) files. (default:"input_imd")')
    args = ap.parse_args()
    # check if user supplied requried arguments
    if args.imd_filename == None:
        sys.exit(
            "!!!Error: missing arguments.\
            \n   imd filepath is required.\
            \n   Use -h to see input requirements.")
        

    print "Translating {} into xml".format(args.imd_filename)
    translator = Translator(args.imd_filename)
    translator.translate()
    if translator.test_code == "":
        print "  No tests defined."
        print "{} created!".format(args.imd_filename[:-3]+'xml')
    else:
        print "  Testing XML ..."
        check = translator.test()

        if check:
            print "All tests passed. {} created!".format(args.imd_filename[:-3]+'xml')
        else:
            print "Please fix above errors and try again."















