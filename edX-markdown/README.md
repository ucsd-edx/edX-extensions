## Translate from markdown files to XML files

This folder contains code used to translate files in imd (our own ipython markdown) format to XML format, which can be used in edX to create problem units.

Each problem unit contains three parts, python script, problem markdown, and test script. Python script is used to generate random numbers used in the problem and to calculate problem solutions. Problem markdown is the text of the problem written using [markdown](https://daringfireball.net/projects/markdown/syntax). Test script defines input/output pairs for testing the python script.

Instructors write python code, markdown code, and test code in one file and save it in a file with an .imd extension. The translator will then take the .imd file and translate it into a XML file which edX studio recognizes. Then, instructors can paste the XML code into edX studio to create a problem.

### 1. Setup
Before the start of each session, cd to this directory and run

	source setup.sh

Once you have run this script, you can cd to your work directory and use the translate.py command without a full path.

(If you want this setup script to run automatically, add a line to your .bashrc)

###You also need to install ply and markdown. 

	pip install ply
	pip install markdown
	
###You also need to use Python2. 

### 2. SelfTest
Run the following in this directory to verify the translate.py runs correctly.

		translate.py imd_examples/basic_example.imd

You should see the following output:

		Translating imd_examples/basic_example.imd into xml
		Testing XML ...
			 python code interpreted.
			 test code interpreted.
			 testing part 1 ...
			 testing part 2 ...
			 testing part 3 ...
		All tests passed. imd_examples/basic_example.xml created!

Look in ```imd_examples``` for more examples of imd files.

### 3. Using translate.py
1. ```translate.py -h``` prints out help message.
2. ```translate.py imd_filename``` runs the test code and generate XML.
3. ```translate.py -html imd_filename``` translate the imd file into an HTML page.
