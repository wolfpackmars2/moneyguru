======================
How to build moneyGuru
======================

Dependencies
============

Before being able to build moneyGuru, a few "non-pip-installable" dependencies have to be installed:

* All systems: Python 3.3+
* Mac OS X: The last XCode to have the 10.6 SDK included.
* Windows: Visual Studio 2010, PyQt 4.7+, cx_Freeze and Advanced Installer (you only need the last
  two if you want to create an installer)

On Ubuntu, the apt-get command to install all pre-requisites is:

    $ apt-get install python3-dev python3-pyqt4 pyqt4-dev-tools

On Arch, it's:

    $ pacman -S python-pyqt4

Setting up the virtual environment
==================================

Use Python's built-in ``pyvenv`` to create a virtual environment in which we're going to install our
Python-related dependencies. ``pyvenv`` is built-in Python but, unlike its ``virtualenv``
predecessor, it doesn't install setuptools and pip, so it has to be installed manually::

    $ pyvenv --system-site-packages env
    $ source env/bin/activate
    $ wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
    $ easy_install pip

Then, you can install pip requirements in your virtualenv::

    $ pip install -r requirements-[osx|win].txt
    
[osx|win] depends on your platform. On Linux, run the base requirements file, requirements.txt.
Sparkle and Advanced Installer, having nothing to do with Python, have to be manually installed.

PyQt isn't in the requirements file either (there's no package uploaded on PyPI) and you also have
to install it manually.

Building moneyGuru
==================

First, make sure you meet the dependencies listed in the section above. Then you need to configure
your build with::

	python configure.py
	
If you want, you can specify a UI to use with the ``--ui`` option. So, if you want to build moneyGuru with Qt on OS X, then you have to type ``python configure.py --ui=qt``. You can also use the ``--dev`` flag to indicate a dev build.

Then, just build the thing and then run it with::

	python build.py
	python run.py

If you want to create ready-to-upload package, run::

	python package.py
