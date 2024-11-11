#!/usr/bin/env bash
#SBATCH -J UvalIA
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --output=IA_Uv.txt
#SBATCH --partition=zen3_0512
#SBATCH --qos=zen3_0512
#SBATCH --time 2-00:00:00

source setup_conda.sh
conda activate alloy_bayes
source ~/tools/setup_data_qe7.3.1.sh
export I_MPI_PMI_LIBRARY=/opt/sw/slurm/x86_64/alma8.8/22-05-2-1/lib/libpmi.so
./find_valley.py InAs In-5p As-4p -5.0 4.36 -5.01 4.36 
