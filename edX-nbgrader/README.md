

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




# Starting XQueu Watcher:
To start:
  1. `cd xqueue-watcher`
  2. `python -m xqueue-watcher -d .`


