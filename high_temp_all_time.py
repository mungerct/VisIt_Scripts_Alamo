#!/usr/bin/env python
"""
VisIt visualization script

Creates a composite visualization of temperature evolution
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
# Global parameters
# -----------------------------------------------------------------------------

num_states     = TimeSliderGetNStates()
step_interval = 1

num_levels = 6
min_temp   = 1000
max_temp   = 2000
# end_state = num_states
end_state = 125

invert_phi_colors = 0

print(f"Found {num_states} time steps")

# -----------------------------------------------------------------------------
# Compute temperature bands
# -----------------------------------------------------------------------------

if num_levels > 1:
    band_width = (max_temp - min_temp) / num_levels
    temp_bands = [
        (min_temp + i * band_width,
         min_temp + (i + 1) * band_width)
        for i in range(num_levels)
    ]
else:
    temp_bands = [(min_temp, max_temp)]

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
# Temperature plot attributes (shared)
# -----------------------------------------------------------------------------

TempPC = PseudocolorAttributes()
TempPC.scaling          = TempPC.Linear
TempPC.limitsMode       = TempPC.OriginalData
TempPC.minFlag          = 1
TempPC.min              = min_temp
TempPC.maxFlag          = 1
TempPC.max              = max_temp
TempPC.colorTableName   = "Default"
TempPC.opacityType      = TempPC.FullyOpaque
TempPC.legendFlag       = 0
TempPC.lightingFlag     = 0

# -----------------------------------------------------------------------------
# Build layered isovolume overlays
# -----------------------------------------------------------------------------

print("Building temperature isovolume overlays...")

for (low, high) in temp_bands:
    print(f"\nTemperature band: {low:.2f} – {high:.2f}")

    # Temperature isovolume
    TempIso = IsovolumeAttributes()
    TempIso.lbound   = low
    TempIso.ubound   = high
    TempIso.variable = "temp"

    # Eta mask isovolume
    EtaIso = IsovolumeAttributes()
    EtaIso.lbound   = 0.5
    EtaIso.ubound   = 1e37
    EtaIso.variable = "eta"

    states = list(range(0, end_state, step_interval))
    total_steps = len(states)

    for i, state in enumerate(states, start=1):
        percent = 100.0 * i / total_steps

        print(
            f"\r  Processing {i}/{total_steps} "
            f"(state {state}/{end_state - 1}) "
            f"[{percent:5.1f}%]",
            end="",
            flush=True
        )

        SetTimeSliderState(state)

        AddPlot("Pseudocolor", "temp", 1, 0)
        SetPlotOptions(TempPC)

        # Temperature band
        AddOperator("Isovolume")
        SetOperatorOptions(TempIso)

        # Eta mask
        AddOperator("Isovolume")
        SetOperatorOptions(EtaIso)

        SetActivePlots(GetNumPlots() - 1)
        SetPlotFollowsTime(0)

    print("")  # newline after each band

# -----------------------------------------------------------------------------
# Draw everything
# -----------------------------------------------------------------------------

print("\nRendering plots...")
DrawPlots()

# -----------------------------------------------------------------------------
# Legend-only plot
# -----------------------------------------------------------------------------

print("Adding legend")

AddPlot("Pseudocolor", "temp", 1, 1)

LegendPC = PseudocolorAttributes()
LegendPC.minFlag        = 1
LegendPC.min            = min_temp
LegendPC.maxFlag        = 1
LegendPC.max            = max_temp
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
SaveAtts.fileName                 = "temp_isovolume_eta_gt_0p5"
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
