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
max_rel_density = 2.5
max_stress_thres = 15
min_stress_thres = 0

# --- Convert to kPa ---
DefineScalarExpression(
    "Xstress",
    "stress_xx/10"
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

# --- density plot attributes ---
DenAtts = PseudocolorAttributes()
DenAtts.minFlag = 1
DenAtts.min = 1
DenAtts.maxFlag = 1
DenAtts.max = max_rel_density
DenAtts.colorTableName = "magma"
DenAtts.legendFlag = 1
DenAtts.lightingFlag = 0

# --- Stress plot attributes ---
StressAtts = PseudocolorAttributes()
StressAtts.scaling = StressAtts.Linear
StressAtts.minFlag = 1
StressAtts.min = 0
StressAtts.maxFlag = 1
StressAtts.max = max_stress_thres
StressAtts.colorTableName = "Default"
StressAtts.opacityType = StressAtts.FullyOpaque
StressAtts.legendFlag = 1
StressAtts.lightingFlag = 0

# --- Stress threshold attributes ---
StressThresh = ThresholdAttributes()
StressThresh.outputMeshType = 0
StressThresh.boundsInputType = 0
StressThresh.listedVarNames = ("Xstress", "eta")
StressThresh.zonePortions = (1, 1)
StressThresh.lowerBounds = (-1e+37, 0.5)
StressThresh.upperBounds = (1e+37, 1e+37)
StressThresh.defaultVarName = "Xstress"
StressThresh.defaultVarIsScalar = 1
StressThresh.boundsRange = ("-1e+37:1e+37", "0.5:1e+37")

# --- Stress threshold attributes ---
DenThresh = ThresholdAttributes()
DenThresh.outputMeshType = 0
DenThresh.boundsInputType = 0
DenThresh.listedVarNames = ("density", "eta")
DenThresh.zonePortions = (1, 1)
DenThresh.lowerBounds = (-1e37, -1e37)
DenThresh.upperBounds = (max_rel_density, 0.5)
DenThresh.defaultVarName = "density"
DenThresh.defaultVarIsScalar = 1
DenThresh.boundsRange = (f"{max_rel_density}:1e+37", "-s1e+37:0.5")

print("Beginning frame-by-frame export...")

# --- Loop through timesteps and export ---
for state in range(start_state, end_state, step_interval):

    print(f"Processing frame at timestep {state}/{end_state}")
    SetTimeSliderState(state)

    # Clear all plots
    DeleteAllPlots()

    # === 1. Draw relative gas density where eta < 0.5 ===
    AddPlot("Pseudocolor", "density")
    AddOperator("Threshold")
    SetOperatorOptions(DenThresh)
    SetPlotOptions(DenAtts)

    # Draw Legend
    LegendPlotAtts = PseudocolorAttributes()
    LegendPlotAtts.minFlag = 1
    LegendPlotAtts.min = 1
    LegendPlotAtts.maxFlag = 1
    LegendPlotAtts.max = max_rel_density
    LegendPlotAtts.colorTableName = "magma"
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
    legend.fontFamily = "times" 
    legend.drawTitle = 0
    legend.numberFormat = "%1.1f"
    legend.drawMinMax = 0

    DrawPlots()
    # === 2. Draw X direction stress wehere eta > 0.5 ===
    AddPlot("Pseudocolor", "Xstress")
    SetPlotOptions(StressAtts)
    AddOperator("Threshold")
    SetOperatorOptions(StressThresh)

    # Draw Legend
    LegendPlotAtts = PseudocolorAttributes()
    LegendPlotAtts.minFlag = 1
    LegendPlotAtts.min = 0
    LegendPlotAtts.maxFlag = 1
    LegendPlotAtts.max = max_stress_thres
    LegendPlotAtts.colorTableName = "Default"
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
    SaveWindowAtts.fileName = f"rel_density_stressXX_fig_frame_{state:04d}"
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