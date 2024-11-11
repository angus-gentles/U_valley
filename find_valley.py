#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt 
from local.stage_functions import run_stage,extract_stage_data
from local.meff import meff_kpoints_eigenvalues,get_xml_info
import sys

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


def stage(r,old_point,keys,bina):
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
        U[keys[0]]=point[0]
        U[keys[1]]=point[1]
        run_stage(U,keys,bina,bina)
        data_out1=extract_stage_data(bina,bina)
        Egs.append(data_out1['Eg'])
        meffs.append(data_out1['meff'])
        latts.append(data_out1['a'])
        del_Eg_new=np.abs(data_out1['Eg']-Eg_exp[bina])
        #print(point,data_out1['Eg'])
        if del_Eg_new<del_Eg:
            lowest_ind=i
            del_Eg=del_Eg_new
    print(new_points)
    print(Egs)
    data_out_new={'Eg':Egs[lowest_ind],'meff':meffs[lowest_ind],'a':latts[lowest_ind]}
    r_new=new_points[lowest_ind]
    return r_new,data_out_new

def main(bina,keys,r_start,old_point):
    data_file='data_%s.csv'%bina
    with open(data_file,'w') as fd:
        fd.write('U_%s,U_%s,a(A),Eg(eV),meff\n'%tuple(keys))
    run_stage({keys[0]:r_start[0],keys[1]:r_start[1]},keys,bina,bina)
    data_out=extract_stage_data(bina,bina)
    with open(data_file,'a') as fd:
        fd.write("%s,%s,%s,%s,%s\n"%(r_start[0],r_start[1],data_out['a'],data_out['Eg'],data_out['meff']))

    iterations=2000
    for i in range(iterations):
        r_new,data_out_new=stage(r_start,old_point,keys,bina)
        r_new=np.round(r_new,2)
        with open(data_file,'a') as fd:
            fd.write("%s,%s,%s,%s,%s\n"%(r_new[0],r_new[1],data_out_new['a'],data_out_new['Eg'],data_out_new['meff']))
        old_point=r_start
        r_start=r_new 

if __name__=='__main__':
    args=sys.argv[1:]
    bina=args[0]
    keys=[args[1],args[2]]
    r_start=np.array([float(args[3]),float(args[4])])
    old_point=np.array([float(args[5]),float(args[6])])
    main(bina,keys,r_start,old_point)
