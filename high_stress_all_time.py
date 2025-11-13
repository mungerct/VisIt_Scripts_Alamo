
#!/usr/bin/env python
"""
VisIt visualization script for overlaying stress plots across all time steps
Creates a composite view of von Mises stress evolution with threshold filters
"""
import numpy as np

# Open the database
OpenDatabase("localhost:/home/mungerct/research/alamo/output.scpsphereselastic.old.coarse_mesh3/celloutput.visit", 0)

# Save session for crash recovery
SaveSession("/home/mungerct/.visit/crash_recovery.695408.session")

# Define custom expression for von Mises stress (scaled by 1/10)
DefineScalarExpression("stress_von_mesis", 
                       "sqrt(stress_xx^2+stress_yy^2-stress_xx*stress_yy+3*stress_xy^2)/10")

# Get the number of time steps
numStates = TimeSliderGetNStates()
print(f"Found {numStates} time steps")

# Optional: Sample every Nth timestep to reduce processing time
step_interval = 10  # Change to 5, 10, etc. to skip timesteps
start_state = 0
end_state = numStates
num_levels = 4  # Number of "levels" of the stress that are plotted
min_stress_thres = 10  # Minimum stress threshold
max_stress_thres = 25  # Maximum stress threshold

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
PhiAtts.invertColorTable = 0
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

# Loop over stress levels and time steps
for level in np.linspace(min_stress_thres, max_stress_thres, num_levels):
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
SaveWindowAtts.outputToCurrentDirectory = 1
SaveWindowAtts.outputDirectory = "."
SaveWindowAtts.fileName = "stress_von_mises_all_timesteps"
SaveWindowAtts.family = 1
SaveWindowAtts.format = SaveWindowAtts.PNG
SaveWindowAtts.width = 1024
SaveWindowAtts.height = 1024
SaveWindowAtts.screenCapture = 0
SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
SetSaveWindowAttributes(SaveWindowAtts)
SaveWindow()

# Add one invisible plot just to show a single legend
print("Adding legend...")
AddPlot("Pseudocolor", "stress_von_mesis", 1, 1)
LegendPlotAtts = PseudocolorAttributes()
LegendPlotAtts.minFlag = 1
LegendPlotAtts.min = min_stress_thres
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
