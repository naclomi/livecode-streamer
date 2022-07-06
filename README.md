# livecode-streamer

Tool for educators running "live coding" sessions to make their source files and terminal sessions viewable as read-only webpages, so that students can refer back to off-screen commands as reference.

This project was originally developed within the context of holding [Carpentries workshops](https://carpentries.org/) to teach UNIX shells, git, Python, and R, though it should be generalizable to other programming environments and teaching contexts.

## Usage

Run the `livecode-streamer` command in a background terminal window during your lesson:

```
livecode-streamer [options] WATCH_DIR REMOTE_URI
```

`WATCH_DIR` is a local directory containing the source files you are working on, and `REMOTE_URI` is a remote webserver to reflect those documents to. Whenever you save your source files, the script will upload HTML versions of them to the remote server. Students can view these files in their browser, and refresh the page as needed to recieve new content.

To stream a shell session, you must use a terminal emulator that supports automatic logging to HTML. This repository contains plugins to do so with [Terminator](https://terminator-gtk3.readthedocs.io/en/latest/) (Linux/MacOS) and [Hyper](https://hyper.is/) (Windows/MacOS/Linux) (see the subdirectories in this repo's `external-plugins/` folder). On starting a new terminal session, just use one of these plugins to log your session to the `WATCH_DIR`.

### Hosting and remote URIs

The most ideal way to host the output of this tool is on a personal web hosting account that allows access over SSH. Most universities provide this service to their faculty and staff, a la [UW's shared web hosting](https://itconnect.uw.edu/connect/web-publishing/shared-hosting/). The instructions for setting this account up, unfortunately, vary from institution to institution. Once you have access, though, the value to put in `REMOTE_URI` would be the remote destination you would normally put in the second half of an `scp` command (eg: `username@servername:remote_path`).

If suitable institutionally provided web hosting isn't available, there are a few other options:

- **Amazon AWS** or **Microsoft Azure** object storage: this script can directly upload contents to an AWS S3 bucket or Azure Blob Storage contianer, both of which can be configured to serve static webpages. The downside of these services is that they are not free
- **GitHub Pages**: You can create a repo on GitHub and have this script automatically push updates to it. This repo can then be served as a website through GitHub's "Pages" feature. This option is free, though GitHub has a soft limit of 10 page updates per hour.


In all cases, access credentials are securely stored in your operating system's keychain.

## Installataion and dependencies

Install with `pip install livecode-streamer[jupyter]`,
which includes all dependencies needed for basic syntax highlighting, rendering jupyter notebooks, and uploading via `scp`/`rsync`.

To install with dependencies for _all_ plugins:
`pip install livecode-streamer[jupyter,git,azure,aws,localhost]`

Core requirements:
* Python 3.7+
* [watchdog](https://pypi.org/project/watchdog/)
* [keyring](https://pypi.org/project/keyring/)
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
* [dulwich](https://pypi.org/project/dulwich/)

For hosting on Azure blob storage:
* [azure-storage-blob](https://pypi.org/project/azure-storage-blob/)

For hosting on AWS S3 buckets:
* [boto3](https://pypi.org/project/boto3/)

For hosting locally over an ngrok tunnel:
* [pyngrok](https://pypi.org/project/pyngrok/)
