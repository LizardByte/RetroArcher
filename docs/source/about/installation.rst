:github_url: https://github.com/RetroArcher/RetroArcher/tree/nightly/docs/source/about/installation.rst

Installation
============
The recommended method for running RetroArcher is to use the `binaries`_ bundled with the `latest release`_.

Binaries
--------
Binaries of RetroArcher are created for each release. They are available for Linux, MacOS, and Windows.
Binaries can be found in the `latest release`_.

Docker
------
Docker images are available on `Dockerhub.io`_ and `ghcr.io`_.

See :ref:`Docker <about/docker:docker>` for additional information.

Source
------
.. Caution:: Installing from source is not recommended most users.

#. Follow the steps in :ref:`Build <about/build:build>` except for :ref:`Compile Binary <about/build:compile binary>`.
#. Run the following within your activated venv.

   .. code-block:: bash

      python retroarcher.py

.. _latest release: https://github.com/RetroArcher/RetroArcher/releases/latest
.. _Dockerhub.io: https://hub.docker.com/repository/docker/retroarcher/retroarcher
.. _ghcr.io: https://github.com/orgs/RetroArcher/packages?repo_name=retroarcher
