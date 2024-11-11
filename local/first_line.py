#!/usr/bin/env python3

import subprocess 
import numpy as np
import os 
import sys 
import re
 
def run_stage(U,int_dir):
    os.chdir(int_dir)
    run1=subprocess.run(['tar -xf GaAs.base.tar'],shell=True)
    list_1=os.listdir()
    list_in=[]
    for item in list_1:
        if '.in' in item:
            list_in.append(item)
    for infile in list_in:
        with open(infile,'r') as fi:
            s=fi.read()
        s=re.sub('<%s>'%'Ga-4p',str(U['Ga-4p']),s)
        s=re.sub('<%s>'%'As-4p',str(U['As-4p']),s)
        with open(infile,'w') as fo:
            fo.write(s)
    
    run2=subprocess.run(['srun --mpi=pmi2 -n ${SLURM_NPROCS} pw.x -i %s > %s'%('GaAs.relax.in','GaAs.relax.out')],shell=True)
    data={}
    os.chdir('..')

#def extract_stage_data(int_dir):




if __name__=="__main__":

    run_stage({'Ga-4p':5,'As-4p':3},'test1')
