import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 


base_mu= 1.1
base_sig = 0.075
targ_mu = 1.2
targ_sig = 0.05
cap = 10000  ## base capital of $10k 
T_hor = 12
a = .015
N1 = int(2e2)
N2 = int(5e1)
N3 = int(1e2)
p_arr = []
sig0 = 0.0045
sigm = 0.001
n_att = 15
data = np.zeros([N1*N2*N3,n_att])
row = 0 
#outer loop iterates over target growths
for k in range(N1):
    targ_rate = np.random.normal(targ_mu,targ_sig) ** (1/T_hor)
    targ_arr = np.ones(T_hor) * targ_rate
    #inner loop iterates over actual return (random)
    for kk in range(N2):
        sigv = np.max([sigm,np.random.normal(sig0,2*sig0)])
        at_rate = np.random.normal(base_mu,base_sig) ** (1/T_hor)
        for kkx in range(N3):
            pipo_contr = cap
            sky_contr  = cap 
            gain = 0 
            act_arr = np.random.normal(at_rate,sigv,T_hor)
            act_rate = act_arr.prod()
            r_diff = targ_arr - act_arr 
            max_rate = np.maximum(act_arr,targ_arr)
            for j in range(T_hor):
                g_fact = targ_rate ** (j+1)#targ_arr[:j+1].prod()
                g_fact_sky = max_rate[:j+1].prod()
                T_diff = r_diff[j]
                pipo_delta = cap * g_fact * T_diff 
                sky_delta = cap * g_fact_sky * T_diff 
                if T_diff <0:
                    gain -= pipo_delta 
                else:
                    pipo_contr += pipo_delta
                    sky_contr += sky_delta
            tot_cap0 = gain + pipo_contr
            pipo_cap = gain + cap * (targ_rate ** T_hor)
            sky_cap = cap * max_rate.prod()
            bnh_cap = cap * act_arr.prod() 
            gper_pipo = (pipo_cap - pipo_contr) / pipo_contr
            gper_bnh = (bnh_cap - cap) / cap
            gper_sky = (sky_cap - sky_contr) / sky_contr
            obcc_sky = sky_contr / cap 
            obcc_pipo = pipo_contr / cap 
            y_pipo = 1 if gper_pipo - gper_bnh > 0 else 0 
            y_sky = 1 if gper_sky - gper_bnh > 0 else 0 
            tma = targ_rate - act_rate 
            entry = np.array([row,targ_rate,act_rate,tma,sigv,gper_pipo,gper_sky,gper_bnh,pipo_cap,sky_cap,bnh_cap,obcc_pipo,obcc_sky,y_pipo,y_sky])
            data[row,:] = entry
            row += 1
    print(f"k is {k}, percent improvement {gper_pipo - gper_bnh},  at {obcc_pipo} over base capital contribution")

columns = ['iter','target_p','actual_p','tma','vola','growthp_pipo','growthp_sky','growthp_bnh','cap_pipo','cap_sky','cap_bnh','obcc_pipo','obcc_sky','y_pipo','y_sky']
df = pd.DataFrame(data =data,columns = columns)
df.to_csv('./../simdata/pipoVbnh/simdata_1.csv',index = False)

plt.figure(1)
plt.plot(data[:,3],data[:,5]-data[:,7],'.')
plt.xlabel('targ - act %')
plt.ylabel('relative growth') 

plt.figure(2)
plt.plot(data[:,3],data[:,11],'.')
plt.xlabel('targ - act %')
plt.ylabel('over base cap contribution') 

plt.show()