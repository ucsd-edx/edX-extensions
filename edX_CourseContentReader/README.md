## Merging two edX repositories
repository = exported course.

1. Download and untar the two repositories.
2. Create a description file that describes each chapter/section/problem for each repository.
   Each line contains:
   * A readable description of the section, the path to the xml file in the repository (includin the repository name)
3. MANUAL: Using an editor, create a new description file that contains lines from either of the two original files.
   For example, I combined weeks 1-2 from CSE103 with weeks 3-9 of DSE210x
4 Create the new rpository based on the new description. One repository is considered the "origin" and the files that are not in the XML tree are taken from there. The xml files are taken from the incoming repository (we can have more than one). 
   1. Remove files that correspond to description lines of the original that have been removed.
   2. Copy new files from the incoming repositories.


## Describe edX Course Content Data
[Detail description from edX](http://edx.readthedocs.io/projects/devdata/en/latest/internal_data_formats/course_structure.html#course-structure)

This folder contains code to generate README.md to describe edX course content file exported from edX interface.

### 1. Setup
cd to current directory and run

	source setup.sh

(If you want this setup script to run automatically, add a line to your .bashrc)

#### You need to have Python2

### 2. Using makeDoc.py
* Export your course from edX
* Unzip the exported .tar.gz file
* cd into the unzipped folder
* run makeDoc.py

		makeDoc.py
	
* The script will generate a README.md to describe your course content.
