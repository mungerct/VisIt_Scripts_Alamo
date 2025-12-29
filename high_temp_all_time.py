#!/usr/bin/env python
"""
VisIt visualization script:
- Saves initial eta/phi field
- Saves legend separately
- Saves temperature plots per timestep and level individually
"""

import sys
import os
import shutil
import glob
from savemetadata import save_metadata_with_git

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

# # ------------------------------------------------------------
# # Copy metadata file
# # ------------------------------------------------------------
# metadata_src = os.path.join(parent_dir, "metadata")
# metadata_dst = os.path.join(output_dir, "metadata")

# if os.path.exists(metadata_src):
#     shutil.copy2(metadata_src, metadata_dst)
#     print(f"Copied metadata to: {metadata_dst}")
# else:
#     print("WARNING: metadata file not found in database folder")

# ------------------------------------------------------------
# Variables
# ------------------------------------------------------------
temperature_var = "temp"
eta_var = "eta"

numStates = TimeSliderGetNStates()
print(f"Found {numStates} time steps")

step_interval = 20
start_state = 0
end_state = min(numStates, 100)

# ------------------------------------------------------------
# Temperature levels
# ------------------------------------------------------------
num_levels = 3
min_temp_thres = 400
max_temp_thres = 1000
invert_phi = 0

# ------------------------------------------------------------
# SaveWindow settings
# ------------------------------------------------------------
SaveWindowAtts = SaveWindowAttributes()
SaveWindowAtts.outputToCurrentDirectory = 0
SaveWindowAtts.outputDirectory = output_dir
SaveWindowAtts.family = 1
SaveWindowAtts.format = SaveWindowAtts.PNG
SaveWindowAtts.width = 1080
SaveWindowAtts.height = 1080
SaveWindowAtts.screenCapture = 0
SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint

# ------------------------------------------------------------
# General annotation settings (hide axes, legend, borders)
# ------------------------------------------------------------
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes2D.visible = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.legendInfoFlag = 0
AnnotationAtts.backgroundColor = (255, 255, 255, 255)
AnnotationAtts.foregroundColor = (0, 0, 0, 255)
SetAnnotationAttributes(AnnotationAtts)

AddPlot("Pseudocolor", temperature_var)
SetTimeSliderState(1)

LegendPlotAtts = PseudocolorAttributes()
LegendPlotAtts.scaling = LegendPlotAtts.Linear
LegendPlotAtts.limitsMode = LegendPlotAtts.OriginalData
LegendPlotAtts.minFlag = 1
LegendPlotAtts.min = min_temp_thres
LegendPlotAtts.maxFlag = 1
LegendPlotAtts.max = max_temp_thres
LegendPlotAtts.colorTableName = "hot"
LegendPlotAtts.opacityType = LegendPlotAtts.FullyOpaque
LegendPlotAtts.legendFlag = 1
LegendPlotAtts.lightingFlag = 0
SetPlotOptions(LegendPlotAtts)

# Draw the plot FIRST so the legend object exists
# DrawPlots()

# legend = GetAnnotationObject(
#     GetPlotList().GetPlots(GetNumPlots() - 1).plotName
# )
# legend.xScale = 1.0
# legend.yScale = 2.0
# legend.orientation = legend.VerticalRight
# legend.managePosition = 0
# legend.position = (0.05, 0.1)
# legend.fontHeight = 0.03
# legend.drawTitle = 0
# legend.numberFormat = "%1.1f"

# # Hide everything except the legend
# AnnotationAtts = AnnotationAttributes()
# AnnotationAtts.axes2D.visible = 0
# AnnotationAtts.userInfoFlag = 0
# AnnotationAtts.databaseInfoFlag = 0
# AnnotationAtts.timeInfoFlag = 0
# AnnotationAtts.legendInfoFlag = 1  # Keep legend visible
# SetAnnotationAttributes(AnnotationAtts)

# Redraw with updated settings
DrawPlots()

SaveWindowAtts.fileName = "legend_only_DELETE_ME"
SetSaveWindowAttributes(SaveWindowAtts)
SaveWindow()
DeleteActivePlots()

print("Legend saved successfully!")

# ------------------------------------------------------------
# Save initial eta/phi field
# ------------------------------------------------------------
SetTimeSliderState(1)
AddPlot("Pseudocolor", eta_var, 1, 1)
PhiAtts = PseudocolorAttributes()
PhiAtts.minFlag = 1
PhiAtts.min = 0
PhiAtts.maxFlag = 1
PhiAtts.max = 1
PhiAtts.colorTableName = "gray"
PhiAtts.invertColorTable = invert_phi
PhiAtts.legendFlag = 0
SetPlotOptions(PhiAtts)
DrawPlots()

SaveWindowAtts.fileName = "initial_field_DELETE_ME"
SetSaveWindowAttributes(SaveWindowAtts)
SaveWindow()
DeleteActivePlots()

print("Legend saved successfully!")

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
# Progress bar function
# ------------------------------------------------------------
def progress_bar(i, total, width=40):
    frac = i / float(total)
    filled = int(width * frac)
    bar = "#" * filled + "-" * (width - filled)
    sys.stdout.write(f"\r  Time steps: [{bar}] {i}/{total} ({frac*100:5.1f}%)")
    sys.stdout.flush()
    if i == total:
        print()

# ------------------------------------------------------------
# Loop over temperature levels and timesteps (no eta background)
# ------------------------------------------------------------
for level in temp_levels:
    print(f"\nProcessing temperature level {level:.2f}")

    for state in range(start_state, end_state, step_interval):
        progress_bar(state, end_state)
        SetTimeSliderState(state)

        # Remove previous temperature plots
        for i in range(GetNumPlots() - 1, 0, -1):
            DeleteActivePlots()

        # Add temperature plot only
        AddPlot("Pseudocolor", temperature_var, 1, 0)
        SetPlotOptions(PseudocolorAtts)

        # Isovolume 2: eta >= 0.5
        AddOperator("Isovolume")
        IsoEtaAtts = IsovolumeAttributes()
        IsoEtaAtts.variable = eta_var
        IsoEtaAtts.lbound = 0.5
        IsoEtaAtts.ubound = 1e37
        SetOperatorOptions(IsoEtaAtts, 0)

        # Isovolume 1: temperature >= level
        AddOperator("Isovolume")
        IsoTempAtts = IsovolumeAttributes()
        IsoTempAtts.variable = temperature_var
        IsoTempAtts.lbound = level
        IsoTempAtts.ubound = 1e37
        SetOperatorOptions(IsoTempAtts, 1)

        SetActivePlots(GetNumPlots() - 1)
        SetPlotFollowsTime(0)

        # Draw and save each timestep
        DrawPlots()
        SaveWindowAtts.fileName = "temp_field_DELETE_ME"
        SetSaveWindowAttributes(SaveWindowAtts)
        SaveWindow()

# ------------------------------------------------------------
# Save metadata
# ------------------------------------------------------------
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

save_metadata_with_git(metadata_parameters, output_dir, os.path.join(parent_dir, "metadata"))
sys.exit(0)
