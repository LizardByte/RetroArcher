Overview
========

About
-----
RetroArcher is a game streaming server application. This project is under development and nowhere near ready for use.

Integrations
------------

.. image:: https://img.shields.io/github/workflow/status/retroarcher/retroarcher/CI/master?label=CI%20build&logo=github&style=for-the-badge
   :alt: GitHub Workflow Status (CI)
   :target: https://github.com/RetroArcher/RetroArcher/actions/workflows/CI.yml?query=branch%3Amaster

.. image:: https://img.shields.io/github/workflow/status/retroarcher/retroarcher/localize/nightly?label=localize%20build&logo=github&style=for-the-badge
   :alt: GitHub Workflow Status (localize)
   :target: https://github.com/RetroArcher/RetroArcher/actions/workflows/localize.yml?query=branch%3Anightly

.. image:: https://img.shields.io/readthedocs/retroarcher?label=Docs&style=for-the-badge&logo=readthedocs
   :alt: Read the Docs
   :target: http://retroarcher.readthedocs.io/

.. image:: https://img.shields.io/badge/dynamic/json?color=blue&label=localized&style=for-the-badge&query=%24.progress..data.translationProgress&url=https%3A%2F%2Fbadges.awesome-crowdin.com%2Fstats-15178612-503340.json&logo=crowdin
   :alt: CrowdIn
   :target: https://crowdin.com/project/retroarcher

Support
---------

Our support methods are listed in our
`LizardByte Docs <https://lizardbyte.readthedocs.io/en/latest/about/support.html>`_.

Downloads
---------

.. image:: https://img.shields.io/github/downloads/lizardbyte/retroarcher/total?style=for-the-badge&logo=github
   :alt: GitHub Releases
   :target: https://github.com/LizardByte/RetroArcher/releases/latest

.. image:: https://img.shields.io/docker/pulls/lizardbyte/retroarcher?style=for-the-badge&logo=docker
   :alt: Docker
   :target: https://hub.docker.com/r/lizardbyte/retroarcher

Stats
------
.. image:: https://img.shields.io/github/stars/lizardbyte/retroarcher?logo=github&style=for-the-badge
   :alt: GitHub stars
   :target: https://github.com/LizardByte/RetroArcher

Project Goals
-------------

Plugin Framework
   Develop a framework friendly to plugins that allows easy expansion of the application.

   Plugin types may be:

   - Game Stream Hosts (`Sunshine`_, `GeForce Experience`_, etc.)
   - Clients (Android, AppleTV, iOS, PC [Linux, MacOS, Windows], Xbox One/Series S/X, etc.)
   - Emulators (`Cemu`_, `RetroArch`_, `RPCS3`_, etc.)
   - Game Stores (`Epic Games`_, `Steam`_, `Microsoft Store`_, etc.)
   - Consoles (game streaming Xbox One/Series S/X, PS4/5, etc.)
   - Media Servers (`Emby`_, `Jellyfin`_, `Kodi`_, `Plex`_, etc.)
   - Misc. (anything that doesn't fit a category above)

Replace Existing RetroArcher.bundle
   `RetroArcher.bundle`_ will still remain; however it will significantly change. In the future it will:

   - No longer be responsible for scanning games
   - No longer be responsible for connecting to clients
   - No longer be responsible for starting games
   - No longer get metadata from IGDB
   - Make an API request to this self-hosted server to get metadata

.. _Sunshine: https://app.lizardbyte.dev/
.. _GeForce Experience: https://www.nvidia.com/en-us/support/gamestream/
.. _Cemu: https://cemu.info/
.. _RetroArch: https://www.retroarch.com/
.. _RPCS3: https://rpcs3.net/
.. _Epic Games: https://www.epicgames.com/
.. _Steam: https://store.steampowered.com/
.. _Microsoft Store: https://www.microsoft.com/store/games/windows
.. _Emby: https://emby.media/
.. _Jellyfin: https://jellyfin.org/
.. _Kodi: https://kodi.tv/
.. _Plex: https://www.plex.tv/
.. _RetroArcher.bundle: https://github.com/RetroArcher/RetroArcher.bundle
