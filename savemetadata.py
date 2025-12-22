#!/usr/bin/env python
import subprocess
import os
import shutil

def save_metadata_with_git(params, output_dir, original_metadata_path=None):
    """
    Save metadata parameters and Git hash to a file in the output directory.
    Also copies the original metadata file from the database if provided.
    
    Args:
        params (dict): Dictionary of metadata parameters. Must include 'image name'.
        output_dir (str): Directory where output files are saved.
        original_metadata_path (str, optional): Path to the original metadata file to copy.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Copy original metadata file if provided

    print(original_metadata_path)
    print(output_dir)

    if original_metadata_path and os.path.exists(original_metadata_path):
        if os.path.abspath(os.path.dirname(original_metadata_path)) != os.path.abspath(output_dir):
            shutil.copy2(original_metadata_path, output_dir)
            print(f"Copied original metadata file to: {output_dir}")

    # Step 2: Build metadata filename based on latest image
    latest_name = params.get("image name")
    if not latest_name:
        raise ValueError("'image name' must be present in the parameters dictionary.")

    base_name, _ = os.path.splitext(latest_name)
    metadata_filename = f"metadata_{base_name}"
    metadata_path = os.path.join(output_dir, metadata_filename)

    # Step 3: Write parameters to the metadata file
    with open(metadata_path, "a", encoding="utf-8") as f:
        f.write("\n--- Parameters ---\n")
        for key, value in params.items():
            f.write(f"{key}: {value}\n")

    # Step 4: Append Git hash
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

    print(f"Metadata and Git hash saved to: {metadata_path}")