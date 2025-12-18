#!/bin/bash
#SBATCH --job-name=visit_job          # Job name
#SBATCH --output=visit_job.%j.out     # Standard output log
#SBATCH --error=visit_job.%j.err      # Standard error log
#SBATCH --ntasks=32                     # Number of tasks (MPI processes)
#SBATCH --cpus-per-task=1             # Number of CPU cores per task
#SBATCH --time=1:00:00               # Max walltime (hh:mm:ss)
#SBATCH --partition=compute           # Partition/queue name

# Load any necessary modules
module load visit/3.1.4               

# Navigate to your working directory
cd /home/mungerct/research/alamo/

# Run Visit in parallel
visit -cli -nowin -np 32 -s high_temp_all_time.py /home/mungerct/research/alamo/output.scpthermalIAstate.old.nova_small_flame_eps/
