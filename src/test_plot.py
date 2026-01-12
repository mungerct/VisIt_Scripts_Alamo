#!/usr/bin/env python
"""
VisIt visualization script for stress analysis
Plots von Mises stress with threshold filter
"""

# Open the database
OpenDatabase("localhost:/home/mungerct/research/alamo/output.scpsphereselastic.old.coarse_mesh3/celloutput.visit", 0)

# Save session for crash recovery
SaveSession("/home/mungerct/.visit/crash_recovery.695408.session")

# Define custom expression for von Mises stress
DefineScalarExpression("stress_von_mesis", 
                       "sqrt(stress_xx^2+stress_yy^2-stress_xx*stress_yy+3*stress_xy^2)")

# Add pseudocolor plot for von Mises stress
AddPlot("Pseudocolor", "stress_von_mesis", 1, 1)
DrawPlots()

# Add threshold operator
AddOperator("Threshold", 0)
SetActivePlots(0)

# Configure threshold attributes
ThresholdAtts = ThresholdAttributes()
ThresholdAtts.outputMeshType = 0
ThresholdAtts.boundsInputType = 0
ThresholdAtts.listedVarNames = ("default")
ThresholdAtts.zonePortions = (1)
ThresholdAtts.lowerBounds = (12.5)
ThresholdAtts.upperBounds = (1e+37)
ThresholdAtts.defaultVarName = "stress_von_mesis"
ThresholdAtts.defaultVarIsScalar = 1
ThresholdAtts.boundsRange = ("12.5:1e+37")

# Apply threshold operator
SetOperatorOptions(ThresholdAtts, 0, 0)
DrawPlots()

# Save the plot as an image in the current folder
SaveWindowAtts = SaveWindowAttributes()
SaveWindowAtts.outputToCurrentDirectory = 1
SaveWindowAtts.outputDirectory = "."
SaveWindowAtts.fileName = "stress_von_mises_plot"
SaveWindowAtts.family = 1
SaveWindowAtts.format = SaveWindowAtts.PNG
SaveWindowAtts.width = 1024
SaveWindowAtts.height = 1024
SaveWindowAtts.screenCapture = 0
SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
SetSaveWindowAttributes(SaveWindowAtts)
SaveWindow()