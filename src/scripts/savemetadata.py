#!/usr/bin/env python

def save_metadata_with_git(params, output_dir):
    import subprocess
    import os
    from datetime import datetime
    """
    Save metadata parameters and Git hash to a file in the output directory.
    
    Args:
        params (dict): Dictionary of metadata parameters. Must include 'image name'.
        output_dir (str): Directory where output files are saved.
        original_metadata_path (str, optional): Path to the original metadata file to copy.
    """

    # Step 1: Build metadata filename based on latest image
    filename_name = params.get("file.output_filename")
    if not filename_name:
        raise ValueError("\n'image file name' must be present in the parameters dictionary.")

    base_name, _ = os.path.splitext(filename_name)
    metadata_filename = f"{base_name}_metadata.txt"
    metadata_path = os.path.join(metadata_filename)

    # Step 2: Write parameters to the metadata file
    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write("\n--- Parameters ---\n")
        for key, value in params.items():
            f.write(f"{key}: {value}\n")

    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write("\n--- Parameters ---\n")
        for key, value in params.items():
            if params["plotting.main_plotting_var.define_scalar_expression.on"] == 0 and key in {"plotting.main_plotting_var.define_scalar_expression.on", 
                                                                                                 "plotting.main_plotting_var.define_scalar_expression.name",
                                                                                                 "plotting.main_plotting_var.define_scalar_expression.expression"}:
                continue
            elif params["plotting.main_plotting_var.thresholding.on"] == 0 and key in {"plotting.main_plotting_var.thresholding.on",
                                                                                                 "plotting.main_plotting_var.thresholding.var.name",
                                                                                                 "plotting.main_plotting_var.thresholding.var.min",
                                                                                                 "plotting.main_plotting_var.thresholding.var.max"}:
                continue
            elif params["plotting.background_var.on"] == 0 and key in {"plotting.background_var.on",
                                                                                                 "plotting.background_var.name",
                                                                                                 "plotting.background_var.invert",
                                                                                                 "plotting.background_var.colormap"}:
                continue
            elif params["plotting.legend.name.on"] == 0 and key in {"plotting.legend.name.on",
                                                                                                 "plotting.legend.name.text",
                                                                                                 "plotting.legend.name.position.x",
                                                                                                 "plotting.legend.name.position.y",
                                                                                                 "plotting.legend.name.dpi",
                                                                                                 "plotting.legend.name.fontsize"}:
                continue
            elif params["plotting.contour.on"] == 0 and key in {"plotting.contour.on",
                                                                                                 "plotting.contour.var.name",
                                                                                                 "plotting.contour.values",
                                                                                                 "plotting.contour.linewidth",
                                                                                                 "plotting.contour.color"}:
                continue
            elif params["high_var.mode"] == "space" and key in {"sim.time.arr"}:
                continue
            elif params["sim.type"] == "high_var" and key in {}

            else:
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
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
    print(f"\nMetadata and Git hash saved to: {metadata_path}")
