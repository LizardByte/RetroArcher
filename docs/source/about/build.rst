Build
=====
RetroArcher binaries are built using `pyinstaller <https://pypi.org/project/pyinstaller/>`_. Cross compilation is not
supported. That means the binaries must be built on the target operating system and architecture.

Use Python 3.7+

Clone
-----
Ensure `git <https://git-scm.com/>`_ is installed and run the following:
   .. code-block:: bash

      git clone https://github.com/lizardbyte/retroarcher.git
      cd ./retroarcher

Setup venv
----------
It is recommended to setup and activate a `venv`_ within the `retroarcher` directory.

Install Python Requirements
---------------------------
**Standard Requirements**
   .. code-block:: bash

      python -m pip install -r requirements.txt

**Advanced Requirements**
   Required for:
      - :ref:`Test with flake8 <contributing/testing:flake8>`
      - :ref:`Test with pytest <contributing/testing:pytest>`
      - :ref:`Compiling binaries <about/build:compile binary>`

   .. code-block:: bash

      python -m pip install -r requirements-dev.txt

   .. Tip:: Advanced requirements include all of the standard dependencies contained in the `requirements.txt`

Compile Locales
---------------
.. code-block:: bash

   python ./scripts/_locale.py --compile

Install NPM Requirements
------------------------
.. code-block:: bash

      npm install
      mv -f ./node_modules/ ./web/

Compile Docs
------------
Docs are visible by the webapp and therefore must be compiled.

.. code-block:: bash

   cd docs
   make html
   cd ..

Compile Binary
--------------
.. code-block:: bash

   python ./scripts/build.py

Remote Build
------------
It may be beneficial to build remotely in some cases. This will enable easier building on different operating systems.

#. Fork the project
#. Activate workflows
#. Trigger the `CI` workflow manually
#. Download the artifacts/binaries from the workflow run summary

.. _venv: https://docs.python.org/3/library/venv.html
