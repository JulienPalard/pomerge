=======
pomerge
=======


.. image:: https://img.shields.io/pypi/v/pomerge.svg
        :target: https://pypi.python.org/pypi/pomerge

Script to merge translations from a set of po files to other set of po files.


Usage
-----

To merge translations from contributors to your files::

    pomerge --from ../contributors/*.po ../contributors/**/*.po --to *.po **/*.po

To merge translations from inside a single repository, usefull when simple
strings can appear in multiple .po files::

    pomerge --from *.po **.*.po --to *.po **/*.po

Note that ``pomerge`` does not care about po file names, a translation
from one file can land in another as long as their msgid are identical.


The style in your ``.po`` files may change a lot, completly destroying
the readability of git diffs, to fix this I use
`poindent <https://pypi.python.org/pypi/poindent>`_.


* Free software: MIT license
