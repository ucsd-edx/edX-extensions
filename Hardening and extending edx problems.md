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
  1. **Python symbol intrpolation** : are replaced by the values of variables defined in the python code. i.e. "you are given \$n_balls balls" will be replaced by "you are given 5 balls" if `n_balls=5`
  2. **Answer boxes** : regions of the problem where the student is to type his/her answer. Each answer box is associated with a correct answer, that can be fixed or can be an interpolated variable.
3. **Answer checking code**: This code runs after the student submitted his/her answer. It compares the student's answer with the correct answer, tells the student whether the answer is correct, and potentially provides a hint. (At this point the hint will not be a question, just a sententence, possibly with some latex math.) 

### The `imd` format

The `.imd` format is an extension of the markdown `.md` format that we developed to add capabilities and make it easier to write problems. 

The format is designed to be used inside a jupyter notebooks (iPython - hence the `i` in `imd`). This allows the problem developer to work in a single environment when writing the python code and when writing the markdown for the problem, and to easily check the different parts.
