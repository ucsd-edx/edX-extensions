## Plan

This is the plan for working on software to support the problem sets on edX. The developmental work will be done against the problem set created for CSE103 and would involve making improvements to the problem set as well.

### General 

1. All of the code has to be factored into classes/methods that have an easy to understand public API.
2. All public parts of the code must have detailed in-code documentation using [Sphinx](http://www.sphinx-doc.org/en/stable/contents.html)
   * If you are using emacs, I recommend [sphinx-doc](http://sphinx-doc.org/index.html) that add a sphinx-mode to the editor. this mode is helpful for writing well formatte4d docstrings.
   * Once sphinx is installed and configured, it takes a single command to traverse a code repository and generate out of it a documentation web site such as [ReadTheDocs](http://docs.readthedocs.io/en/latest/getting_started.html)
3. In addition to the code documentation, which is intended for programmers, there should be documentation describing how to write problems.

### Anatomy of a problem

A problem definition file consists of the following elements:

1. **Python code** that gets executed right before the problem is presented to the student. This code typically creates different variants of the problem.
2. Markdown code that defines how the problem will be presented to the student. The markdown code include the following hooks to connect it with the rest of the system:
  1. **Python symbol interpolation** : are replaced by the values of variables defined in the python code. i.e. "you are given \$n_balls balls" will be replaced by "you are given 5 balls" if `n_balls=5`
  2. **Answer boxes** : regions of the problem where the student is to type his/her answer. Each answer box is associated with a correct answer, that can be fixed or can be an interpolated variable.
3. **Answer checking code**: This code runs after the student submitted his/her answer. It compares the student's answer with the correct answer, tells the student whether the answer is correct, and potentially provides a hint. (At this point the hint will not be a question, just a sententence, possibly with some latex math.) 

### Creating a problem

The steps, using the current methodology, are :

1. Write the problem in .imd
2. Generate an XML
3. Cut and paste the XML into the edX interface.

In the future, we want to create code that can take the exported course content, parse it to identify the location of the problem files, and change those files appropriately.

#### Importing and exporting course content from/to edx

* http://edx.readthedocs.io/projects/edx-partner-course-staff/en/latest/releasing_course/export_import_course.html

### The `imd` format

The `.imd` format is an extension of the markdown `.md` format that we developed to add capabilities and make it easier to write problems. 

The format is designed to be used inside a jupyter notebooks (iPython - hence the `i` in `imd`). This allows the problem developer to work in a single environment when writing the python code and when writing the markdown for the problem, and to easily check the different parts.

### The directories

Code that resides in different parts of different github repositories should be copied to appropriate parts of this repository.

#### List of current directories:

Put pointers to new locations one repositories have been copied:

1. Code for problems and problem translation is here. https://github.com/zhenzhai/TA_repo/tree/master/problem_database
2. Code for writing hints is here. https://github.com/zhenzhai/TA_repo/tree/master/hint_database
3. Answer checking code: https://github.com/zhenzhai/edx-platform/tree/master/common/lib/sandbox-packages/hint

Directories 1 and 2 contain both code and problem and hint definitions. The code should be put here, while the problem definition files should be put directories under the Probability and Statistics subdirectory.

###  Compatibility and division of work.

1. **Most urgent**: write documentation (not just a video) explaining how to write problems, check them, and load the to edX studio. This is critical because it allows others (Sanjoy, Alon and their students) to start writing and editing problem sets.

2. We plan to do varius improvements, some of which we do not know yet. It is important to keep backward compatibility with the current way in which problems are written, going back to change the problem definitions is error prone and a big pain.

3. 1 and 2 are somewhat in conflict with each other, if we do the documentation too soon, it will include various stange hacks (such as $,$$, \$$ all meaning different things) that make it hard to achieve backward compatibility. We should therefor have as a **First Step** 
to refactor the problem parsing code and make sure that it is clean, easy to explain, and easy to extend (We should use a standard markdown parser so that we can support images, sections etc.) . Then we write documentation, and then we start working on extending the capabilities. 

### Some specific problems:
* Varying the shape of the input box.
* Generating image variations: CDF

## Next steps:

1. Copy and organize directories.
2. Refactor the imd 2 xml compilation code (Use Markdown compiler, RE, PLY)
2. Refactor the definition / documentation of an `imd` file.
3. Write a tutorial on writing problems, with examples.

