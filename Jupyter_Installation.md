## How to install jupyter notebook and it's extensions

### Installing Jupyter
We highly recommend using anaconda (conda) installation. Directions are available 
* here: http://jupyter.readthedocs.io/en/latest/install.html
* and here: https://mas-dse.github.io/startup/

### Installing Extensions to jupyter

from https://github.com/ipython-contrib/jupyter_contrib_nbextensions
```
conda install -c conda-forge jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

from https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator
```
conda install -c conda-forge jupyter_nbextensions_configurator
```

### nbgrader:

from: https://github.com/jupyter/nbgrader/blob/master/nbgrader/docs/source/user_guide/installation.rst

conda install -c conda-forge nbgrader

### rise

from: https://github.com/damianavila/RISE

```
conda install -c damianavila82 rise
```
