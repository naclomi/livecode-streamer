#!/usr/bin/env python3
import argparse
import glob
import logging
import os
import platform
import subprocess
import sys
import tempfile
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import keyring
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import renderers
import uploaders

class UploadHandler(FileSystemEventHandler):
    def __init__(self, watch_uri, local_uri, uploader, min_event_delta=.5):
        self.watch_uri = watch_uri
        self.local_uri = local_uri
        self.uploader = uploader
        self.renderers = {}
        self.lastUploadedVersion = {}
        self.min_event_delta = min_event_delta
        self.last_event = None

    def update(self):
        if os.path.isdir(self.watch_uri):
            files = glob.glob(os.path.join(self.watch_uri, "*"))
        else:
            files = [self.watch_uri]
        out_files = []
        for in_filename in files:
            # TODO: make out filename relative to watch_uri:
            out_filename = os.path.basename(in_filename) + ".html"
            out_full_filename = os.path.join(self.local_uri, out_filename)
            mod_time = os.path.getmtime(in_filename)
            if in_filename in self.lastUploadedVersion:
                if mod_time == self.lastUploadedVersion[in_filename]:
                    continue
            self.lastUploadedVersion[in_filename] = mod_time

            if in_filename not in self.renderers:
                self.renderers[in_filename] = renderers.get_renderer(in_filename)(in_filename, out_full_filename)
            out_files += self.renderers[in_filename].render()
            print("Processed {:} into {:} using {:}".format(in_filename, out_full_filename, type(self.renderers[in_filename]).__name__))

        self.uploader.uploadFiles(out_files)
        for file in out_files:
            print("Uploaded {:} to {:}".format(file, self.uploader.uri))


    def on_modified(self, event):
        # Debounce filesystems where a save triggers multiple
        # modification events
        now = time.time()
        if self.last_event is not None:
            if now - self.last_event < self.min_event_delta:
                return
        self.last_event = now

        # TODO: figure out a way to avoid this:
        # On Windows this pause is necessary to let filesystem changes
        # propagate between WSL and the host OS
        time.sleep(.2)

        self.update()

def getPlatformString():
    uname = platform.uname()
    return "{:} ({:}) @ '{:}'".format(
        uname.system, uname.release, sys.prefix)

def detectWslWarnings(args):
    if 'microsoft-standard' in platform.uname().release:
        cmd = ["df", "--output=source", args.watch_dir]
        result = subprocess.run(cmd, capture_output=True)
        stdout = result.stdout.decode()
        if "drvfs" in stdout:
            # Watching a windows drive from WSL
            logging.error("Cannot watch files from a Windows drive from with WSL. Either rerun this script outside of WSL, or keep your watched source files from within WSL's filesystem.")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("watch_dir", metavar="WATCH_DIR", help="Directory to watch for changing source files")
    parser.add_argument("remote_uri", metavar="REMOTE_URI", help="Remote URI to upload HTML-rendered copies of the watched source to")
    parser.add_argument("--configure-uploader", action="store_true", help="Configure settings for the in-use uploader plugin")
    parser.add_argument("--uploader", type=str, help="Use a specific uploader plugin, rather than choose one automatically")
    parser.add_argument("--list-plugins", action="store_true", help="List plugins available and exit")
    parser.add_argument(
        '-v', '--verbose',
        help="Print extra operating information",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    logging.info(getPlatformString())
    detectWslWarnings(args)


    if args.list_plugins:
        uploaders.get_uploader("")
        renderers.get_renderer("")
        print("Supported uploader plugins: {:}\nSupported render plugins: {:}".format(
            ", ".join(plugin.__name__ for plugin in uploaders.plugin_classes),
            ", ".join(plugin.__name__ for plugin in renderers.plugin_classes)
            ))
        sys.exit(0)


    if args.uploader is None:
        uploader_type = uploaders.get_uploader(args.remote_uri)
        if uploader_type is None:
            sys.stderr.write("Could not identify an uploader capable of handling remote URI\n")
            sys.exit(1)
    else:
        uploader_type = None
        uploaders.get_uploader("")
        for uploader in uploaders.plugin_classes:
            if uploader.__name__ == args.uploader:
                uploader_type = uploader
                break
        if uploader_type is None:
            sys.stderr.write("Could not find specified uploader plugin\n")
            sys.exit(1)
    print("Using " + uploader_type.__name__)

    with tempfile.TemporaryDirectory() as serve_dir:
        print("Staging directory is " + serve_dir)
    
        uploader = uploader_type(serve_dir, args.remote_uri, args.configure_uploader)

        observer = Observer()
        handler = UploadHandler(args.watch_dir, serve_dir, uploader)
        observer.schedule(handler, args.watch_dir, recursive=True)
        observer.start()

        print("Watching {:}...\nHit Ctrl+C to exit".format(args.watch_dir))
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
            observer.join()

if __name__ == "__main__":
    main()