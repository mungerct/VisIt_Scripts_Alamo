#!/usr/bin/env python
import subprocess

def get_git_hash():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "not a git repo"

print(get_git_hash())

with open("metadata", "a", encoding="utf-8") as f:
    f.write()
    f.write(f"\nGit hash: {get_git_hash()}\n")