#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt 
from local.stage_functions import run_stage,extract_stage_data
from local.meff import meff_kpoints_eigenvalues,get_xml_info
import sys 

def main(bina,keys,start,stop,step):
    U1={keys[0]:-5,keys[1]:3}
    ylist=np.arange(start,stop,step)
    data_file='data_%s.csv'%bina 
    with open(data_file,'w') as fd:
        fd.write('U_%s,U_%s,a(A),Eg(eV),meff\n'%tuple(keys))
    
    for y in ylist:
        U1[keys[1]]=y
        run_stage(U1,keys,bina,bina)
        data_out=extract_stage_data(bina,bina)
        with open(data_file,'a') as fd:
            fd.write("%s,%s,%s,%s,%s\n"%(U1[keys[0]],U1[keys[1]],data_out['a'],data_out['Eg'],data_out['meff']))
        print('here')

if __name__=='__main__':
    args=sys.argv[1:]
    bina=args[0]
    U1={args[1]:-5,args[2]:3}
    keys=[args[1],args[2]]
    ylist=np.arange(float(args[3]),float(args[4]),float(args[5]))
    start=float(args[3])
    stop=float(args[4])
    step=float(args[5])
    main(bina,keys,start,stop,step)
    '''
    data_file='data_%s.csv'%bina 
    with open(data_file,'w') as fd:
        fd.write('U_%s,U_%s,a(A),Eg(eV),meff\n'%tuple(keys))
    

    for y in ylist:
        U1[keys[1]]=y
        run_stage(U1,keys,bina,bina)
        data_out=extract_stage_data(bina,bina)
        with open(data_file,'a') as fd:
            fd.write("%s,%s,%s,%s,%s\n"%(U1[keys[0]],U1[keys[1]],data_out['a'],data_out['Eg'],data_out['meff']))
        print('here')'''