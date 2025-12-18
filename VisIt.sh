#!/usr/bin/env bash
#SBATCH --job-name="VisIt"            # Job name
#SBATCH --output=visit_job.%j.out     # Standard output log
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --time=1:00:00                # Max walltime (hh:mm:ss)
#SBATCH --mail-user=mungerct@iastate.edu
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

# Load any necessary modules
module load visit/3.4.1-py311-openmpi4-gns5n4x

# Run Visit in parallel
visit -cli -nowin -np 36 -s high_temp_all_time.py /home/brunnels/mungerct/alamo/output.scpthermalIAstate.old.nova_small_flame_eps/
