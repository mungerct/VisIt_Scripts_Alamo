
#!/usr/bin/env python
"""
VisIt visualization script for overlaying stress plots across all time steps
Creates a composite view of von Mises stress evolution with threshold filters
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

# Define custom expression for von Mises stress (scaled by 1/10)
DefineScalarExpression("stress_von_mesis", 
                       "sqrt(stress_xx^2+stress_yy^2-stress_xx*stress_yy+3*stress_xy^2)/10")

# Get the number of time steps
numStates = TimeSliderGetNStates()
print(f"Found {numStates} time steps")

# Optional: Sample every Nth timestep to reduce processing time
step_interval = 5  # Change to 5, 10, etc. to skip timesteps
start_state = 0
# end_state = numStates
end_state = 150
num_levels = 4  # Number of "levels" of the stress that are plotted
min_stress_thres = 0.1  # Minimum stress threshold
max_stress_thres = 0.6  # Maximum stress threshold
invert_phi = 0 # Boolean to invert phi colormap

# Configure annotation settings - hide axes and other annotations
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes2D.visible = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.legendInfoFlag = 1
AnnotationAtts.backgroundColor = (255, 255, 255, 255)
AnnotationAtts.foregroundColor = (0, 0, 0, 255)
SetAnnotationAttributes(AnnotationAtts)

# Draw phi plot from the 50th time step as background
print("Drawing phi plot from timestep 50...")
SetTimeSliderState(50)
AddPlot("Pseudocolor", "phi", 1, 1)
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

# Configure plot attributes (applies to all stress plots)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = 0
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = max_stress_thres
PseudocolorAtts.colorTableName = "Default"
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque
PseudocolorAtts.legendFlag = 0
PseudocolorAtts.lightingFlag = 0

# Generate stress levels without numpy
if num_levels > 1:
    step_size = (max_stress_thres - min_stress_thres) / (num_levels - 1)
    stress_levels = [min_stress_thres + i * step_size for i in range(num_levels)]
else:
    stress_levels = [min_stress_thres]

# Loop over stress levels and time steps
for level in stress_levels:
    print(f"Processing stress level {level:.2f}")
    
    # Configure threshold attributes
    ThresholdAtts = ThresholdAttributes()
    ThresholdAtts.outputMeshType = 0
    ThresholdAtts.boundsInputType = 0
    ThresholdAtts.listedVarNames = ("stress_von_mesis", "eta")
    ThresholdAtts.zonePortions = (1, 1)
    ThresholdAtts.lowerBounds = (level, 0.5)
    ThresholdAtts.upperBounds = (1e+37, 1e+37)
    ThresholdAtts.defaultVarName = "stress_von_mesis"
    ThresholdAtts.defaultVarIsScalar = 1
    ThresholdAtts.boundsRange = (f"{level}:1e+37", "0.5:1e+37")

    total_steps = len(range(0, end_state, step_interval))

    # Loop over all time steps
    for state in range(start_state, end_state, step_interval):
        percent = 100.0 * state / end_state
        print(
            f"\r"
            f"state {state}/{end_state - 1} - "
            f"[{percent:5.1f}%]",
            end="",
            flush=True
        )
        
        SetTimeSliderState(state)
        
        AddPlot("Pseudocolor", "stress_von_mesis", 1, 0)
        SetPlotOptions(PseudocolorAtts)
        
        AddOperator("Threshold")
        SetOperatorOptions(ThresholdAtts)
        
        # Make the last-added plot active and lock it to current time
        SetActivePlots(GetNumPlots() - 1)
        SetPlotFollowsTime(0)

print("All time steps configured, drawing all plots...")

# Draw all plots at once
DrawPlots()

print("All time steps overlaid, preparing to save...")

# Save the composite plot as an image
SaveWindowAtts = SaveWindowAttributes()
SaveWindowAtts.outputToCurrentDirectory = 0
SaveWindowAtts.outputDirectory = output_dir
SaveWindowAtts.fileName = "stress_von_mises_all_timesteps"
SaveWindowAtts.family = 1
SaveWindowAtts.format = SaveWindowAtts.PNG
SaveWindowAtts.width = 4000
SaveWindowAtts.height = 4000
SaveWindowAtts.screenCapture = 0
SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
SetSaveWindowAttributes(SaveWindowAtts)

# Add one invisible plot just to show a single legend
print("Adding legend...")
AddPlot("Pseudocolor", "stress_von_mesis", 1, 1)
LegendPlotAtts = PseudocolorAttributes()
LegendPlotAtts.minFlag = 1
LegendPlotAtts.min = 0
LegendPlotAtts.maxFlag = 1
LegendPlotAtts.max = max_stress_thres
LegendPlotAtts.colorTableName = "Default"
LegendPlotAtts.opacity = 0  # Make it fully transparent
LegendPlotAtts.legendFlag = 1  # Show the legend
LegendPlotAtts.lightingFlag = 0
SetPlotOptions(LegendPlotAtts)
DrawPlots()

# Customize legend appearance
legend = GetAnnotationObject(GetPlotList().GetPlots(GetNumPlots() - 1).plotName)
legend.xScale = 1.0
legend.yScale = 2.0
legend.orientation = legend.VerticalRight
legend.managePosition = 0
legend.position = (0.0, 0.9)
legend.fontHeight = 0.03
legend.drawTitle = 0
legend.numberFormat = "%1.1f"

# Save final image with legend
SaveWindow()

print("Image saved successfully!")
sys.exit(0)