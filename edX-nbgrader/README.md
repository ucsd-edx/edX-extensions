

# Installation:

Below is a list of everything that must be installed. Alternatively you can [use this docker image](https://hub.docker.com/r/pupster90/cse255-dse230/)

Install python 2.7 and install jupyter notebooks. After that, the only things left to install are a few jupyter extensions:


* [nbExtensions](https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator) is package that provides a gui in jupyter for installing other extensions
    * Conda Terminal Code:
    `conda install -c conda-forge jupyter_nbextensions_configurator`


* [these are some unofficial extensions](https://github.com/ipython-contrib/jupyter_contrib_nbextensions) added by the community
    * Conda Terminal Code: 
    
    `conda install -c conda-forge jupyter_contrib_nbextensions
jupyter contrib nbextension install --user`


* [nbGrader](https://github.com/jupyter/nbgrader/blob/master/nbgrader/docs/source/user_guide/installation.rst) is the extension we will use to create and grade assignments. Here is [nbGrader's documentation page](https://nbgrader.readthedocs.io/en/stable/)
    * Conda Terminal Code: `conda install -c conda-forge nbgrader`





# Create and Grade an Assignment

Now that everything is installed lets run a few terminal commands and check out what nbgrader does. Lets pretend that we want to create our first problem set, *"ps1",* for a course called, *"cse101"* :

    `nbgrader quickstart cse101`

This one line will create a template envirnonment for our course. Inside the temple you will see a directory called *source,* this is the directory where you create your problem sets for hte course. Notice that the quickstart command already created an example problem set called ps1. Please investigate this directory. When you are satisfied with *ps1* it is time to release the assignment to the students. *source/ps1* is only for teachers, *ps1* must be "compiled" into the version that is given to the students. This is done like this:

    `nbgrader assign ps1`

A new directory has been created called *release,* inside it there is also a folder called *ps1.* *release/ps1* is the version of the assignment that we give out to students. When a student submits a problem set it is put into a directory called *submitted.* Lets create a sample student submission:

```
mkdir submitted
mkdir submitted/hacker
cp -r release/ submitted/hacker/
```
In *submitted/hacker/ps1* you can view the submission of the students *hacker* for *ps1.* Take a look at some of *hackers* notebooks and try doing a few of the assignments. We can now try grading the problem assignment submitted in *subitted/hacker/ps1* :

    `nbgrader autograde ps1`

We have just graded *hackers ps1* assignment. *hackers* grade has been added to the database. Notice a new file appeared, *grades.db* . Also, there is a new directory *autograded* which contains the student notbook after it has been run for grading. However, if we want to view the student's notebook, there is another *nbgrader* function that produces and *.html* version of the notebook with a user's summary:

    `nbgrader feedback ps1`

A directory called *feedback* has been created. Try viewing the feedback that *hacker* got on *ps1* .






# Starting XQueu Watcher:
To start:
  1. `cd xqueue-watcher`
  2. `python -m xqueue-watcher -d .`


