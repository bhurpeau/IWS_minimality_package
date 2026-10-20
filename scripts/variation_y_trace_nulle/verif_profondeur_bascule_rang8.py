"""Bascule du declencheur du 8e impact (noeud 1 -> rang suivant) : eps_c par bissection sur le flot hybride complet (protocole de verif_profondeur.py), directions (gamma,lambda)_bar = (1,0), (0,1), (1,1), eps dans [0, 1e-2]. Compare a eps_c = nu/|nu_prime| de verif_profondeur_propagation.py."""
import sys, os
sys.path.insert(0,'' + os.path.dirname(os.path.abspath(__file__)) + '')
import numpy as np
import zero_V0_lib as Z, iws_kairos_core as core, finger_perturbation_ball as FB
tau0=FB.tau_ref(); U=np.array([core.Ux,core.Uy])
def trig(g,l,K=10):
    res=Z.run(tau0,g,l,U,K,word_ref=None)
    P=[np.sort(res['sols'][r][1].sol(res['sols'][r][2])[36:42])[::-1] for r in range(K)]
    return [w[0] for w in res['word']], P[7][0]-P[7][1]
for name,(gb,lb) in {'gam':(1,0),'lam':(0,1),'both':(1,1)}.items():
    out=[]
    for eps in (0,1e-4,3e-4,1e-3,3e-3,1e-2):
        w,m=trig(eps*gb,eps*lb); out.append('%g:%s'%(eps,''.join(map(str,w[5:9]))))
    print(name,' '.join(out))
# bissection eps_c (declencheur du 8e impact) pour chaque direction
from scipy.optimize import brentq
for name,(gb,lb) in {'gam':(1,0),'lam':(0,1),'both':(1,1)}.items():
    f=lambda e: trig(e*gb,e*lb)[0][7]-0.5
    w0=trig(0,0)[0][7]
    lo,hi=0.0,0.01
    if trig(hi*gb,hi*lb)[0][7]==w0: print(name,'pas de bascule <1e-2'); continue
    for _ in range(14):
        mid=(lo+hi)/2
        if trig(mid*gb,mid*lb)[0][7]==w0: lo=mid
        else: hi=mid
    print(name,'eps_c(8e declencheur) ~ %.2e'%((lo+hi)/2))
