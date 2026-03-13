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
min_threhold = params["plotting.main_plotting_var.thresholding.var.min"]
max_threhold = params["plotting.main_plotting_var.thresholding.var.max"]

# ------------------------------------------------------------
# SaveWindow settings
# ------------------------------------------------------------
SaveWindowAtts = SaveWindowAttributes()
SaveWindowAtts.outputToCurrentDirectory = 1
SaveWindowAtts.family = 1
SaveWindowAtts.format = SaveWindowAtts.PNG
SaveWindowAtts.width = params["file.width"]
SaveWindowAtts.height = params["file.height"]
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
# Plot attributes
# ------------------------------------------------------------
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = min_var
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = max_var
PseudocolorAtts.colorTableName = params["plotting.main_plotting_var.colormap"]
PseudocolorAtts.invertColorTable = 0
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 0

# ------------------------------------------------------------
# Loop over temperature levels and timesteps (no eta background)
# ------------------------------------------------------------

print(f"\nSaving Time Steps:")

for state in range(start_state, end_state, step_interval):
    progress_bar(state + 1, end_state)
    DeleteAllPlots()

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

    # Add temperature plot only
    SetTimeSliderState(state)
    AddPlot("Pseudocolor", plotting_var, 1, 0)
    SetPlotOptions(PseudocolorAtts)

    if params["plotting.main_plotting_var.thresholding.on"]:
        # Isovolume for eta >= 0.5
        AddOperator("Isovolume")
        IsoEtaAtts = IsovolumeAttributes()
        IsoEtaAtts.variable = threhold_var
        IsoEtaAtts.lbound = min_threhold
        IsoEtaAtts.ubound = max_threhold
        SetOperatorOptions(IsoEtaAtts, 0)  # First operator (index 0)

        # Isovolume for temperature >= min_var
        AddOperator("Isovolume")
        IsoTempAtts = IsovolumeAttributes()
        IsoTempAtts.variable = plotting_var
        IsoTempAtts.lbound = min_var
        IsoTempAtts.ubound = 1e37
        SetOperatorOptions(IsoTempAtts, 1)  # Second operator (index 1)
    else:
        # Isovolume for temperature >= min_var only
        AddOperator("Isovolume")
        IsoTempAtts = IsovolumeAttributes()
        IsoTempAtts.variable = plotting_var
        IsoTempAtts.lbound = min_var
        IsoTempAtts.ubound = 1e37
        SetOperatorOptions(IsoTempAtts, 0)  # First (and only) operator

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
    legend.drawMinMax = 0
    legend.numberFormat = "%1.1f"

    if params["plotting.contour.on"]:
        AddPlot("Contour", params["plotting.contour.var.name"], 1, 1)
        ContourAtts = ContourAttributes()
        ContourAtts.contourMethod = ContourAtts.Value  # Explicitly set method
        ContourAtts.contourValue = params["plotting.contour.values"]  # Must be a tuple with trailing comma
        ContourAtts.minFlag = 0
        ContourAtts.maxFlag = 0
        ContourAtts.lineWidth = params["plotting.contour.linewidth"]
        ContourAtts.colorType = ContourAtts.ColorBySingleColor
        ContourAtts.singleColor = params["plotting.contour.color"]
        ContourAtts.legendFlag = 0
        SetPlotOptions(ContourAtts)

        # if params["plotting.main_plotting_var.thresholding.on"]:
            # AddOperator("Threshold")
            # SetOperatorOptions(Thresh)
    DrawPlots()

    SaveWindowAtts.fileName = "temp_field_DELETE_ME"
    SetSaveWindowAttributes(SaveWindowAtts)
    SaveWindow()

AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes2D.visible = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.legendInfoFlag = 0
AnnotationAtts.backgroundColor = (255, 255, 255, 255)
AnnotationAtts.foregroundColor = (0, 0, 0, 255)
SetAnnotationAttributes(AnnotationAtts)

SetTimeSliderState(1)
AddPlot("Pseudocolor", plotting_var, 1, 1)
SizePlot = PseudocolorAttributes()
SizePlot.minFlag = 1
SizePlot.min = 0
SizePlot.maxFlag = 1
SizePlot.max = 1
SizePlot.colorTableName = "hot"
SizePlot.invertColorTable = 0
SizePlot.legendFlag = 0
SetPlotOptions(SizePlot)
DrawPlots()

SaveWindowAtts.fileName = "size_plot_DELETE_ME"
SetSaveWindowAttributes(SaveWindowAtts)
SaveWindow()
DeleteActivePlots()

params["sim.type"] = "gif_images"

save_metadata_with_git(params, ".")
sys.exit(0)
