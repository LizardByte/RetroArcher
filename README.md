# RetroArcher
RetroArcher is a game streaming server application. This project is under development and nowhere near ready for use.

Contributions would be very welcome! Please discuss with us on our Discord server.

## Usage
 - Create and activate a venv
     ```bash
     python -m pip install -r requirements.txt
     python retroarcher.py
     ```
 - Arguments:
     ```bash
     python retroarcher.py --help
     ``` 

## Build
RetroArcher binaries are built using [pyinstaller](https://pypi.org/project/pyinstaller/). Cross compilation is not
supported. That means the binaries must be built on the target architecture.

### Building locally
```bash
python -m pip install -r requirements-dev.txt
python ./scripts/build.py
```

### Building remotely
- Fork the project
- Activate workflows
- Trigger the `CI` workflow manually
- Download the artifacts/binaries from the workflow run summary

## Goals or RetroArcher
 - Develop a framework friendly to plugins that allows easy expansion of the application.
 - Plugin types may be:
   - Game Stream Hosts ([Sunshine](https://sunshinestream.github.io/),
     [GeForce Experience](https://www.nvidia.com/en-us/support/gamestream/), etc.)
     - Responsible for handling the streaming session 
   - Clients (Android, AppleTV, iOS, PC [Linux, MacOS, Windows], Xbox One/Series S/X, etc.)
     - Clients connect to the game stream host 
   - Emulators (Cemu, RetroArch, RPCS3, etc.)
   - Game Stores (Epic, Steam, Microsoft Store, etc.)
   - Consoles (game streaming Xbox One/Series S/X, PS4/5, etc.)
   - Media Servers (Emby, Jellyfin, Kodi, Plex, etc.)
   - Misc. (anything that doesn't fit a category above)
     - Other categories may be added
 - Replace RetroArcher.bundle in its current form
   - RetroArcher.bundle will still remain; however it will significantly change. In the future it will:
     - No longer be responsible for scanning games
     - No longer be responsible for connecting to clients
     - No longer be responsible for starting games
     - No longer get metadata from IGDB
     - Make an API request to this self-hosted server to get metadata

## Contributing
 - Fork the repo using GitHub
 - Clone the project to your local machine
 - Create a new branch for the feature you are adding or the issue you are fixing (base the new branch off `nightly`)
 - Create and activate a venv
 - `pip install -r requirements.txt`
 - Make changes, push commits, etc.
   - Follow [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).
 - When ready create a PR to this repo on the `nightly` branch
   - If you accidentally make your PR against a different branch, a bot will comment letting you know it's on the wrong 
     branch. Don't worry. You can edit the PR to change the target branch, no reason to close the PR!
   - Draft PRs are also welcome as you work through issues. The benefit of creating a draft PR is that an automated
     build can run in a github runner.
