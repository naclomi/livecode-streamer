#!/usr/bin/env python3
import argparse
import glob
import os
import subprocess
import sys
import tempfile
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import sysrsync
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from renderers import get_renderer
from uploaders import get_uploader

class UploadHandler(FileSystemEventHandler):
    def __init__(self, watch_uri, local_uri, uploader, min_event_delta=.5):
        self.watch_uri = watch_uri
        self.local_uri = local_uri
        self.uploader = uploader
        self.renderers = {}
        self.min_event_delta = min_event_delta
        self.last_event = None

    def update(self):
        if os.path.isdir(self.watch_uri):
            files = glob.glob(os.path.join(self.watch_uri, "*"))
        else:
            files = [self.watch_uri]
        for in_filename in files:
            out_filename = os.path.splitext(os.path.basename(in_filename))[0] + ".html"
            out_full_filename = os.path.join(self.local_uri, out_filename)            
            if in_filename not in self.renderers:
                self.renderers[in_filename] = get_renderer(in_filename, out_full_filename)
            self.renderers[in_filename].render()
            print("Processed {:} into {:} using {:}".format(in_filename, out_full_filename, type(self.renderers[in_filename]).__name__))
        self.uploader.uploadDirectory(self.local_uri)

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("watch_dir", metavar="WATCH_DIR", help="Directory to watch for changing source files")
    parser.add_argument("remote_uri", metavar="REMOTE_URI", help="Remote URI to upload HTML-rendered copies of the watched source to")
    
    args = parser.parse_args()

    uploader = get_uploader(args.remote_uri)
    print("Using " + type(uploader).__name__)

    with tempfile.TemporaryDirectory() as serve_dir:
        print("Staging directory is " + serve_dir)

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
