## Translate from markdown files to XML files

This folder contains code used to translate files in imd (our own ipython markdown) format to XML format, which can be used in edX to create problem units.

Each problem unit contains three parts, python script, problem markdown, and test script. Python script is used to generate random numbers used in the problem and to calculate problem solutions. Problem markdown is the text of the problem written using (markdown)[https://daringfireball.net/projects/markdown/syntax]. Test script defines input/output pairs for testing the python script.

Instructors write python code, markdown code, and test code in one file and save it in a file with an .imd extension. The translator will then take the .imd file and translate it into a XML file which edX studio recognizes. Then, instructors can paste the XML code into edX studio to create a problem.

#### Create and translate to XML (See ```input_imd\imd_examples``` for imd examples)

1. Create a .imd file.
2. Open terminal and run the following to learn more about the translator script.

		python translate.py -h
		
   (i) Run the following to translate a file:
   
   		python translate.py -path [path]

3. paste XML content to edX to generate problems.
