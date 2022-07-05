# Contributing to livecode-streamer

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

This toolset's primary maintainer is currently Naomi Alterman at the University of Washington's eScience Institute

Pull requests are welcome, though (:

