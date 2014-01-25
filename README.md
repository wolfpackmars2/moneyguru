# moneyGuru

[moneyGuru][moneyguru] is a personal finance management application. With it, you can evaluate your
financial situation so you can make informed (and thus better) decisions. Most finance applications
have the same goal, but moneyGuru's difference is in the way it achieves it. Rather than having
reports which you have to configure (or find out which pre-configured report is the right one), your
important financial data (net worth, profit) is constantly up-to-date and "in your face". This
allows you to constantly make informed decision rather than doing so periodically.

# Contents of this folder

This package contains the source for moneyGuru. Its documentation is
[available online][documentation]. Here's how this source tree is organised:

* core: Contains the core logic code for moneyGuru. It's Python code.
* cocoa: UI code for the Cocoa toolkit. It's Objective-C code.
* qt: UI code for the Qt toolkit. It's written in Python and uses PyQt.
* images: Images used by the different UI codebases.
* debian: Skeleton files required to create a .deb package.
* help: Help document, written for Sphinx.
* locale: .po files for localisation.

There are also other sub-folder that comes from external repositories and are part of this repo as
git subtrees:

* hscommon: A collection of helpers used across HS applications.
* cocoalib: A collection of helpers used across Cocoa UI codebases of HS applications.
* qtlib: A collection of helpers used across Qt UI codebases of HS applications.
* ambuttonbar: Cocoa library to display filter buttons.
* psmtabbarcontrol: Cocoa library for tabs.

# How to build moneyGuru from source

## The very, very, very easy way

If you're on Linux or Mac, there's a bootstrap script that will make building very, very easy. There
might be some things that you need to install manually on your system, but the bootstrap script will
tell you when what you need to install. You can run the bootstrap with:

    ./bootstrap.sh

and follow instructions from the script. You can then ignore the rest of the build documentation.

## Prerequisites installation

Then, you have to make sure that your system has its "non-pip-installable" prerequisites installed:

* All systems: [Python 3.3+][python]
* Mac OS X: The last XCode to have the 10.6 SDK included.
* Windows: Visual Studio 2010, [PyQt 4.7+][pyqt], [cx_Freeze][cxfreeze] and
  [Advanced Installer][advinst] (you only need the last two if you want to create an installer)

On Ubuntu, the apt-get command to install all pre-requisites is:

    $ apt-get install python3-dev python3-pyqt4 pyqt4-dev-tools python3-setuptools

On Arch, it's:

    $ pacman -S python-pyqt5

## Setting up the virtual environment

Use Python's built-in `pyvenv` to create a virtual environment in which we're going to install our
Python-related dependencies. `pyvenv` is built-in Python but, unlike its `virtualenv` predecessor,
it doesn't install setuptools and pip, so it has to be installed manually:

    $ pyvenv --system-site-packages env
    $ source env/bin/activate
    $ wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
    $ easy_install pip

Then, you can install pip requirements in your virtualenv:

    $ pip install -r requirements-[osx|win].txt
    
([osx|win] depends, of course, on your platform. On other platforms, just use requirements.txt).

## Actual building and running

With your virtualenv activated, you can build and run moneyGuru with these commands:

    $ python configure.py
    $ python build.py
    $ python run.py

You can also package moneyGuru into an installable package with:
    
    $ python package.py

# Further documentation

There's a more complete development documention in 'devdoc'. This documentation has to be built
using [Sphinx][sphinx]. This documentation is also [available online][devdocs].

[moneyguru]: http://www.hardcoded.net/moneyguru/
[documentation]: http://www.hardcoded.net/moneyguru/help/en/
[python]: http://www.python.org/
[pyqt]: http://www.riverbankcomputing.com
[cxfreeze]: http://cx-freeze.sourceforge.net/
[advinst]: http://www.advancedinstaller.com
[sphinx]: http://sphinx.pocoo.org/
[devdocs]: http://www.hardcoded.net/docs/moneyguru/
[polib]: https://bitbucket.org/izi/polib/issue/42
