"""Hypothese (T) : min_t ||tau_j|| sur les 8 premiers episodes, trois protocoles (gamma_bar, lambda_bar), eps = 1e-2 et 1e-3 (grille de 4001 points par episode)."""
import sys
sys.path.insert(0,'.')
import numpy as np, verif_profondeur_propagation as VP, zero_V0_lib as Z
tau0=VP.tau0.reshape(-1)
for gb,lb in ((1,0),(1,1),(0,1)):
    for eps in (1e-2,1e-3):
        res=Z.run(tau0,eps*gb,eps*lb,VP.U,8,word_ref=None)
        mins=[]
        for (t0,sol,Td) in res['sols']:
            Y=sol.sol(np.linspace(0,Td,4001))
            mins.append(np.linalg.norm(Y[24:36].reshape(6,2,-1),axis=1).min())
        w=len(res['sols'])
        print("(gb,lb)=(%d,%d) eps=%g : %d episodes, min ||tau_j|| par episode = %s ; global %.4f"%(gb,lb,eps,w,np.array2string(np.array(mins),precision=3),min(mins)))
