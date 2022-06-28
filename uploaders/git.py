import os
import sys
import traceback
import time

import dulwich.porcelain as git

from uploaders.uploader import UploaderPlugin

class GithubPagesUploader(UploaderPlugin):
    @classmethod
    def canHandleURI(cls, uri):
        # TODO: check for push permissions
        if uri.startswith("https://github.com") or uri.startswith("git@github.com"):
            return True
        return False

    @classmethod
    def priority(cls, uri):
        return 30

    @classmethod
    def configure(cls, uri, forced, old_config):
        print("WARNING! The current repository contents and their history at '{:}' will be completely erased by this tool.".format(uri))
        response = None
        while response not in ["Y", "N"]:
            response = input("Is this ok? Y/[N]: ").upper().strip()
            if response == "":
                response = "N"
        if response == "N":
            sys.exit(1)
        return {"confirmed": True}

    def initUploader(self):
        self.repo = git.init(path=self.local_path)
        git.remote_add(self.repo, "origin", self.uri)

        # Touch an empty file called .nojekyll to tell Github to
        # not run jekyll on our static site:
        with open(os.path.join(self.local_path, ".nojekyll"), "w") as f:
            pass
        git.add(self.repo, os.path.join(self.local_path, ".nojekyll"))

        git.commit(self.repo, b"initial commit")
        git.branch_create(self.repo, "main")
        git.update_head(self.repo, b"refs/heads/main")
        self.upload_count = 0

    def uploadFiles(self, files):
        self.upload_count += 1
        for file in files:
            git.add(self.repo, file)
        git.commit(self.repo, "update {:}".format(self.upload_count).encode())
        git.push(self.repo, refspecs="main", force=True)
