#!/bin/bash
echo "start"

virtualenv venv
. venv/bin/activate

#
# Unit tests
#
pip install pytest
python -m pytest tests
rc=$?

#
# Do some style checks
#
if [ $rc -eq 0 ]; then
    pip install pep8
    venv/bin/pep8 *.py tests
    rc=$?
fi

if [ 0 -eq 1 ]; then
    pip install autopep8
    autopep8 --in-place *.py tests/*.py
fi

deactivate

exit $rc
