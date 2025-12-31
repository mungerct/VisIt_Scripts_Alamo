#!/usr/bin/env python

def delete_delete_me_files(directory="."):
    import os
    """
    Deletes all files in the given directory whose names contain 'DELETE_ME'.
    Defaults to the current directory.
    """
    deleted = 0

    for filename in os.listdir(directory):
        if "DELETE_ME" in filename:
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):
                os.remove(filepath)
                deleted += 1
    return