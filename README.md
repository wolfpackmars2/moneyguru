# moneyGuru

[moneyGuru][moneyguru] is a personal finance management application. With it, you can evaluate your
financial situation so you can make informed (and thus better) decisions. Most finance applications
have the same goal, but moneyGuru's difference is in the way it achieves it. Rather than having
reports which you have to configure (or find out which pre-configured report is the right one), your
important financial data (net worth, profit) is constantly up-to-date and "in your face". This
allows you to constantly make informed decision rather than doing so periodically.

# Current status: People wanted

moneyGuru has currently only one maintainer, me. This is a dangerous situation that needs to be
corrected.

The goal is to eventually have another active maintainer, but before we can get there, the project
needs more contributors.

Whatever your skills, if you are remotely interestested in being a contributor, I'm interested in
mentoring you. If that's the case, please refer to [the open ticket on the subject][contrib-issue]
and let's get started.

## Windows maintainer wanted

As [described on my website][nowindows], v2.9.x serie of moneyGuru is the last one to support
Windows unless someone steps up to maintain it. If you're a Windows developer and are interested
in taking this task, [don't hesitate to let me know][contrib-issue].

## OS X maintainer wanted

My Mac Mini is already a couple of years old and is likely to be my last Apple purchase. When it
dies, I will be unable maintain the OS X version of moneyGuru. I've already stopped paying for the
Mac Developer membership so I can't sign the apps anymore (in the "official way" I mean. The
download is still PGP signed) If you're a Mac developer and are interested in taking this task,
[don't hesitate to let me know][contrib-issue].

# Contents of this folder

This package contains the source for moneyGuru. Its documentation is
[available online][documentation]. Here's how this source tree is organised:

* core: Contains the core logic code for moneyGuru. It's Python code.
* cocoa: UI code for the Cocoa toolkit. It's Objective-C code.
* qt: UI code for the Qt toolkit. It's written in Python and uses PyQt.
* images: Images used by the different UI codebases.
* debian: Skeleton files required to create a .deb package.
* help: Help document, written for [Sphinx][sphinx].
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

* All systems: [Python 3.4+][python]
* Mac OS X: 10.7+ with XCode command line tools and a "framework enabled" Python (see below)
* Windows: Visual Studio 2010, [PyQt 5.4+][pyqt], [cx_Freeze][cxfreeze] and
  [Advanced Installer][advinst] (you only need the last two if you want to create an installer)

On Ubuntu, the apt-get command to install all pre-requisites is:

    $ apt-get install python3-dev python3-venv python3-pyqt5 pyqt5-dev-tools

On Arch, it's:

    $ pacman -S python-pyqt5

On OS X, an easy way to install a "framework enabled" Python 3 is through [pyenv][pyenv]. Once
pyenv in installed, run a command like:

    env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.5.1

## Setting up the virtual environment

Use Python's built-in `pyvenv` to create a virtual environment in which we're going to install our
Python-related dependencies.

    $ pyvenv --system-site-packages env
    $ source env/bin/activate
    $ pip install -r requirements-[osx|win].txt

([osx|win] depends, of course, on your platform. On other platforms, just use requirements.txt).

## Actual building and running

With your virtualenv activated, you can build and run moneyGuru with these commands:

    $ python build.py
    $ python run.py

You can also package moneyGuru into an installable package with:
    
    $ python package.py

# Running tests

The complete test suite is ran with [Tox 1.7+][tox]. If you have it installed system-wide, you
don't even need to set up a virtualenv. Just `cd` into the root project folder and run `tox`.

If you don't have Tox system-wide, install it in your virtualenv with `pip install tox` and then
run `tox`.

You can also run automated tests without Tox. Extra requirements for running tests are in
`requirements-tests.txt`. So, you can do `pip install -r requirements-tests.txt` inside your
virtualenv and then `py.test core hscommon`

# Further documentation

For further development-related documentation, there's a "moneyGuru Developer Documentation"
section in the english version of the main documentation. This documentation is built with the app
and is also [available online][documentation].

[moneyguru]: http://www.hardcoded.net/moneyguru/
[contrib-issue]: https://github.com/hsoft/moneyguru/issues/425
[nowindows]: https://www.hardcoded.net/archive2015#2015-11-01
[documentation]: http://www.hardcoded.net/moneyguru/help/en/
[python]: http://www.python.org/
[pyenv]: https://github.com/yyuu/pyenv
[pyqt]: http://www.riverbankcomputing.com
[cxfreeze]: http://cx-freeze.sourceforge.net/
[advinst]: http://www.advancedinstaller.com
[sphinx]: http://sphinx.pocoo.org/
[tox]: https://tox.readthedocs.org/en/latest/

