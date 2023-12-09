Localization
============
RetroArcher is being localized into various languages. The default language is `en` (English).

.. image:: https://app.lizardbyte.dev/uno/crowdin/LizardByte_graph.svg

CrowdIn
-------
The translations occur on
`CrowdIn <https://crowdin.com/project/lizardbyte>`__. Feel free to contribute to localization there.
Only elements of the interface are planned to be translated.

Translations Basics
   - The brand name `LizardByte` should never be translated.
   - The project name `RetroArcher` should never be translated.
   - Other brand and project names should never be translated.
     Examples:

     - CEMU
     - GitHub
     - Linux
     - MacOS
     - RetroArch
     - RPCS3
     - Sunshine
     - Windows

**CrowdIn Integration**
   How does it work?

   When a change is made to retroarcher python source or web templates, a workflow generates new translation templates
   that get pushed to CrowdIn automatically.

   When translations are updated on CrowdIn, a push gets made to the `l10n_master` branch and a PR is made against the
   `master` branch. Once PR is merged, all updated translations are part of the project and will be included in the
   next release.

Extraction
----------
There should be minimal cases where strings need to be extracted from python code; however it may be necessary in some
situations. For example the system tray icon is user interfacing and therefore should have strings extracted.

- In order for strings to be extracted from python code, the following lines must be added.
   .. code-block:: python

      from pyra import locales
      _ = locales.get_text()

- Wrap the string to be extracted in a function as shown.
   .. code-block:: python

      _('Hello world!')

- In order to include a name that should not be translated, the following example should be used.
   .. code-block:: python

      _('Open %(app_name)s') % {'app_name': 'RetroArcher'}

While strings are to be rarely extracted from python code, it is common for strings to be extracted from html. The
extraction method from html templates is very similar to extracting from python code.

- This is a simple `Hello world` example.
   .. code-block:: html

      {{ _('Hello world!') }}

- No other code needs to be added to html templates.

.. Warning:: This is for information only. Contributors should never include manually updated template files, or
   manually compiled language files in Pull Requests.

Strings are automatically extracted from the code to the `locale/retroarcher.po` template file. The generated file is
used by CrowdIn to generate language specific template files. The file is generated using the
`.github/workflows/localize.yml` workflow and is run on any push event into the `master` branch. Jobs are only run if
any of the following paths are modified.

.. code-block:: yaml

   - 'retroarcher.py'
   - 'pyra/**.py'
   - 'web/templates/**'

When testing locally it may be desirable to manually extract, initialize, update, and compile strings.

**Extract, initialize, and update**
   .. code-block:: bash

      python ./scripts/_locale.py --extract --init --update

**Compile**
   .. code-block:: bash

      python ./scripts/_locale.py --compile
