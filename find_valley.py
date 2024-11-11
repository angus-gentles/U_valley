#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt 
from local.stage_functions import run_stage,extract_stage_data
from local.meff import meff_kpoints_eigenvalues,get_xml_info

class TransGroup :
    def __init__(self):
        self.members=np.array([[0.01,0.0],[-0.01,0.],[0.,0.01],[0.,-0.01]])

    def apply(self,r):
        output=[]
        for g in self.members:
            output.append(r+g)
        output=np.array(output)
        return output

transgroup=TransGroup()
Eg_exp={'GaAs':1.519,'InAs':0.417,'GaSb':0.812,'InSb':0.235}


def stage(r,old_point):
    U={}
    r_group=transgroup.apply(r)
    same=np.logical_not(np.logical_and(np.isclose(r_group,old_point)[:,0],np.isclose(r_group,old_point)[:,1]))
    new_points=r_group[same]
    print('new points:',new_points)
    Egs=[]
    meffs=[]
    latts=[]
    data_out_list=[]
    del_Eg=3.0
    for i,point in enumerate(new_points):
        U['Ga-4p']=point[0]
        U['As-4p']=point[1]
        run_stage(U,['Ga-4p','As-4p'],'GaAs')
        data_out1=extract_stage_data('GaAs','GaAs')
        Egs.append(data_out1['Eg'])
        meffs.append(data_out1['meff'])
        latts.append(data_out1['a'])
        del_Eg_new=np.abs(data_out1['Eg']-Eg_exp['GaAs'])
        #print(point,data_out1['Eg'])
        if del_Eg_new<del_Eg:
            lowest_ind=i
            del_Eg=del_Eg_new
    print(new_points)
    print(Egs)
    data_out_new={'Eg':Egs[lowest_ind],'meff':meffs[lowest_ind],'a':latts[lowest_ind]}
    r_new=new_points[lowest_ind]
    return r_new,data_out_new

if __name__=='__main__':
    data_file='data_GaAs.csv'
    with open(data_file,'w') as fd:
        fd.write('U_%s,U_%s,a(A),Eg(eV),meff\n'%('Ga-4p','As-4p'))

    r_start=np.array([-5,6.34])
    old_point=np.array([-5.01,6.34])

    run_stage({'Ga-4p':r_start[0],'As-4p':r_start[1]},['Ga-4p','As-4p'],'GaAs')
    data_out=extract_stage_data('GaAs','GaAs')
    with open(data_file,'a') as fd:
        fd.write("%s,%s,%s,%s,%s\n"%(r_start[0],r_start[1],data_out['a'],data_out['Eg'],data_out['meff']))

    iterations=3
    for i in range(iterations):
        r_new,data_out_new=stage(r_start,old_point)
        r_new=np.round(r_new,2)
        with open(data_file,'a') as fd:
            fd.write("%s,%s,%s,%s,%s\n"%(r_new[0],r_new[1],data_out_new['a'],data_out_new['Eg'],data_out_new['meff']))
        old_point=r_start
        r_start=r_new 
