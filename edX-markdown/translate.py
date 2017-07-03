## Written by Zhipeng Yan and Zhen Zhai
## Translate imd files to xml
## Can have math expressions wrapped with $$ \math $$
## and also inline math expression $ \math $
## Use variables in html by having \$ at front

import markdown
import json
import sys

def XML_wrapper(content):
	return '<problem>\n  <text>\n{0}\n  </text>\n</problem>\n'.format(content)

def py_wrapper(code):
	#XML_PY_EVAL = XML_PY_START + 'from hint import evaluate\ndef check(expect, ans):\n  return evaluate.evaluate(expect, ans)\n' + XML_PY_END
	return '    <script type="loncapa/python">\n{0}\n    </script>\n\n\n'.format(code)

def math_wrapper(sol):
	return '    <customresponse cfn="check" expect="\[${0}\]">\n      <textline/>\n    </customresponse>\n\n'.format(sol)

def option_wrapper(opt, sol):
	opt_string = '      <optioninput options="${0}" correct="${1}"/>'.format(opt, sol)
	return '    <optionresponse>\n'+opt_string+'\n    </optionresponse>\n\n'

def multi_choice_wrapper(choices):
	head = '    <choiceresponse>\n      <checkboxgroup>\n'
	end = '      </checkboxgroup>\n    </choiceresponse>\n\n'
	return head+choices+end

def correct_choice_wrapper(choice):
	return '<choice correct="true">{0}</choice>\n'.format(choice)

def wrong_choice_wrapper(choice):
	return '<choice correct="false">{0}</choice>\n'.format(choice)

def read_md(contents):
	'''
	Given imd file content, split python code and markdown code. Then, convert markdown code to HTML.
	input:
		contents: imd file content
	output:
		python_code: python code
		html_code: converted from markdown code to html code
	'''

	if "```python\n" in contents:
		start_index = contents.index("```python\n")
		end_index = contents.index("```\n")
		python_code = contents[start_index+1:end_index]
		python_code = "".join(python_code)
		md_code = contents[end_index+1:]
	else:
		python_code = ""
		md_code = contents

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

		line = line.replace('\\$','\001')   # record dollar sign in $var by a safe substitute

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

		line = line.replace('\001','$')
		md_code[j] = line
	html_code = markdown.markdown("".join(md_code), extensions=['markdown.extensions.tables'], output_format="HTML")

	f.close()

	return python_code, html_code

def convert_html(html_code, py_code):
	html_code = html_code.splitlines()
	py_code_lines = py_code.splitlines()
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

			xml_code = option_wrapper(opt, sol)
			updated_html_code += xml_code
			part_id += 1

		elif '<p>[_]</p>' == line:
			xml_code = math_wrapper('solution'+str(part_id))
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
				choice_insert = wrong_choice_wrapper(choice_context[3:])
			elif '[x]' in line:
				choice_insert = correct_choice_wrapper(choice_context[3:])

			choice_list += choice_insert

			if '</p>' in line:
				updated_html_code += multi_choice_wrapper(choice_list)
				part_id += 1
				choice_list = ""

		else:
			updated_html_code.append(line)
			updated_html_code.append("\n")

	updated_html_code = "".join(updated_html_code)
	template = XML_wrapper(py_wrapper(py_code) + updated_html_code)
	return template




if __name__ == "__main__":
	if sys.argv[1] == "--help":
		print "Please type in parameters as follow(if you have variables type in 1 at the end):"
		print "python translate.py <Week ID> <Problem ID> <1>"
		sys.exit()

	var = ""
	if len(sys.argv) == 3:
		week, problem = sys.argv[1:]
	elif len(sys.argv) == 4:
		week, problem, var = sys.argv[1:]
	else:
		sys.exit("Error, see 'python translate.py --help' for input requirement")

    # Get source file name
	mapping = json.loads(open("problems_mapping.json").read())
	mapping_key = "Week{0}_Problem{1}".format(week, problem)
	#mapping_key = "PracticeFinal{1}".format(week, problem)
	file_name = mapping[mapping_key]
	input_file_name = "input_imd/{0}".format(file_name)
	output_file_name = "output_XML/{0}.xml".format(mapping_key)

	f = open(input_file_name, "r")
	contents = f.readlines()
	f.close()

	print "generating XML"

	py_code, html_code = read_md(contents)

	template = convert_html(html_code, py_code)

	print "writing files ..."

	f = open(output_file_name, "w")
	f.write("".join(template))
	f.close()

	print "Done! XML files saved in output_XML folder!"
