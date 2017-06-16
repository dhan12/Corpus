#!/bin/bash
echo "start"


function start_virtualenv {
    virtualenv venv
    . venv/bin/activate
}

function stop_virtualenv {
    deactivate
}

# Check arguments
if [[ $# -gt 0 ]]; then
    if [[ "$1" = "install" ]]; then
        echo "Will install packages"
        start_virtualenv
        pip install pytest
        pip install pep8
        pip install autopep8
    elif [[ "$1" = "autopep8" ]]; then
        echo "Will run autopep8"
        start_virtualenv
        autopep8 --in-place *.py tests/*.py
    else
        echo "Unknown argument: $1"
    fi

    stop_virtualenv
    exit
fi


#
# Unit tests
#
start_virtualenv
python -m pytest -s tests
rc=$?

#
# Do some style checks
#
if [ $rc -eq 0 ]; then
    venv/bin/pep8 *.py tests
    rc=$?
fi


stop_virtualenv

exit $rc
