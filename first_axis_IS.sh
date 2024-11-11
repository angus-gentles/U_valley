#!/usr/bin/env bash
#SBATCH -J UaxIS
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --output=IS_Ua.txt
#SBATCH --partition=zen3_0512
#SBATCH --qos=zen3_0512_devel
#SBATCH --time 00:10:00

source setup_conda.sh
conda activate alloy_bayes
source ~/tools/setup_data_qe7.3.1.sh
export I_MPI_PMI_LIBRARY=/opt/sw/slurm/x86_64/alma8.8/22-05-2-1/lib/libpmi.so
./axis_process.py InSb In-5p Sb-5p 4.5 4.6 0.01
