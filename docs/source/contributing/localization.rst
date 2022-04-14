:github_url: https://github.com/RetroArcher/RetroArcher/tree/nightly/docs/source/contributing/localization.rst

Localization
============
RetroArcher is being localized into various languages. The default language is `en` (English) and is highlighted green.

.. image:: https://img.shields.io/badge/dynamic/json?color=blue&label=de&style=for-the-badge&query=%24.progress.0.data.translationProgress&url=https%3A%2F%2Fbadges.awesome-crowdin.com%2Fstats-15178612-503340.json
.. image:: https://img.shields.io/badge/dynamic/json?color=green&label=en&style=for-the-badge&query=%24.progress.1.data.translationProgress&url=https%3A%2F%2Fbadges.awesome-crowdin.com%2Fstats-15178612-503340.json
.. image:: https://img.shields.io/badge/dynamic/json?color=blue&label=en-GB&style=for-the-badge&query=%24.progress.2.data.translationProgress&url=https%3A%2F%2Fbadges.awesome-crowdin.com%2Fstats-15178612-503340.json
.. image:: https://img.shields.io/badge/dynamic/json?color=blue&label=en-US&style=for-the-badge&query=%24.progress.3.data.translationProgress&url=https%3A%2F%2Fbadges.awesome-crowdin.com%2Fstats-15178612-503340.json
.. image:: https://img.shields.io/badge/dynamic/json?color=blue&label=es-ES&style=for-the-badge&query=%24.progress.4.data.translationProgress&url=https%3A%2F%2Fbadges.awesome-crowdin.com%2Fstats-15178612-503340.json
.. image:: https://img.shields.io/badge/dynamic/json?color=blue&label=fr&style=for-the-badge&query=%24.progress.5.data.translationProgress&url=https%3A%2F%2Fbadges.awesome-crowdin.com%2Fstats-15178612-503340.json
.. image:: https://img.shields.io/badge/dynamic/json?color=blue&label=it&style=for-the-badge&query=%24.progress.6.data.translationProgress&url=https%3A%2F%2Fbadges.awesome-crowdin.com%2Fstats-15178612-503340.json
.. image:: https://img.shields.io/badge/dynamic/json?color=blue&label=ru&style=for-the-badge&query=%24.progress.7.data.translationProgress&url=https%3A%2F%2Fbadges.awesome-crowdin.com%2Fstats-15178612-503340.json
.. image:: https://badges.awesome-crowdin.com/translation-15178612-503340.png

CrowdIn
-------
The translations occur on
`CrowdIn <https://crowdin.com/project/retroarcher>`_. Feel free to contribute to localization there.
Only elements of the interface are planned to be translated.

Translations Basics
   - The brand name `RetroArcher` should never be translated.
   - Other brand names should never be translated.
     Examples: RetroArch, CEMU, RPCS3, Windows, Linux, MacOS

CrowdIn Integration
   How does it work?

   When a change is made to retroarcher python source or web templates, workflow generates new translation templates
   that get pushed to CrowdIn automatically.

   When translations are updated on CrowdIn, a push gets made to the `l10n_nightly` branch and a PR is made against the
   `nightly` branch. Once PR is merged, all updated translations are part of the project and will be included in the
   next release.
