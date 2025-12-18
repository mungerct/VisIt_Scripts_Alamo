#!/usr/bin/env python
import subprocess
import os

def save_git_hash(metadata_path="metadata"):
    def get_git_hash():
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except Exception:
            return "not a git repo"

    with open(metadata_path, "a", encoding="utf-8") as f:
        f.write("\n\nvisit script metadata:")
        f.write(f"\nGit hash: {get_git_hash()}\n")


def save_metadata_params(params, metadata_dir):
    """
    Append key-value pairs from a dictionary to a metadata file.
    The metadata filename is modified to include the 'image name' value from the dictionary.
    
    Args:
        params (dict): Dictionary of key-value pairs to save. Must include 'image name'.
        metadata_dir (str): Directory to save the metadata file (use the output directory).
    """
    # Ensure the directory exists
    os.makedirs(metadata_dir, exist_ok=True)

    # Get latest_name from dictionary
    latest_name = params.get("image name")
    if not latest_name:
        raise ValueError("'image name' must be present in the dictionary to name the metadata file.")

    # Build metadata filename
    base_name, _ = os.path.splitext(latest_name)
    metadata_filename = f"metadata_{base_name}"
    metadata_path = os.path.join(metadata_dir, metadata_filename)

    # Write dictionary to metadata file
    with open(metadata_path, "a", encoding="utf-8") as f:
        f.write("\n--- Parameters ---\n")
        for key, value in params.items():
            f.write(f"{key}: {value}\n")
    
def main():
    save_git_hash()

if __name__ == "__main__":
    main()