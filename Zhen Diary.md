* 6/26
  1. Moved problems to CSE103-DSE210x repository.
  2. Moved md2xml to extension repository.
  3. Cleaned up code in md2xml.
  4. Added simple tutorial of md2xml.

* 6/27
  1. Fixed translate.py errors.
  2. Re-wrote imd tutorial.
  3. Cleaned up the repository further.
  4. Cleaned up the CSE103-DSE210x repository.

* 6/28
  1. Converted all .md files to .imd files in the CSE103-DSE210x repository.
  2. Moved HW files to the correct folder. Removed duplicate files.
  3. Updated readme files in CSE103-DSE210x repository.

* 6/29
  1. Re-wrote tutorial for CSE103-DSE210x repository.
  2. Translated .pg files to .imd files.

* 7/3
  Meeting

* 7/5
  Refactored translate.py based on discussion with Yoav.
  1. Splitted functions.
  2. Added doc string to functions.

* 7/6
  1. Read Matt's class definition.
  2. Moved codes in corresponding class functions.
  3. Finished doc string for each class function.

* 7/7
  Skype meeting with Matt.
  Started to work on the test function of the translator class.
  1. Found codes for parse trees and math expression evaluation.
  2. Moved codes to github and cleaned up the code.
  3. Added doc string.

* 7/10
  1. Found and refactor eval function.
  2. Made sure eval can be imported in translator class.
  3. Cleaned up translatorClass.py

* 7/11
  1. Added detail help function using argparse in translatorClass.py
  2. Finished implementing test function in translatorClass.py
    i. Added code to test py_code and test_code to make sure it compiles.
    ii. Made sure solution definition in py_code is executed after test_code.
    iii. Had both codes execute in scope and test the solution values.

* 7/12
  1. Implemented --selftest
  2. Added more test in example imd files.
  3. Added code to test problems with variables.

* 7/13
  Meeting with Matt:
  1. Talked about the structure of the translator class.
  2. Talked about how test work.
  3. Talked about ideas of rendering HTML.

* 7/14
  1. Discuss code in translate.py. What format will the solutions be?

    Two options:
    (i) Have instructors write "solution1", "solution2", etc.
    (ii) Have instructors write "solutions = [{}.format(var1), {}.format(var2), ...]"

    Change code in translate.py correspondingly.

  2. Removed the json from translator
  3. Allow to input direct path to the file that need to be translated.
  4. XML will save in the same dir as imd files.
