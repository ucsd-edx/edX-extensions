## Merging two edX repositories

This folder contains scripts used to merge two course into a new course. 

You will need a course that you want to use as the base. We call it original course here. We will remove sections from the oirginal course and will also add sections in the original course. You will also need a course that you want to add files from, we will call it incoming course here. The sections you add to the original course will be from the incoming course.

You will run two scripts to merge the course. First, you will run the pre-update script, which will create description files for the two courses and will also create a new description file for you to edit. After you edit the new description file, it will create a new course based on your new description file, which you can then upload to edX to create a new course.

**Note:**
Please try to avoid adding draft files(unpublished content on edX) from the incoming course to the original course. Please make sure you publish the changes on edX before you export the course file.

### 1. Setup
cd to current directory and run

	source setup.sh

(If you want this setup script to run automatically, add a line to your .bashrc)

### 2. Download course files
* Export both original and incoming course files from edX and put in one folder.
* cd into the folder containing both course files.
* run pre-update script, this script will generate two description files, one for the original course and one for the incoming course. It will also generate another new description file by duplicating the original course description file. You will then edit the new description file before you run the second script.

		pre_update.py [original_course_name] [incoming_course_name]

* You can then update the new description file by removing course sections or adding course sections from the incoming description files.
* After you are done, you run the update script, it will generate a new course file and zip it for you to upload to edX.

		update_course.py [original_course_name] [incoming_course_name]


<!-- repository = exported course.

1. Download and untar the two repositories.
2. Create a description file that describes each chapter/section/problem for each repository.
   Each line contains:
   * A readable description of the section, the path to the xml file in the repository (includin the repository name)
3. MANUAL: Using an editor, create a new description file that contains lines from either of the two original files.
   For example, I combined weeks 1-2 from CSE103 with weeks 3-9 of DSE210x
4 Create the new rpository based on the new description. One repository is considered the "origin" and the files that are not in the XML tree are taken from there. The xml files are taken from the incoming repository (we can have more than one). 
   1. Remove files that correspond to description lines of the original that have been removed.
   2. Copy new files from the incoming repositories. -->


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