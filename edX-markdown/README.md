## Translate from markdown files to XML files

This folder contains code used to translate files in markdown format to XML format, which can be used in edX to create problem units.

Each problem unit contains two parts, python script and markdown concept. Python script is used to generate random number used in the problem and to calculate problem solutions. Markdown concept is the description of the problem. Instructors can write python code and markdown code in one file and save it with .imd format. The translator will then take the .imd file and translate it into a XML file which edX recognizes. Then, instructors can paste the XML code into edX studio to create a problem.

#### Create and translate to XML (See ```input_imd\imd_examples``` for imd examples)

1. Write .imd files in ```input_imd``` folder.
2. fill in ```problems_mapping.json``` with imd file names.
3. open terminal to run

		python translate.py <week_id> <problem_id>

4. find output files in ```output_XML``` folder
5. paste XML content to edX to generate problems.
