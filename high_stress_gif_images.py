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

# --- Expression for von Mises stress ---
DefineScalarExpression(
    "stress_von_mesis",
    "sqrt(stress_xx^2 + stress_yy^2 - stress_xx*stress_yy + 3*stress_xy^2) / 10"
)

# --- Time setup ---
numStates = TimeSliderGetNStates()
print(f"Found {numStates} time steps")

start_state = 4
end_state = numStates
step_interval = 1

# --- Parameters ---
min_stress_thres = 10.0
max_stress_thres = 25

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

# --- phi plot attributes ---
PhiAtts = PseudocolorAttributes()
PhiAtts.minFlag = 1
PhiAtts.min = 0
PhiAtts.maxFlag = 1
PhiAtts.max = 1
PhiAtts.colorTableName = "gray"
PhiAtts.legendFlag = 0
PhiAtts.lightingFlag = 0

# --- Stress plot attributes ---
VonAtts = PseudocolorAttributes()
VonAtts.scaling = VonAtts.Linear
VonAtts.minFlag = 1
VonAtts.min = 0
VonAtts.maxFlag = 1
VonAtts.max = max_stress_thres
VonAtts.colorTableName = "Default"
VonAtts.opacityType = VonAtts.FullyOpaque
VonAtts.legendFlag = 0
VonAtts.lightingFlag = 0

# --- Stress threshold attributes ---
StressThresh = ThresholdAttributes()
StressThresh.outputMeshType = 0
StressThresh.boundsInputType = 0
StressThresh.listedVarNames = ("stress_von_mesis", "eta")
StressThresh.zonePortions = (1, 1)
StressThresh.lowerBounds = (min_stress_thres, 0.5)
StressThresh.upperBounds = (1e+37, 1e+37)
StressThresh.defaultVarName = "stress_von_mesis"
StressThresh.defaultVarIsScalar = 1
StressThresh.boundsRange = (f"{min_stress_thres}:1e+37", "0.5:1e+37")

# --- phi threshold: draw phi only where eta > 0.5 ---
PhiThresh = ThresholdAttributes()
PhiThresh.outputMeshType = 0
PhiThresh.boundsInputType = 0
PhiThresh.listedVarNames = ("eta",)
PhiThresh.zonePortions = (1,)
PhiThresh.lowerBounds = (0.5,)      # eta > 0.5
PhiThresh.upperBounds = (1e+37,)    
PhiThresh.defaultVarName = "eta"
PhiThresh.defaultVarIsScalar = 1
PhiThresh.boundsRange = ("0.5:1e+37",)

print("Beginning frame-by-frame export...")

# --- Loop through timesteps and export ---
for state in range(start_state, end_state, step_interval):

    print(f"Processing frame at timestep {state}/{end_state}")
    SetTimeSliderState(state)

    # Clear all plots
    DeleteAllPlots()

    # === 1. Draw PHI where eta > 0.5 ===
    AddPlot("Pseudocolor", "phi")
    AddOperator("Threshold")
    SetOperatorOptions(PhiThresh)
    SetPlotOptions(PhiAtts)

    # === 2. Draw STRESS with threshold ===
    AddPlot("Pseudocolor", "stress_von_mesis")
    SetPlotOptions(VonAtts)

    AddOperator("Threshold")
    SetOperatorOptions(StressThresh)

    DrawPlots()

    # --- Save frame ---
    SaveWindowAtts = SaveWindowAttributes()
    SaveWindowAtts.outputToCurrentDirectory = 0
    SaveWindowAtts.outputDirectory = output_dir
    SaveWindowAtts.fileName = f"phi_highvonMises_gif_frame_{state:04d}"
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