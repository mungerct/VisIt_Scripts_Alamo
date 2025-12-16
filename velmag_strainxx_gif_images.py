#!/usr/bin/env python
"""
VisIt visualization script for exporting one image per time step,
drawing phi only where eta > 0.5, then overlaying stress_von_mises.
"""

import sys
import os

default_db = "celloutput.visit"

# If user supplied a path (e.g., running from elsewhere)
if len(sys.argv) > 1:
    db_path = sys.argv[1]
    if not db_path.endswith(default_db):
        db_path = os.path.join(db_path, default_db)
else:
    db_path = os.path.join(os.getcwd(), default_db)

# Normalize path
db_path = os.path.abspath(db_path)

if not os.path.exists(db_path):
    print("ERROR: Could not find celloutput.visit at:")
    print("   " + db_path)
    sys.exit(1)

print(f"Opening database: {db_path}")
OpenDatabase(db_path, 0)

# --- Create output folder based on last directory of the input path ---
# Example: /path/to/sim/output.scp.../celloutput.visit
# → folder name = "output.scp...”
parent_dir = os.path.dirname(db_path)
folder_name = os.path.basename(parent_dir)

output_dir = os.path.join(os.getcwd(), folder_name)

# Create directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")
else:
    print(f"Saving frames in existing directory: {output_dir}")

# --- Time setup ---
numStates = TimeSliderGetNStates()
print(f"Found {numStates} time steps")

start_state = 4
end_state = numStates
step_interval = 1

# --- Parameters ---
max_velmag = 20
max_strain_thres = 1.1
min_strain_thres = 1

# --- Convert to kPa ---
DefineScalarExpression(
    "Xstrain",
    "(strain_xx - 1)/10 + 1"
)

# --- Turn off axes, metadata, etc. ---
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes2D.visible = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.legendInfoFlag = 1
AnnotationAtts.backgroundColor = (255, 255, 255, 255)
AnnotationAtts.foregroundColor = (0, 0, 0, 255)
SetAnnotationAttributes(AnnotationAtts)

# --- velmag plot attributes ---
VelMagAtts = PseudocolorAttributes()
VelMagAtts.minFlag = 1
VelMagAtts.min = 0
VelMagAtts.maxFlag = 1
VelMagAtts.max = max_velmag
VelMagAtts.colorTableName = "Default"
VelMagAtts.legendFlag = 1
VelMagAtts.lightingFlag = 0

# --- Strain plot attributes ---
StrainAtts = PseudocolorAttributes()
StrainAtts.scaling = StrainAtts.Linear
StrainAtts.minFlag = 1
StrainAtts.min = min_strain_thres
StrainAtts.maxFlag = 1
StrainAtts.max = max_strain_thres
StrainAtts.colorTableName = "Default"
StrainAtts.opacityType = StrainAtts.FullyOpaque
StrainAtts.legendFlag = 1
StrainAtts.lightingFlag = 0

# --- Strain threshold attributes ---
StrainThresh = ThresholdAttributes()
StrainThresh.outputMeshType = 0
StrainThresh.boundsInputType = 0
StrainThresh.listedVarNames = ("Xstrain", "eta")
StrainThresh.zonePortions = (1, 1)
StrainThresh.lowerBounds = (-1e+37, 0.5)
StrainThresh.upperBounds = (1e+37, 1e+37)
StrainThresh.defaultVarName = "Xstrain"
StrainThresh.defaultVarIsScalar = 1
StrainThresh.boundsRange = ("-1e+37:1e+37", "0.5:1e+37")

# --- Velamg threshold attributes ---
VelMagThresh = ThresholdAttributes()
VelMagThresh.outputMeshType = 0
VelMagThresh.boundsInputType = 0
VelMagThresh.listedVarNames = ("velocity_magnitude", "eta")
VelMagThresh.zonePortions = (1, 1)
VelMagThresh.lowerBounds = (-1e37, -1e37)
VelMagThresh.upperBounds = (1e+37, 0.5)
VelMagThresh.defaultVarName = "velocity_magnitude"
VelMagThresh.defaultVarIsScalar = 1
VelMagThresh.boundsRange = ("1e+37:1e+37", "-1e+37:0.5")

print("Beginning frame-by-frame export...")

# --- Loop through timesteps and export ---
for state in range(start_state, end_state, step_interval):

    print(f"Processing frame at timestep {state}/{end_state}")
    SetTimeSliderState(state)

    # Clear all plots
    DeleteAllPlots()

    # === 1. Draw relative gas density where eta < 0.5 ===
    AddPlot("Pseudocolor", "velocity_magnitude")
    AddOperator("Threshold")
    SetOperatorOptions(VelMagThresh)
    SetPlotOptions(VelMagAtts)

    # Draw Legend
    LegendPlotAtts = PseudocolorAttributes()
    LegendPlotAtts.minFlag = 1
    LegendPlotAtts.min = 0
    LegendPlotAtts.maxFlag = 1
    LegendPlotAtts.max = max_velmag
    LegendPlotAtts.colorTableName = "Default"
    LegendPlotAtts.legendFlag = 1  # Show the legend
    LegendPlotAtts.lightingFlag = 0
    SetPlotOptions(LegendPlotAtts)
    DrawPlots()

    # Customize legend appearance
    legend = GetAnnotationObject(GetPlotList().GetPlots(0).plotName)
    legend.xScale = 1.0
    legend.yScale = 1.5
    legend.orientation = legend.VerticalRight
    legend.managePosition = 0
    legend.position = (0.0, 0.9)
    legend.fontHeight = 0.03
    legend.drawTitle = 0
    legend.numberFormat = "%1.1f"
    legend.drawMinMax = 0

    DrawPlots()
    # === 2. Draw X direction strain wehere eta > 0.5 ===
    AddPlot("Pseudocolor", "Xstrain")
    SetPlotOptions(StrainAtts)
    AddOperator("Threshold")
    SetOperatorOptions(StrainThresh)

    # Draw Legend
    LegendPlotAtts = PseudocolorAttributes()
    LegendPlotAtts.minFlag = 1
    LegendPlotAtts.min = min_strain_thres
    LegendPlotAtts.maxFlag = 1
    LegendPlotAtts.max = max_strain_thres
    LegendPlotAtts.colorTableName = "bluehot"
    LegendPlotAtts.legendFlag = 1  # Show the legend
    LegendPlotAtts.lightingFlag = 0
    SetPlotOptions(LegendPlotAtts)
    DrawPlots()

    # Customize legend appearance
    legend = GetAnnotationObject(GetPlotList().GetPlots(1).plotName)
    legend.xScale = 1.0
    legend.yScale = 1.5
    legend.orientation = legend.VerticalRight
    legend.managePosition = 0
    legend.position = (0.0, 0.45)
    legend.fontHeight = 0.03
    legend.drawTitle = 0
    legend.numberFormat = "%1.1f"
    legend.drawMinMax = 0

    DrawPlots()

    # --- Save frame ---
    SaveWindowAtts = SaveWindowAttributes()
    SaveWindowAtts.outputToCurrentDirectory = 0
    SaveWindowAtts.outputDirectory = output_dir
    SaveWindowAtts.fileName = f"velamg_strainxx_{state:04d}"
    SaveWindowAtts.family = 0
    SaveWindowAtts.format = SaveWindowAtts.PNG
    SaveWindowAtts.width = 1080
    SaveWindowAtts.height = 1080
    SaveWindowAtts.screenCapture = 0
    SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
    SetSaveWindowAttributes(SaveWindowAtts)

    SaveWindow()

print("All frames exported! Ready to assemble into a GIF.")

sys.exit(0)