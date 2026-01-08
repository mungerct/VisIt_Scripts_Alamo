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
default_db = params["file.default_db"]
db_root = params["file.db_path"]
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
if params["plotting.main_plotting_var.define_scalar_expression.on"]:
    DefineScalarExpression(
        params["plotting.main_plotting_var.define_scalar_expression.name"],
        params["plotting.main_plotting_var.define_scalar_expression.expression"]
    )
    plotting_var = params["plotting.main_plotting_var.define_scalar_expression.name"]
else:
    plotting_var = params["plotting.main_plotting_var.name"]

background_var = params["plotting.background_var.name"]

numStates = TimeSliderGetNStates()

step_interval = params["step.interval"]
start_state = params["step.start"]
threhold_var = params["plotting.main_plotting_var.thresholding.var.name"]

if params["step.end"] == -1:
    end_state = numStates
    print(f"Found {numStates} time steps")
    params["step.end"] = numStates
else:
    end_state = params["step.end"]
    print(f"Using {numStates} time steps")
    if end_state > numStates:
        print(f"Warning: end_state {end_state} exceeds available states {numStates}, using {numStates} instead")
        end_state = min(numStates, end_state)

# ------------------------------------------------------------
# Temperature levels
# ------------------------------------------------------------
num_levels = 1
min_var = params["plotting.main_plotting_var.min"]
max_var = params["plotting.main_plotting_var.max"]
invert_phi = params["plotting.background_var.invert"]

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

AddPlot("Pseudocolor", plotting_var)
SetTimeSliderState(1)

LegendPlotAtts = PseudocolorAttributes()
LegendPlotAtts.scaling = LegendPlotAtts.Linear
LegendPlotAtts.limitsMode = LegendPlotAtts.OriginalData
LegendPlotAtts.minFlag = 1
LegendPlotAtts.min = min_var
LegendPlotAtts.maxFlag = 1
LegendPlotAtts.max = max_var
LegendPlotAtts.colorTableName = params["plotting.main_plotting_var.colormap"]
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
IsoEtaAtts.variable = threhold_var
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
if params["plotting.background_var.on"]:
    SetTimeSliderState(1)
    AddPlot("Pseudocolor", background_var, 1, 1)
    PhiAtts = PseudocolorAttributes()
    PhiAtts.minFlag = 1
    PhiAtts.min = 0
    PhiAtts.maxFlag = 1
    PhiAtts.max = 1
    PhiAtts.colorTableName = params["plotting.background_var.colormap"]
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
PseudocolorAtts.min = min_var
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = max_var
PseudocolorAtts.colorTableName = "gray"
PseudocolorAtts.invertColorTable = 1
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque
PseudocolorAtts.legendFlag = 0
PseudocolorAtts.lightingFlag = 0

# ------------------------------------------------------------
# Loop over temperature levels and timesteps (no eta background)
# ------------------------------------------------------------

print(f"\nSaving Time Steps:")

for state in range(start_state, end_state, step_interval):
    progress_bar(state + 1, end_state)
    SetTimeSliderState(state)

    # Remove previous temperature plots
    for i in range(GetNumPlots() - 1, 0, -1):
        DeleteActivePlots()

    # Add temperature plot only
    AddPlot("Pseudocolor", plotting_var, 1, 0)
    SetPlotOptions(PseudocolorAtts)

    # Isovolume 2: eta >= 0.5
    AddOperator("Isovolume")
    IsoEtaAtts = IsovolumeAttributes()
    IsoEtaAtts.variable = threhold_var
    IsoEtaAtts.lbound = 0.5
    IsoEtaAtts.ubound = 1e37
    SetOperatorOptions(IsoEtaAtts, 1)

    # Isovolume 1: temperature >= min_var
    AddOperator("Isovolume")
    IsoTempAtts = IsovolumeAttributes()
    IsoTempAtts.variable = plotting_var
    IsoTempAtts.lbound = min_var
    IsoTempAtts.ubound = 1e37
    SetOperatorOptions(IsoTempAtts, 0)

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

save_metadata_with_git(params, ".")
sys.exit(0)
