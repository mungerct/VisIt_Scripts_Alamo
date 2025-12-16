#!/usr/bin/env python
"""
VisIt visualization script

Creates a composite visualization of von Mises stress evolution
across all time steps using layered isovolumes, overlaid on a
static phi background.
"""

import sys
import os

# -----------------------------------------------------------------------------
# Database handling
# -----------------------------------------------------------------------------

DEFAULT_DB = "celloutput.visit"

if len(sys.argv) > 1:
    db_path = sys.argv[1]
    if not db_path.endswith(DEFAULT_DB):
        db_path = os.path.join(db_path, DEFAULT_DB)
else:
    db_path = os.path.join(os.getcwd(), DEFAULT_DB)

db_path = os.path.abspath(db_path)

if not os.path.exists(db_path):
    print("ERROR: Could not find database:")
    print("  ", db_path)
    sys.exit(1)

print(f"Opening database: {db_path}")
OpenDatabase(db_path, 0)

# Output directory named after simulation folder
parent_dir = os.path.dirname(db_path)
output_dir = os.path.join(os.getcwd(), os.path.basename(parent_dir))

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# -----------------------------------------------------------------------------
# Expressions
# -----------------------------------------------------------------------------

DefineScalarExpression(
    "stress_von_mises",
    "sqrt(stress_xx^2 + stress_yy^2 - stress_xx*stress_yy + 3*stress_xy^2) / 10"
)

# -----------------------------------------------------------------------------
# Global parameters
# -----------------------------------------------------------------------------

num_states      = TimeSliderGetNStates()
step_interval  = 10

num_levels         = 3
min_stress         = 0.1
max_stress         = 100
invert_phi_colors  = 0

print(f"Found {num_states} time steps")

# Compute stress bands
if num_levels > 1:
    band_width = (max_stress - min_stress) / num_levels
    stress_bands = [
        (min_stress + i * band_width,
         min_stress + (i + 1) * band_width)
        for i in range(num_levels)
    ]
else:
    stress_bands = [(min_stress, max_stress)]

# -----------------------------------------------------------------------------
# Annotation settings
# -----------------------------------------------------------------------------

Ann = AnnotationAttributes()
Ann.axes2D.visible        = 0
Ann.userInfoFlag          = 0
Ann.databaseInfoFlag      = 0
Ann.timeInfoFlag          = 0
Ann.legendInfoFlag        = 1
Ann.backgroundColor       = (255, 255, 255, 255)
Ann.foregroundColor       = (0, 0, 0, 255)
SetAnnotationAttributes(Ann)

# -----------------------------------------------------------------------------
# Static phi background (single timestep)
# -----------------------------------------------------------------------------

print("Adding phi background (timestep 50)")
SetTimeSliderState(50)

AddPlot("Pseudocolor", "phi", 1, 1)
SetPlotFollowsTime(0)

PhiAtts = PseudocolorAttributes()
PhiAtts.minFlag           = 1
PhiAtts.min               = 0
PhiAtts.maxFlag           = 1
PhiAtts.max               = 1
PhiAtts.colorTableName    = "gray"
PhiAtts.invertColorTable  = invert_phi_colors
PhiAtts.legendFlag        = 0
PhiAtts.lightingFlag      = 0
SetPlotOptions(PhiAtts)

# -----------------------------------------------------------------------------
# Stress plot attributes (shared)
# -----------------------------------------------------------------------------

StressPC = PseudocolorAttributes()
StressPC.scaling          = StressPC.Linear
StressPC.limitsMode       = StressPC.OriginalData
StressPC.minFlag          = 1
StressPC.min              = 0
StressPC.maxFlag          = 1
StressPC.max              = max_stress
StressPC.colorTableName   = "Default"
StressPC.opacityType      = StressPC.FullyOpaque
StressPC.legendFlag       = 0
StressPC.lightingFlag     = 0

# -----------------------------------------------------------------------------
# Build layered isovolume overlays
# -----------------------------------------------------------------------------

print("Building isovolume overlays...")

for (low, high) in stress_bands:
    print(f"  Stress band: {low:.2f} – {high:.2f}")

    IsoAtts = IsovolumeAttributes()
    IsoAtts.lbound   = low
    IsoAtts.ubound   = high
    IsoAtts.variable = "stress_von_mises"

    for state in range(0, num_states, step_interval):
        SetTimeSliderState(state)

        AddPlot("Pseudocolor", "stress_von_mises", 1, 0)
        SetPlotOptions(StressPC)

        AddOperator("Isovolume")
        SetOperatorOptions(IsoAtts)

        SetActivePlots(GetNumPlots() - 1)
        SetPlotFollowsTime(0)

# -----------------------------------------------------------------------------
# Draw everything
# -----------------------------------------------------------------------------

print("Rendering plots...")
DrawPlots()

# -----------------------------------------------------------------------------
# Legend-only plot
# -----------------------------------------------------------------------------

print("Adding legend")

AddPlot("Pseudocolor", "stress_von_mises", 1, 1)

LegendPC = PseudocolorAttributes()
LegendPC.minFlag        = 1
LegendPC.min            = 0
LegendPC.maxFlag        = 1
LegendPC.max            = max_stress
LegendPC.colorTableName = "Default"
LegendPC.opacity        = 0
LegendPC.legendFlag     = 1
LegendPC.lightingFlag   = 0
SetPlotOptions(LegendPC)

DrawPlots()

legend = GetAnnotationObject(
    GetPlotList().GetPlots(GetNumPlots() - 1).plotName
)
legend.orientation   = legend.VerticalRight
legend.managePosition = 0
legend.position      = (0.0, 0.9)
legend.fontHeight    = 0.03
legend.drawTitle     = 0
legend.numberFormat  = "%1.1f"

# -----------------------------------------------------------------------------
# Save image
# -----------------------------------------------------------------------------

SaveAtts = SaveWindowAttributes()
SaveAtts.outputToCurrentDirectory = 0
SaveAtts.outputDirectory          = output_dir
SaveAtts.fileName                 = "stress_von_mises_isovolume_overlay"
SaveAtts.family                   = 0
SaveAtts.format                   = SaveAtts.PNG
SaveAtts.width                    = 4000
SaveAtts.height                   = 4000
SaveAtts.screenCapture            = 0
SaveAtts.resConstraint            = SaveAtts.NoConstraint
SetSaveWindowAttributes(SaveAtts)

SaveWindow()

print("Image saved successfully.")
sys.exit(0)

'''
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
step_interval = 2  # Change to 5, 10, etc. to skip timesteps
start_state = 0
end_state = numStates
# end_state = 500
num_levels = 5  # Number of "levels" of the stress that are plotted
min_stress_thres = 12.5 # Minimum stress threshold
max_stress_thres = 25  # Maximum stress threshold
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

    # Loop over all time steps
    for state in range(start_state, end_state, step_interval):
        print(f"Setting up time step {state + 1}/{numStates} at stress level {level:.2f}")
        
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
'''