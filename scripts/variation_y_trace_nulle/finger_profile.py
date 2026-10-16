"""Profil du doigt : pour un eta donne, norme des traces tau_j au rang 4 et scores c_j(phi4) autour du doigt."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core'))
import numpy as np
os.environ.setdefault('PHI_LO','200'); os.environ.setdefault('PHI_HI','228')
sys.argv=[sys.argv[0], os.environ.get('NPHI','3000')] + sys.argv[1:]
import finger_y_variation as F
from iws_kairos_core import run_to_kairos, cos_sim
def profile(eta, ref):
    groups = F.groups_at_depth3(eta)
    grp = [g for g in groups if g['path']==ref][0]
    Hs,Vs,taus,Ps,done = run_to_kairos(grp['H'],grp['V'],grp['tau'],grp['P'],grp['A'])
    order=np.argsort(grp['idx']); phi=F.phi4_deg[grp['idx']][order]
    t=taus[order]; sc={j:cos_sim(t[:,0,:],t[:,j,:]) for j in (1,4,5)}
    nr={j:np.linalg.norm(t[:,j,:],axis=1) for j in range(6)}
    return phi,sc,nr,done[order]
if __name__=="__main__":
    ref=((0,frozenset({1,2,3})),(0,frozenset({1,4,5})))
    for eta in [float(x) for x in sys.argv[2:]]:
        phi,sc,nr,done=profile(eta,ref)
        g14=sc[1]-sc[4]
        print("eta=%+.3f  done=%d/%d"%(eta,done.sum(),len(done)))
        for q in np.linspace(0,len(phi)-1,13).astype(int):
            print("  phi4=%7.3f  c1=%+.3f c4=%+.3f c5=%+.3f  g14=%+.3f | |tau|: %s"%(phi[q],sc[1][q],sc[4][q],sc[5][q],g14[q]," ".join("%.3f"%nr[j][q] for j in range(6))))
        # extremes of g14
        k=np.argmin(g14); print("  min g14 %+.4f at %.3f ; max g14 %+.4f at %.3f"%(g14[k],phi[k],g14.max(),phi[np.argmax(g14)]))
