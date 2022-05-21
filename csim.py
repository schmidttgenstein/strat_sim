import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 


base_mu= 1.075
base_sig = 0.04
targ_mu = 1.2
targ_sig = 0.075
cap = 10000  ## base capital of $10k 
T_hor = 12
a = .015
N1 = int(1e3)
N2 = int(1e3)
p_arr = []
sig0 = 0.0025
n_att = 10
data = np.zeros([N1,N2,n_att])
#outer loop iterates over target growths
for k in range(N1):
    targ_rate = np.random.normal(targ_mu,targ_sig) ** (1/T_hor)
    targ_arr = np.ones(T_hor) * targ_rate
    #inner loop iterates over actual return (random)
    for kk in range(N2):
        cont = cap
        gain = 0 
        act_rate = np.random.normal(base_mu,base_sig) ** (1/T_hor)
        act_arr = np.random.normal(act_rate,sig0,T_hor)
        r_diff = targ_arr - act_arr 
        for j in range(T_hor):
            growth_agg = targ_arr[:j+1].prod()
            T_diff = r_diff[j]
            change = cap * growth_agg * T_diff
            if change <0:
                gain -= change 
            else:
                cont += change
        tot_cap = gain + cont 
        hold_cap = cap * act_arr.prod() 
        rg_perc = (tot_cap - hold_cap) / cap
        cg_perc = (tot_cap - cont) / cont 
        hg_perc = (hold_cap - cap) / cap
        ag_perc = tot_cap / cap 
        exp_cap = cap * (act_rate ** T_hor)
        entry = np.array([targ_rate,act_rate,targ_rate-act_rate,tot_cap,hold_cap,exp_cap,tot_cap-hold_cap,rg_perc,ag_perc,cg_perc-hg_perc])
        data[k,kk,:] = entry
    print(f"iter {k}, targ rate {targ_rate}, relative growth % {data[k,:,7].mean()}")
plt.plot(data[:,:,2].flatten(),data[:,:,9].flatten(),'.')
plt.xlabel('target rate - actual rate')
plt.ylabel('relative growth percentage')
plt.show()