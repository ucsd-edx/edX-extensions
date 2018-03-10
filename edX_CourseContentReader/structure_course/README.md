## Structuring Edx Courses

This folder contains scripts to convert an exported Edx course to a heirarchical file structure, as well as converting the course back to the original format.

In order to run this script, you will need to set up your environment first:


**Note:**
The current version of this program does not allow for adding new files to a course. You can make changes to the existing files, but any additional files will be lost during this process if added.

### 1. Setup

Change to the directory containing this read me and run the following command from your terminal:
```
source setup.sh

```

(If you want this setup script to run automatically, add a line to your .bashrc)

### 2. Download course files
* Export the course you would like to structure from edx using the instructions found [here](http://edx.readthedocs.io/projects/edx-partner-course-staff/en/latest/releasing_course/export_import_course.html)

* Unpack the exported course to a folder.

### 3. Create a new course structure

**Note:**
You need to have Python2 in order to run this script.

Run the following command from your terminal:

```
storeInMemory.py -c <unpacked_course_folder>
```

This will generate a new folder called `<unpacked_course_folder>_structured` with a new heirarchy for the course. 


When you are ready to package your course back up for uploading to edX, you can run the following command:


```
storeInMemory.py -c <structured_course_folder> -p True
```

This will place the packed course folder into a folder by the original name of the course, or if a folder of that name already exists, it will add a number on the end, i.e. `course_1`.

## Configuration options

The following table shows the various configuration options when running `storeInMemory.py`:


| Option Description                                                                                                            | Option | Argument options (Case sensitive)          | Default Value                                                                                                                                              | Required |
|-------------------------------------------------------------------------------------------------------------------------------|--------|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| Package Course                                                                                                                | `-p`   | True, False                                | False                                                                                                                                                      | No       |
| Course Folder                                                                                                                 | `-c`   | Valid Edx course folder path               | None                                                                                                                                                       | Yes      |
| Destination Folder                                                                                                            | `-dst` | Valid name of folder desired to be created | If package course is False, it will use '<course folder>_structured', otherwise it will use the original folder name from which the course was structured. | No       |
| Compress course folder (only valid when package course is true)                                                               | `-cmp` | True, False                                | False                                                                                                                                                      | No       |
| Keep original course folder copy when package course is false                                                                 | `-d`   | True, False                                | True                                                                                                                                                       | No       |
| If the original course folder is available, outputs the files included in the newly generated course and the previous course. | `-ver` | True, False                                | False                                                                                                                                                      | No       |
