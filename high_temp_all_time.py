#!/usr/bin/env python
"""
VisIt visualization script:
- Saves initial eta/phi field
- Saves legend separately
- Saves temperature plots per timestep and level individually
"""

import sys
import os
from scripts.savemetadata import save_metadata_with_git
from scripts.compile_images import progress_bar
from scripts.input_processing import get_parameters

SuppressMessages(2)  # Suppress warnings
SuppressQueryOutputOn()  # Suppress query output

# ------------------------------------------------------------
# Read input file
# ------------------------------------------------------------
input_file = sys.argv[1] if len(sys.argv) > 1 else None
params = get_parameters(input_file)

# ------------------------------------------------------------
# Database handling
# ------------------------------------------------------------
default_db = "celloutput.visit"
db_root = params["db_path"]
db_path = os.path.join(db_root, default_db)
db_path = os.path.abspath(db_path)

if not os.path.exists(db_path):
    print("ERROR: Could not find celloutput.visit at:")
    print("   " + db_path)
    sys.exit(1)

print(f"Opening database: {db_path}")
OpenDatabase(db_path, 0)

# ------------------------------------------------------------
# Variables
# ------------------------------------------------------------
temperature_var = params["temperature_var"]
background_var = params["background_var"]

numStates = TimeSliderGetNStates()
print(f"Found {numStates} time steps")

step_interval = 10
start_state = 0
end_state = 100
end_state = min(numStates, end_state)

# ------------------------------------------------------------
# Temperature levels
# ------------------------------------------------------------
num_levels = 1
min_temp_thres = 1200
max_temp_thres = 2000
invert_phi = 0

# ------------------------------------------------------------
# SaveWindow settings
# ------------------------------------------------------------
SaveWindowAtts = SaveWindowAttributes()
SaveWindowAtts.outputToCurrentDirectory = 1
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
AnnotationAtts.legendInfoFlag = 1
AnnotationAtts.backgroundColor = (255, 255, 255, 255)
AnnotationAtts.foregroundColor = (0, 0, 0, 255)
SetAnnotationAttributes(AnnotationAtts)

# ------------------------------------------------------------
# Save legend
# ------------------------------------------------------------

AddPlot("Pseudocolor", temperature_var)
SetTimeSliderState(1)

LegendPlotAtts = PseudocolorAttributes()
LegendPlotAtts.scaling = LegendPlotAtts.Linear
LegendPlotAtts.limitsMode = LegendPlotAtts.OriginalData
LegendPlotAtts.minFlag = 1
LegendPlotAtts.min = min_temp_thres
LegendPlotAtts.maxFlag = 1
LegendPlotAtts.max = max_temp_thres
LegendPlotAtts.colorTableName = "plasma"
LegendPlotAtts.opacityType = LegendPlotAtts.FullyOpaque
LegendPlotAtts.legendFlag = 1
LegendPlotAtts.lightingFlag = 0
SetPlotOptions(LegendPlotAtts)

# Draw the plot first so the legend object exists
DrawPlots()

legend = GetAnnotationObject(
    GetPlotList().GetPlots(GetNumPlots() - 1).plotName
)
legend.xScale = 1.0
legend.yScale = 2.0
legend.orientation = legend.VerticalRight
legend.managePosition = 0
legend.position = (0.0, 0.8)
legend.fontHeight = 0.03
legend.drawTitle = 0
legend.numberFormat = "%1.1f"

# Hide everything except the legend
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes2D.visible = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.legendInfoFlag = 1  # Keep legend visible
SetAnnotationAttributes(AnnotationAtts)

AddOperator("Isovolume")
IsoEtaAtts = IsovolumeAttributes()
IsoEtaAtts.variable = background_var
IsoEtaAtts.lbound = 1.1
IsoEtaAtts.ubound = 1e37
SetOperatorOptions(IsoEtaAtts, 0)

# Redraw with updated settings
DrawPlots()

SaveWindowAtts.fileName = "legend_only_DELETE_ME"
SetSaveWindowAttributes(SaveWindowAtts)
SaveWindow()
DeleteActivePlots()

print("Legend saved")

# ------------------------------------------------------------
# Save initial eta/phi field
# ------------------------------------------------------------
SetTimeSliderState(1)
AddPlot("Pseudocolor", background_var, 1, 1)
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

print("Inital Field Saved")

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
PseudocolorAtts.colorTableName = "gray"
PseudocolorAtts.invertColorTable = 1
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

# ------------------------------------------------------------
# Loop over temperature levels and timesteps (no eta background)
# ------------------------------------------------------------
for level in temp_levels:
    print(f"\nSaving Time Steps:")

    for state in range(start_state, end_state, step_interval):
        progress_bar(state + 1, end_state)
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
        IsoEtaAtts.variable = background_var
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

metadata_parameters = {
    "visit_scripts filename": os.path.basename(__file__),
    "step_interval": step_interval,
    "state step number": start_state,
    "end step number": end_state,
    "number of temperature levels": num_levels,
    "minimum temperature": min_temp_thres,
    "maximum temperature": max_temp_thres,
    "initial phi/eta variable name": background_var,
    "invert initial phi/eta": invert_phi,
    "image name": "file_name_test"
}

save_metadata_with_git(metadata_parameters, ".")
sys.exit(0)
