#!/usr/bin/env python
"""
VisIt visualization script for overlaying temperature plots across all time steps
Creates a composite view of temperature evolution with threshold filters
"""

import sys
import os

default_db = "celloutput.visit"

# If user supplied a path
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

# Create output folder based on last directory of the input path
parent_dir = os.path.dirname(db_path)
folder_name = os.path.basename(parent_dir)

output_dir = os.path.join(os.getcwd(), folder_name)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")
else:
    print(f"Saving frames in existing directory: {output_dir}")

# Temperature variable – assume it's named "temperature" in the database
temperature_var = "temp"

# Get number of time steps
numStates = TimeSliderGetNStates()
print(f"Found {numStates} time steps")

# Optional: Sample every Nth timestep to reduce processing time
step_interval = 10
start_state = 0
end_state = numStates

# Temperature levels and thresholds
num_levels = 3  # Number of temperature levels
min_temp_thres = 1000.0  # Minimum temperature threshold (adjust to your data)
max_temp_thres = 2000.0  # Maximum temperature threshold
invert_phi = 0  # Boolean to invert phi colormap

# Configure annotation settings
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes2D.visible = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.legendInfoFlag = 1
AnnotationAtts.backgroundColor = (255, 255, 255, 255)
AnnotationAtts.foregroundColor = (0, 0, 0, 255)
SetAnnotationAttributes(AnnotationAtts)

# Draw phi plot from timestep 50 as background
print("Drawing phi plot from timestep 1")
SetTimeSliderState(1)
AddPlot("Pseudocolor", "eta", 1, 1)
SetPlotFollowsTime(0)

# Configure phi plot with black and white colormap
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

print("Phi plot from timestep 50 configured")

# Configure plot attributes for temperature
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = min_temp_thres
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = max_temp_thres
PseudocolorAtts.colorTableName = "hot"  # Better for temperature
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque
PseudocolorAtts.legendFlag = 0
PseudocolorAtts.lightingFlag = 0

# Generate temperature levels
if num_levels > 1:
    step_size = (max_temp_thres - min_temp_thres) / (num_levels - 1)
    temp_levels = [min_temp_thres + i * step_size for i in range(num_levels)]
else:
    temp_levels = [min_temp_thres]

# Loop over temperature levels and time steps
for level in temp_levels:
    print(f"Processing temperature level {level:.2f}")
    
    ThresholdAtts = ThresholdAttributes()
    ThresholdAtts.outputMeshType = 0
    ThresholdAtts.boundsInputType = 0
    ThresholdAtts.listedVarNames = (temperature_var, "eta")
    ThresholdAtts.zonePortions = (1, 1)
    ThresholdAtts.lowerBounds = (level, 0.8)
    ThresholdAtts.upperBounds = (1e+37, 1e+37)
    ThresholdAtts.defaultVarName = temperature_var
    ThresholdAtts.defaultVarIsScalar = 1
    ThresholdAtts.boundsRange = (f"{level}:1e+37", "0.8:1e+37")

    for state in range(start_state, end_state, step_interval):
        print(f"Setting up time step {state + 1}/{numStates} at temperature level {level:.2f}")
        
        SetTimeSliderState(state)
        
        AddPlot("Pseudocolor", temperature_var, 1, 0)
        SetPlotOptions(PseudocolorAtts)
        
        AddOperator("Threshold")
        SetOperatorOptions(ThresholdAtts)
        
        SetActivePlots(GetNumPlots() - 1)
        SetPlotFollowsTime(0)

print("All time steps configured, drawing all plots...")
DrawPlots()

# Save the composite plot
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

# Add one invisible plot just to show a single legend
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

legend = GetAnnotationObject(GetPlotList().GetPlots(GetNumPlots() - 1).plotName)
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
