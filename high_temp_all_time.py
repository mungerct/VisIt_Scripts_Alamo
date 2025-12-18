#!/usr/bin/env python
"""
VisIt visualization script for overlaying temperature plots across all time steps
Creates a composite view of temperature evolution using TWO isovolume filters
"""

import sys
import os

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
# Variables
# ------------------------------------------------------------
temperature_var = "temp"
eta_var = "eta"

numStates = TimeSliderGetNStates()
print(f"Found {numStates} time steps")

step_interval = 50
start_state = 0
end_state = numStates

# ------------------------------------------------------------
# Temperature levels
# ------------------------------------------------------------
num_levels = 3
min_temp_thres = 1000
max_temp_thres = 1750
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
for level in temp_levels:
    print(f"Processing temperature level {level:.2f}")

    for state in range(start_state, end_state, step_interval):
        print(f"  Time step {state + 1}/{numStates}")
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
SaveWindowAtts.family = 0
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
sys.exit(0)
