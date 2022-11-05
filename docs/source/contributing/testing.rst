Testing
=======

Flake8
------
RetroArcher uses `Flake8 <https://pypi.org/project/flake8/>`_ for enforcing consistent code styling. Flake is included
in the `requirements-dev.txt`.

The config file for flake8 is `.flake8`. This is already included in the root of the repo and should not be modified.

**Test with Flake8**
   .. code-block:: bash

      python -m flake8

Sphinx
------
RetroArcher uses `Sphinx <https://www.sphinx-doc.org/en/master/>`_ for documentation building. Sphinx is included
in the standard `requirements.txt` as building the docs is required for RetroArcher to be fully functional.

RetroArcher follows `numpydoc <https://numpydoc.readthedocs.io/en/latest/format.html>`_ styling and formatting in
docstrings. This will be tested when building the docs.

The config file for Sphinx is `docs/source/conf.py`. This is already included in the root of the repo and should not
be modified.

**Test with Sphinx**
   .. code-block:: bash

      cd docs
      make html

   Alternatively

   .. code-block:: bash

      cd docs
      sphinx-build -b html source build

pytest
------
RetroArcher uses `pytest <https://pypi.org/project/pytest/>`_ for unit testing. pytest is included in the
`requirements-dev.txt`.

No config is required for pytest.

Prior to running pytest you will need to:

- :ref:`compile docs <contributing/testing:sphinx>`
- :ref:`compile translations <about/build:compile locales>`

**Test with pytest**
   .. code-block:: bash

      python -m pytest
