#!/usr/bin/env python
"""
VisIt visualization script for overlaying temperature plots across all time steps
Creates a composite view of temperature evolution using TWO isovolume filters
"""

import sys
import os
import shutil
import glob
from savemetadata import save_git_hash, save_metadata_params

default_db = "celloutput.visit"

# ------------------------------------------------------------
# Database handling
# ------------------------------------------------------------
if len(sys.argv) > 1:
    db_path = sys.argv[1]
    if not db_path.endswith(default_db):
        db_path = os.path.join(db_path, default_db)
else:
    db_path = os.path.join(os.getcwd(), default_db)

db_path = os.path.abspath(db_path)

if not os.path.exists(db_path):
    print("ERROR: Could not find celloutput.visit at:")
    print("   " + db_path)
    sys.exit(1)

print(f"Opening database: {db_path}")
OpenDatabase(db_path, 0)

# ------------------------------------------------------------
# Output directory
# ------------------------------------------------------------
parent_dir = os.path.dirname(db_path)
folder_name = os.path.basename(parent_dir)
output_dir = os.path.join(os.getcwd(), folder_name)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")
else:
    print(f"Saving frames in existing directory: {output_dir}")

# ------------------------------------------------------------
# Copy metadata file
# ------------------------------------------------------------
metadata_src = os.path.join(parent_dir, "metadata")
metadata_dst = os.path.join(output_dir, "metadata")

if os.path.exists(metadata_src):
    shutil.copy2(metadata_src, metadata_dst)
    print(f"Copied metadata to: {metadata_dst}")
else:
    print("WARNING: metadata file not found in database folder")

# ------------------------------------------------------------
# Variables
# ------------------------------------------------------------
temperature_var = "temp"
eta_var = "eta"

numStates = TimeSliderGetNStates()
print(f"Found {numStates} time steps")

step_interval = 50
start_state = 0
end_state = min(numStates, 100)

# ------------------------------------------------------------
# Temperature levels
# ------------------------------------------------------------
num_levels = 2
min_temp_thres = 1300
max_temp_thres = 1500
invert_phi = 0

# ------------------------------------------------------------
# Annotation settings
# ------------------------------------------------------------
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes2D.visible = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.legendInfoFlag = 1
AnnotationAtts.backgroundColor = (255, 255, 255, 255)
AnnotationAtts.foregroundColor = (0, 0, 0, 255)
SetAnnotationAttributes(AnnotationAtts)

# ------------------------------------------------------------
# Background eta plot (frozen in time)
# ------------------------------------------------------------
print("Drawing eta plot from timestep 1")
SetTimeSliderState(1)

AddPlot("Pseudocolor", eta_var, 1, 1)
SetPlotFollowsTime(0)

PhiAtts = PseudocolorAttributes()
PhiAtts.minFlag = 1
PhiAtts.min = 0
PhiAtts.maxFlag = 1
PhiAtts.max = 1
PhiAtts.colorTableName = "gray"
PhiAtts.invertColorTable = invert_phi
PhiAtts.legendFlag = 0
PhiAtts.lightingFlag = 0
SetPlotOptions(PhiAtts)

print("Eta background plot configured")
DrawPlots()
# ------------------------------------------------------------
# Temperature plot attributes
# ------------------------------------------------------------
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = min_temp_thres
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = max_temp_thres
PseudocolorAtts.colorTableName = "hot"
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque
PseudocolorAtts.legendFlag = 0
PseudocolorAtts.lightingFlag = 0

# ------------------------------------------------------------
# Generate temperature levels
# ------------------------------------------------------------
if num_levels > 1:
    step_size = (max_temp_thres - min_temp_thres) / (num_levels - 1)
    temp_levels = [min_temp_thres + i * step_size for i in range(num_levels)]
else:
    temp_levels = [min_temp_thres]

# ------------------------------------------------------------
# Loop over temperature levels and timesteps
# ------------------------------------------------------------

def progress_bar(i, total, width=40):
    frac = (i + 1) / float(total)
    filled = int(width * frac)
    bar = "#" * filled + "-" * (width - filled)
    sys.stdout.write(
        f"\r  Time steps: [{bar}] {i + 1}/{total} ({frac*100:5.1f}%)"
    )
    sys.stdout.flush()

    if i + 1 == total:
        print()  # newline at end

for level in temp_levels:
    print(f"\nProcessing temperature level {level:.2f}")

    for state in range(start_state, end_state, step_interval):
        progress_bar(state, end_state)
        SetTimeSliderState(state)

        AddPlot("Pseudocolor", temperature_var, 1, 0)
        SetPlotOptions(PseudocolorAtts)

        # ----------------------------------------------------
        # Isovolume 2: eta >= 0.5
        # ----------------------------------------------------
        AddOperator("Isovolume")
        IsoEtaAtts = IsovolumeAttributes()
        IsoEtaAtts.variable = eta_var
        IsoEtaAtts.lbound = 0.5
        IsoEtaAtts.ubound = 1e37
        # IsoEtaAtts.outputMeshType = IsoEtaAtts.InputZones
        SetOperatorOptions(IsoEtaAtts, 0)

        # ----------------------------------------------------
        # Isovolume 1: temperature >= level
        # ----------------------------------------------------
        AddOperator("Isovolume")
        IsoTempAtts = IsovolumeAttributes()
        IsoTempAtts.variable = temperature_var
        IsoTempAtts.lbound = level
        IsoTempAtts.ubound = 1e37
        # IsoTempAtts.outputMeshType = IsoTempAtts.InputZones
        SetOperatorOptions(IsoTempAtts, 1)

        SetActivePlots(GetNumPlots() - 1)
        SetPlotFollowsTime(0)

print("All time steps configured, drawing all plots...")
DrawPlots()

# ------------------------------------------------------------
# Save window settings
# ------------------------------------------------------------
SaveWindowAtts = SaveWindowAttributes()
SaveWindowAtts.outputToCurrentDirectory = 0
SaveWindowAtts.outputDirectory = output_dir
SaveWindowAtts.fileName = "temperature_all_timesteps"
SaveWindowAtts.family = 1
SaveWindowAtts.format = SaveWindowAtts.PNG
SaveWindowAtts.width = 4000
SaveWindowAtts.height = 4000
SaveWindowAtts.screenCapture = 0
SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
SetSaveWindowAttributes(SaveWindowAtts)

# ------------------------------------------------------------
# Legend (single invisible plot)
# ------------------------------------------------------------
print("Adding legend...")
AddPlot("Pseudocolor", temperature_var, 1, 1)

LegendPlotAtts = PseudocolorAttributes()
LegendPlotAtts.minFlag = 1
LegendPlotAtts.min = min_temp_thres
LegendPlotAtts.maxFlag = 1
LegendPlotAtts.max = max_temp_thres
LegendPlotAtts.colorTableName = "hot"
LegendPlotAtts.opacity = 0
LegendPlotAtts.legendFlag = 1
LegendPlotAtts.lightingFlag = 0
SetPlotOptions(LegendPlotAtts)

DrawPlots()

legend = GetAnnotationObject(
    GetPlotList().GetPlots(GetNumPlots() - 1).plotName
)
legend.xScale = 1.0
legend.yScale = 2.0
legend.orientation = legend.VerticalRight
legend.managePosition = 0
legend.position = (0.0, 0.9)
legend.fontHeight = 0.03
legend.drawTitle = 0
legend.numberFormat = "%1.1f"

SaveWindow()

print("Image saved successfully!")

def most_recent_file(directory, pattern="*"):
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    return max(files, key=os.path.getctime)

latest_file = most_recent_file(
    SaveWindowAtts.outputDirectory,
    f"{SaveWindowAtts.fileName}*"
)

if latest_file:
    latest_name = os.path.basename(latest_file)

metadata_parameters = {
    "visit_scripts filename": os.path.basename(__file__),
    "step_interval": step_interval,
    "state step number": start_state,
    "end step number": end_state,
    "number of temperature levels": num_levels,
    "minimum temperature": min_temp_thres,
    "maximum temperature": max_temp_thres,
    "initial phi/eta variable name": eta_var,
    "invert initial phi/eta": invert_phi,
    "image name": latest_name
}

save_git_hash(metadata_path=os.path.join(output_dir, "metadata"))
save_metadata_params(metadata_parameters, output_dir)

sys.exit(0)
