#!/usr/bin/env python
import subprocess
import os
import shutil

def save_metadata_with_git(params, output_dir):
    """
    Save metadata parameters and Git hash to a file in the output directory.
    
    Args:
        params (dict): Dictionary of metadata parameters. Must include 'image name'.
        output_dir (str): Directory where output files are saved.
        original_metadata_path (str, optional): Path to the original metadata file to copy.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Build metadata filename based on latest image
    filename_name = params.get("image name")
    if not filename_name:
        raise ValueError("\n'image file name' must be present in the parameters dictionary.")

    base_name, _ = os.path.splitext(filename_name)
    metadata_filename = f"{base_name}_metadata.txt"
    metadata_path = os.path.join(output_dir, metadata_filename)

    # Step 2: Write parameters to the metadata file
    with open(metadata_path, "a", encoding="utf-8") as f:
        f.write("\n--- Parameters ---\n")
        for key, value in params.items():
            f.write(f"{key}: {value}\n")

    # Step 3: Append Git hash
    def get_git_hash():
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except Exception:
            return "not a git repo"

    with open(metadata_path, "a", encoding="utf-8") as f:
        f.write("\n--- Visit Script Metadata ---\n")
        f.write(f"Git hash: {get_git_hash()}\n")

    print(f"\nMetadata and Git hash saved to: {metadata_path}")