#!/bin/bash

PYTHON=python3
ret=`$PYTHON -c "import sys; print(int(sys.version_info[:2] >= (3, 4)))"`
if [ $ret -ne 1 ]; then
    echo "Python 3.4+ required. Aborting."
    exit 1
fi

if [ ! -d "env" ]; then
    echo "No virtualenv. Creating one"
    if ! $PYTHON -m venv env ; then
        echo "Creation of our virtualenv failed. If you're on Ubuntu, you probably need python3-venv."
        exit 1
    fi
    if [ -f "requirements.freeze" ]; then
        # We're in a "frozen" (packaged) source environment. We should use the exact same deps
        # as those used at freeze time. Moreover, this needs to happen *before* we go in
        # system-site-packages mode so that globally-installed packages don't interfere.
        ./env/bin/pip install -r requirements.freeze
    fi
    if [ "$(uname)" != "Darwin" ]; then
        # We only need system site packages for PyQt, so under OS X, we don't enable it
        $PYTHON -m venv env --upgrade --system-site-packages
    fi
fi

echo "Installing pip requirements"
if [ "$(uname)" == "Darwin" ]; then
    ./env/bin/pip install -r requirements-osx.txt
else
    ./env/bin/python -c "import PyQt5" >/dev/null 2>&1 || { echo >&2 "PyQt 5.4+ required. Install it and try again. Aborting"; exit 1; }
    ./env/bin/pip install -r requirements.txt
fi

echo "Bootstrapping complete! You can now configure, build and run moneyGuru with:"
echo ". env/bin/activate && python build.py && python run.py"

