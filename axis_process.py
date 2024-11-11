#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt 
from local.stage_functions import run_stage,extract_stage_data
from local.meff import meff_kpoints_eigenvalues,get_xml_info


if __name__=='__main__':
    data_file='data_GaAs.csv'
    with open(data_file,'w') as fd:
        fd.write('U_%s,U_%s,a(A),Eg(eV),meff\n'%('Ga-4p','As-4p'))
    U1={'Ga-4p':-5,'As-4p':3}
    keys=['Ga-4p','As-4p']
    ylist=np.arange(6.3,6.4,0.01)
    for y in ylist:
        U1['As-4p']=y
        run_stage(U1,keys,'GaAs')
        data_out=extract_stage_data('GaAs','GaAs')
        with open(data_file,'a') as fd:
            fd.write("%s,%s,%s,%s,%s\n"%(U1['Ga-4p'],U1['As-4p'],data_out['a'],data_out['Eg'],data_out['meff']))
        print('here')