#!/usr/bin/env bash
#SBATCH -J UvalGA
#SBATCH -N 1
#SBATCH --output=GA_Uv.txt
#SBATCH --partition=zen3_0512
#SBATCH --qos=zen3_0512
#SBATCH --time 1-00:00:00

source setup_conda.sh
conda activate alloy_bayes
source ~/tools/setup_data_qe7.3.1.sh
export I_MPI_PMI_LIBRARY=/opt/sw/slurm/x86_64/alma8.8/22-05-2-1/lib/libpmi.so
./find_valley.py GaAs Ga-4p As-4p -5.0 6.34 -5.01 6.34 
