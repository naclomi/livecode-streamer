import functools
import http.server
import os
import sys
import threading

from uploaders.uploader import UploaderPlugin
import pyngrok.ngrok

def serveDirectoryWithHTTP(local_uri, hostname="localhost"):
    # Adapted from:
    # https://gist.github.com/kwk/5387c0e8d629d09f93665169879ccb86
    port = 0
    directory = os.path.abspath(local_uri)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    httpd = http.server.HTTPServer((hostname, 0), handler, False)
    httpd.timeout = 0.5
    httpd.allow_reuse_address = True

    httpd.server_bind()
    httpd.server_activate()

    def serve_forever(httpd):
        with httpd:
            httpd.serve_forever()

    thread = threading.Thread(target=serve_forever, args=(httpd, ))
    thread.setDaemon(True)
    thread.start()

    return httpd

class LocalhostUploader(UploaderPlugin):
    @classmethod
    def canHandleURI(cls, uri):
        return uri == "localhost"

    @classmethod
    def priority(cls, uri):
        return 30

    @classmethod
    def configure(cls, uri, forced, old_config):
        auth_token = input("Please specify ngrok auth token: ")
        if auth_token.strip() == "":
            print("No token specified, aborting")
            sys.exit(1)
        return {"auth_token": auth_token}

    def initUploader(self):
        pyngrok.ngrok.set_auth_token(self.config["auth_token"])
        self.server = serveDirectoryWithHTTP(self.local_path, "0.0.0.0")
        self.tunnel = pyngrok.ngrok.connect(addr="{:}".format(self.server.server_address[1]))
        print(self.server.server_address)
        print("Serving local files from {:}".format(self.tunnel.public_url))
