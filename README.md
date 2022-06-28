# livecode-streamer

Tools for educators running "live coding" sessions to make their source files and terminal sessions viewable as read-only webpages, so that students can refer back to off-screen commands as reference.

This project was originally developed within the context of holding [Carpentries workshops](https://carpentries.org/) to teach UNIX shells, git, Python, and R, though it should be generalizable to other programming environments and teaching contexts.

## Dependencies

Hard requirements:
* Python 3.6+
* [watchdog](https://pypi.org/project/watchdog/)
* [keyring](https://pypi.org/project/keyring/)

For general syntax highlighting:
* [pygments](https://pygments.org/)

For Jupyter notebooks:
* [nbformat](https://pypi.org/project/nbformat/)
* [nbconvert](https://pypi.org/project/nbconvert)

For shell sessions, one of the following terminal emulators:
* [Hyper](https://hyper.is/) with the [hyper-html-log plugin](https://github.com/naclomi/hyper-html-log) (Windows/MacOS/Linux)
* [Terminator](https://terminator-gtk3.readthedocs.io/en/latest/) with the [terminator-html-log plugin](https://github.com/naclomi/terminator-html-log) (Linux/MacOS) (TODO)

For generic webspace hosting:
* rsync (optional)
* ssh/scp

For hosting on Github Pages:
* dulwich

## Usage

Run the `livecode-streamer` script in a background terminal window during your lesson:

```
stream.py [options] WATCH_DIR REMOTE_URI
```

`WATCH_DIR` is a local directory containing the source files you are working on, and `REMOTE_URI` is a remote webserver to reflect those documents to. Whenever you save your source files, the script will re-render them to HTML and upload them to the remote server. Students can view these files in their browser, and refresh the page as needed to recieve new content.

To stream a shell session, you must use a terminal emulator that supports automatic logging to HTML. This repository contains plugins to do so with [Terminator](https://terminator-gtk3.readthedocs.io/en/latest/) (Linux/MacOS) and [Hyper](https://hyper.is/) (Windows/MacOS/Linux). For instructions on how to install and use those plugins, see the README.md files in `plugins/terminator` and `plugins/hyper`, respectively. On starting a new terminal session, just use one of these plugins to log your session to the `WATCH_DIR`.

### Hosting and remote URIs

TODO: host on github pages or on local webspace

## Design

Under the hood, this is what's going on:

1. The script goes to sleep and gets woken up whenever a file modification event triggers in the watch directory
2. The script goes through every file in the watch directory and renders it, from scratch, to an HTML file
3. The script uploads the HTML files to a webserver, ideally in a way that minimizes upload bandwidth (ideally with rsync or git, and falling back to scp when neither are available)
4. The script goes back to sleep and waits for the next file modification.

This architecture was chosen to maintain the following design goals:

* Minimal server requirements: The end result can be hosted as a static webpage without custom software or configuration on the remote end of the setup. This allows for usage of University-provided personal webspaces, static file hosts like AWS S3 Buckets and Azure Blob Storage, or static page hosts like Github Pages
* Minimal editor integration: Any code editor should be usable with this system, without specialized modifications (a rule we unfortunately have to break for streaming terminal sessions)
* Robustness and ease-of-use: Ideally, these tools should be able to run with minimal fuss or configuration regardless of operating system or webhost. This project started as a three-line shell script that only worked with Jupyter on Linux, but to make the tool more generally useful more complexity was required.

The following are anti-goals we are NOT trying to solve:

* Keystroke-level page updates: The primary use case for these documents is for students to refer to work on the instructor's computer that has scrolled off-screen. It is not important to build a system that can support this frequency of updates.
* Collaborative editing: Documents are read-only and authored by a single person
* Sandbox execution environments: The audience is expected to be following along with the code on their own set-up; being able to run code in-webpage is less desirable than being able to reproduce the webpage's contents offline in the students' own editors.
* Student feedback, polling, or viewer metrics: These are challenges best left to their own dedicated tools.

## Contributions

This toolset's primary maintainers are currently Naomi Alterman and Noah Benson at the University of Washington's eScience Institute

Pull requests are welcome, though (:

