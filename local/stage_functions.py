#!/usr/bin/env python3

import subprocess 
import numpy as np
import os 
import sys 
import glob
import re
import shutil
from local.xml_bandgap import get_Eg_xml,read_qe_xml_latt
from local.meff import get_xml_info,meff_kpoints_eigenvalues

def extract_base(input_string):
    if '.' in input_string:
        return '.'.join(input_string.split('.')[:-1])
    else:
        return input_string
    
def run_stage(U,keys,int_dir,bina):
    os.chdir(int_dir)
    run1=subprocess.run(['tar -xf %s.base.tar'%bina],shell=True)
    list_1=os.listdir()
    list_in=[]
    for item in list_1:
        if '.in' in item:
            list_in.append(item)
    for infile in list_in:
        with open(infile,'r') as fi:
            s=fi.read()
        for key in keys:
            s=re.sub('<%s>'%key,str(U[key]),s)
        #s=re.sub('<%s>'%'As-4p',str(U['As-4p']),s)
        with open(infile,'w') as fo:
            fo.write(s)
    
    for item in list_in:
        if 'relax.in' in item:
            base=extract_base(item)
            run2=subprocess.run(['srun --mpi=pmi2 -n ${SLURM_NPROCS} pw.x -i %s.in > %s.out'%(base,base)],shell=True)
    
    directory = 'tmp/*.save'
    pattern = 'wfc*.dat'
    for filename in glob.glob(os.path.join(directory, pattern)):
        os.remove(filename)
        #print(f"Deleted file: {filename}")
    
    subprocess.run(['rm -r ./meff/'],shell=True)
    shutil.copytree('tmp','meff')
    for item in list_in:
        if 'meff.in' in item:
            base=extract_base(item)
            run3=subprocess.run(['srun --mpi=pmi2 -n ${SLURM_NPROCS} pw.x -i %s.in > %s.out'%(base,base)],shell=True)

    #run2=subprocess.run(['srun --mpi=pmi2 -n ${SLURM_NPROCS} pw.x -i %s.in > %s.in'%(base,base)],shell=True)

    data={}
    os.chdir('..')

def extract_stage_data(bina,int_dir):
    os.chdir(int_dir)
    data_out={}
    Eg=get_Eg_xml('tmp/%s.xml'%bina)
    data_out['Eg']=get_Eg_xml('tmp/%s.xml'%bina)
    k_points,eigenvalues,a,occupations=get_xml_info('meff/%s'%('%s.xml'%bina))
    homo_i=int(int(np.sum(occupations[0]))-1)
    homo_i=13
    meff=meff_kpoints_eigenvalues(k_points,eigenvalues,a,homo_i+1)
    data_out['meff']=meff 
    a_ang=read_qe_xml_latt('tmp/%s.xml'%bina)
    data_out['a']=a_ang
    os.chdir('..')
    return data_out


if __name__=="__main__":
    #print(extract_base('GaAs.relax.in'))
    data_file='data_GaAs.csv'
    with open(data_file,'w') as fd:
        fd.write('U_%s,U_%s,a(A),Eg(eV),meff\n'%('Ga-4p','As-4p'))
    U1={'Ga-4p':5,'As-4p':3}
    keys=['Ga-4p','As-4p']
    run_stage(U1,keys,'test1')
    data_out=extract_stage_data('GaAs','test1')
    with open(data_file,'a') as fd:
        fd.write("%s,%s,%s,%s,%s\n"%(U1['Ga-4p'],U1['As-4p'],data_out['a'],data_out['Eg'],data_out['meff']))


    print(data_out)
    #run_stage({'Ga-4p':5,'As-4p':3},'test1')
