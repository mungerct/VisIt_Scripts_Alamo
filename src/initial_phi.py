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

# --- Parameter ---
state = 10

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

# --- Stress plot attributes ---
PhiAtts = PseudocolorAttributes()
PhiAtts.scaling = PhiAtts.Linear
PhiAtts.minFlag = 1
PhiAtts.min = 0
PhiAtts.maxFlag = 1
PhiAtts.max = 1
PhiAtts.colorTableName = "Default"
PhiAtts.opacityType = PhiAtts.FullyOpaque
PhiAtts.legendFlag = 1
PhiAtts.lightingFlag = 0

SetTimeSliderState(state)

# Clear all plots
DeleteAllPlots()

# === 1. Draw relative gas density where eta < 0.5
AddPlot("Pseudocolor", "phi")

# Draw Legend
LegendPlotAtts = PseudocolorAttributes()
LegendPlotAtts.minFlag = 1
LegendPlotAtts.min = 0
LegendPlotAtts.maxFlag = 1
LegendPlotAtts.max = 1
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
legend.fontHeight = 0.06
legend.drawTitle = 0
legend.numberFormat = "%1.1f"
legend.drawMinMax = 0

DrawPlots()


# --- Save frame ---
SaveWindowAtts = SaveWindowAttributes()
SaveWindowAtts.outputToCurrentDirectory = 0
SaveWindowAtts.outputDirectory = output_dir
SaveWindowAtts.fileName = f"initial_phi"
SaveWindowAtts.family = 0
SaveWindowAtts.format = SaveWindowAtts.PNG
SaveWindowAtts.width = 4000
SaveWindowAtts.height = 4000
SaveWindowAtts.screenCapture = 0
SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
SetSaveWindowAttributes(SaveWindowAtts)

SaveWindow()
sys.exit(0)