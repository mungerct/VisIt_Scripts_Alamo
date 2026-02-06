#!/usr/bin/env bash
#SBATCH --time=1:00:00                                                                                                                                                                 
#SBATCH --nodes=1                                                                                                                                                                       
#SBATCH --ntasks-per-node=16                                                                                                                                                            
#SBATCH --mem-per-cpu=1000                                                                                                                                                             
#SBATCH --job-name="high_var"                                                                                                                                                              
#SBATCH --output="%x-%j-log.txt"                                                                                                                                                        
#SBATCH --mail-user=mungerct@iastate.edu                                                                                                                                                
#SBATCH --mail-type=BEGIN,END,FAIL 

echo "======================================================"
echo " Job '$SLURM_JOB_NAME' (ID: $SLURM_JOB_ID) is starting"
echo " Submitted by: $SLURM_JOB_USER"
echo " Running on node(s): $SLURM_NODELIST"
echo " Start time: $(date)"
echo "======================================================"

INPUT_FILE=$1

module load lammps-cpu/2025.07.22-stable-openmpi4.1.2
module load visit/3.4.1-py311-openmpi4-gns5n4x
module load openmpi_hpc
module load python/3.11.9-i2aasxp
module load numpy 
srun visit -cli -np 16 -nowin -s ../src/high_var_all_time.py "$INPUT_FILE"