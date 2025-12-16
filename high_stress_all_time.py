#!/usr/bin/env python
"""
VisIt visualization script

Creates a composite visualization of von Mises stress evolution
across all time steps using layered isovolumes, restricted to
regions where eta > 0.5, overlaid on a static phi background.
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
print(f"Found {num_states} time steps")
step_interval  = 1

num_levels         = 1
min_stress         = 0.1
max_stress         = 0.6
invert_phi_colors  = 0

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

print("Adding phi background")
SetTimeSliderState(1)

AddPlot("Pseudocolor", "eta", 1, 1)
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
# Eta threshold (shared)
# -----------------------------------------------------------------------------

print("Building isovolume overlays...")

for (low, high) in stress_bands:
    print(f"  Stress band: {low:.2f} – {high:.2f}")

    # Stress isovolume
    StressIso = IsovolumeAttributes()
    StressIso.lbound   = low
    StressIso.ubound   = high*100
    StressIso.variable = "stress_von_mises"

    # Eta isovolume (mask)
    EtaIso = IsovolumeAttributes()
    EtaIso.lbound   = 0.5
    EtaIso.ubound   = 1e37
    EtaIso.variable = "eta"

    total_steps = len(range(0, num_states, step_interval))

    for i, state in enumerate(range(0, num_states, step_interval), start=1):
        percent = 100.0 * i / total_steps

        print(
            f"\rProcessing step {i}/{total_steps} "
            f"(state {state}/{num_states - 1}) "
            f"[{percent:5.1f}%]",
            end="",
            flush=True
        )

        SetTimeSliderState(state)

        AddPlot("Pseudocolor", "stress_von_mises", 1, 0)
        SetPlotOptions(StressPC)

        # Stress band selection
        AddOperator("Isovolume")
        SetOperatorOptions(StressIso)

        # Eta mask (second isovolume)
        AddOperator("Isovolume")
        SetOperatorOptions(EtaIso)

        SetActivePlots(GetNumPlots() - 1)
        SetPlotFollowsTime(0)


# -----------------------------------------------------------------------------
# Draw everything
# -----------------------------------------------------------------------------

print("\n Rendering plots...")
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
legend.orientation    = legend.VerticalRight
legend.managePosition = 0
legend.position       = (0.0, 0.9)
legend.fontHeight     = 0.03
legend.drawTitle      = 0
legend.numberFormat   = "%1.1f"

# -----------------------------------------------------------------------------
# Save image
# -----------------------------------------------------------------------------

SaveAtts = SaveWindowAttributes()
SaveAtts.outputToCurrentDirectory = 0
SaveAtts.outputDirectory          = output_dir
SaveAtts.fileName                 = "stress_von_mises_isovolume_eta_gt_0p5"
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
