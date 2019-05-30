# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:00:20 2019

@author: lzt68
"""

from pyscipopt import Model
import numpy as np

demand_ch=np.array([15,5,7,10,0,15,20,10,0,8,2,16])
#demand_sh=np.array([40,4,4,14,38,20,0,16,4,32,0,0])
init_ch=17
init_sh=40
ch_in_unit_cost=2
sh_in_unit_cost=1
ch_pre=90
sh_pre=45

model = Model("MRP PLAN")

ch_order=[]
for i in range(10):
    ch_order.append(model.addVar('ch_'+str(i),vtype="INTEGER",lb=0)) #其实是默认大于0 
ch_bin=[] 
for i in range(10):
    ch_bin.append(model.addVar('ch_bin_'+str(i),vtype="BINARY"))
    
sh_order=[]
for i in range(7):
    sh_order.append(model.addVar('sh_'+str(i),vtype="INTEGER",lb=0))
sh_bin=[] 
for i in range(7):
    sh_bin.append(model.addVar('sh_bin_'+str(i),vtype="BINARY"))
    
ch_inven=[]
for i in range(12):
    ch_inven.append(model.addVar('ch_in_'+str(i),vtype="C")) 
    
sh_inven=[]
for i in range(10):
    sh_inven.append(model.addVar('sh_in_'+str(i),vtype="C")) 
    
demand_sh=[]
for i in range(10):
    demand_sh.append(model.addVar('demand_sh_'+str(i),vtype="C"))

up_ch_in=[]#更新ch库存用的约束
up_ch_in.append(model.addCons(init_ch-demand_ch[0]==ch_inven[0]))
up_ch_in.append(model.addCons(ch_inven[0]+5-demand_ch[1]==ch_inven[1]))
for i in range(2,12):
    up_ch_in.append(model.addCons(ch_inven[i-1]+ch_order[i-2]-demand_ch[i]==ch_inven[i]))
    
up_sh_in=[]#更新sh库存用的约束
up_sh_in.append(model.addCons(init_sh-demand_sh[0]==sh_inven[0]))
up_sh_in.append(model.addCons(sh_inven[0]+22-demand_sh[1]==sh_inven[1]))
up_sh_in.append(model.addCons(sh_inven[1]+0-demand_sh[2]==sh_inven[2]))
for i in range(3,10):
    up_ch_in.append(model.addCons(sh_inven[i-1]+sh_order[i-3]-demand_sh[i]==sh_inven[i]))
    
for i in range(10):#为了计算成本，确认当天是否有订货
    model.addCons(ch_bin[i]<=ch_order[i])
    model.addCons(9999*ch_bin[i]>=ch_order[i])

for i in range(7):#为了计算成本，确认当天是否有订货
    model.addCons(sh_bin[i]<=sh_order[i])
    model.addCons(9999*sh_bin[i]>=sh_order[i]) 

for i in range(10):
    model.addCons(demand_sh[i]==ch_order[i]*2)
    
model.setObjective(sum(ch_inven)*ch_in_unit_cost+sum(sh_inven)*sh_in_unit_cost+\
                   sum(ch_bin)*ch_pre+sum(sh_bin)*sh_pre, "minimize")
model.optimize()
if model.getStatus() == "optimal":
    print("Optimal value:", model.getObjVal())
    print("Solution:")
    for i in range(10):
        print('ch_'+str(i)+'=',model.getVal(ch_order[i]),' ch_bin_'+str(i)+'=',model.getVal(ch_bin[i]))
    for i in range(7):
        print('sh_'+str(i)+'=',model.getVal(sh_order[i]),' sh_bin_'+str(i)+'=',model.getVal(sh_bin[i]))
    print("status:")
    for i in range(10):
        print('demand_sh_'+str(i)+'=',model.getVal(demand_sh[i]))
    for i in range(12):
        print('ch_inven_'+str(i)+'=',model.getVal(ch_inven[i]))
    for i in range(10):
        print('sh_inven_'+str(i)+'=',model.getVal(sh_inven[i]))
else:
    print("Problem could not be solved to optimality")