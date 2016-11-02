# QGRAF Diagram Drawer
## Dependencies
This code uses [QGRAF](http://cfif.ist.utl.pt/~paulo/qgraf.html) and [tikz-feynman](https://github.com/JP-Ellis/tikz-feynman)

## Use

The program *qgraf-xml-drawer* is a Python program for drawing Feynman diagrams. The code translates [QGRAF](http://cfif.ist.utl.pt/~paulo/qgraf.html) diagrams  into a *LuaLaTeX* file using [tikz-feynman](https://github.com/JP-Ellis/tikz-feynman) to draw them after compilation

#### QGRAF
The program is provided with a *QGRAF* style file called `xmldraw.sty`. Any set of feynman rules compatible with *QGRAF* can be handled and the output should be put in the package folder to be processed.
#### LuaLaTeX Generation
The user is required to modify the code to adapt it to their situation.
* The *QGRAF* output file name should be provided by modifying the variable `INPUTS` in the file `drawer.py`.
* The particle dictionnary `pt` in `drawer.py` should also be modified to contain the list of particles and anti-particles appearing in the diagrams. Each key in the dictionnary is the name of the particle as defined in *QGRAF* and the associated value should be the associated propagator type as defined in *tikz-feynman*.

Once this is defined, run the code using `python drawer.py` and compile the output using `lualatex main.tex`. The diagrams ared drawn in `main.pdf`.

## Citing

This code is citeable using the following DOI:

[![DOI](https://zenodo.org/badge/22973/ndeutschmann/qgraf-xml-drawer.svg)](https://zenodo.org/badge/latestdoi/22973/ndeutschmann/qgraf-xml-drawer)
