## Plan

This is the plan for working on software to support the problem sets on edX. The developmental work will be done against the problem set created for CSE103 and would involve making improvements to the problem set as well.

### General 

1. All of the code has to be factored into classes/methods that have an easy to understand public API.
2. All public parts of the code must have detailed in-code documentation using [Sphinx](http://www.sphinx-doc.org/en/stable/contents.html)
   * If you are using emacs, I recommend [sphinx-doc](http://sphinx-doc.org/index.html) that add a sphinx-mode to the editor. this mode is helpful for writing well formatte4d docstrings.
   * Once sphinx is installed and configured, it takes a single command to traverse a code repository and generate out of it a documentation web site such as [ReadTheDocs](http://docs.readthedocs.io/en/latest/getting_started.html)
3. In addition to the code documentation, which is intended for programmers, there should be documentation describing how to write problems.

### The `imd` format
