pygeda
******

This project is in the very first development phase. You may not want to
clone it.

Pygeda is a collection of missing scripts to manipulate gEDA-gaf files.

gEDA is an open-source electronic design automation toolchain for schematic
and layout design. Pygeda adds functionality like unique IDs for components,
advanced device enumeration and incremental layout updates on schematic
changes. 

Pygeda doesn't change or reuse code of the gEDA projects, it only parses
and manipulates schematic and layout files.


Installation
============

Pygeda is installed as a Python2 package and can be installed using the
python setup tools::

    python setup.py install

Dependencies
------------

* cmdparse `https://github.com/markushutzler/cmdparse`
* gEDA


Commands
========

Pygeda comes with a set of commands::

    pygeda [cmd]

path
----

Print information about project pathes and applications.

stat
----

Print statistics of schematic files. This command is used for parser
testing and debugging the python library.

unique
------

Check all components for unique IDs and add or replace IDs for new or
dublicate components.


License
=======

GPL3