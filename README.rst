=======
pomerge
=======


.. image:: https://img.shields.io/pypi/v/pomerge.svg
        :target: https://pypi.python.org/pypi/pomerge

Script to merge translations from a set of po files to other set of po files.

``pomerge`` does not care about ``.po`` file names, a translation
from one file can land in another as long as their ``msgid`` are identical.


Usage
-----

Basic usage is ``pomerge --from source.po --to dest.po``, see
``pomerge --help`` for more.

``--from`` and ``--to`` are optional, when not given, pomerge will use
a temporay file. So::

    pomerge --from a/**/*.po --to b/**/*.po

is strictly equivalent to::

    pomerge --from a/**/*.po
    pomerge --to b/**/*.po


The wrapping of your ``.po`` files is not kept by ``pomerge``,
completly destroying the readability of git diffs, to fix this I use
`poindent <https://pypi.python.org/pypi/poindent>`_.


Recipes
-------

Propagating translations from a directory to another
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you're having two directories with ``.po`` files and want to copy
translations (``msgstr``) from one to another, even if the hiearchy is
not the same, run::

    pomerge --from ../contributors/**/*.po --to **/*.po

In this case, two options can be useful:

- ``--no-overwrite``: Avoid touching already translated strings.
- ``--mark-as-fuzzy``: Mark all new translations as fuzzy, usefull
  when you know you'll have to proofread the translations.


Propagating known translations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In big projects, there may be multiple occurrences of the same string
in different ``.po`` files, to automatically fill blanks with already
translated ones, use::

    pomerge --no-overwrite --from **/*.po --to **/*.po

The ``--no-overwrite`` is usefull if the same ``msgstr`` has already
been translated twice, but differently (depending on the context
maybe), the ``--no-overwrite`` will prevent one to be overwritten by
the other.


Synchronizing translation between git branches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you're having multiple branches of your documentation to track
multiple branches of your project, you may want to synchronize known
translations between branches, you can do it like this::

    git checkout master  # The place where your contributors work
    pomerge --from **/*.po  # Make pomerge "learn" this set of translations
    git checkout old_version  # The translation for an old branch
    pomerge --to **/*.po

This way you can still make old translation progress a bit while
focusing only on the current master.
