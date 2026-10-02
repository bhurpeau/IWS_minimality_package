import sys, numpy as np, pickle
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core_gen import run_to_kairos, jump_batch, d

N = 9
edges = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges: A0[i,j]=A0[j,i]=1

mag = 0.3
phi1_fixed, phi3_fixed = np.radians(15.0), np.radians(45.0)
phi4_fixed, phi5_fixed = np.radians(5.0), np.radians(355.0)
phi7_fixed, phi8_fixed = np.radians(200.0), np.radians(160.0)

# scan large en phi2 (0..360, pas fin), phi6 limite a la bande [0,24] (deja
# identifiee comme necessaire pour que "6" batte "5"), a la recherche d'une
# fenetre {2,4,6} eloignee du premier centre (348,12).
phi2_scan = np.linspace(0, 360, 360, endpoint=False)
phi6_scan = np.linspace(0, 24, 25)
PHI2, PHI6 = np.meshgrid(phi2_scan, phi6_scan, indexing='ij')
G0 = PHI2.size
phi2_flat = np.radians(PHI2).ravel(); phi6_flat = np.radians(PHI6).ravel()

tau_init = np.zeros((G0,N,d))
tau_init[:,0] = mag*np.array([1.0,0.0])
tau_init[:,1] = mag*np.array([np.cos(phi1_fixed), np.sin(phi1_fixed)])
tau_init[:,2] = mag*np.stack([np.cos(phi2_flat), np.sin(phi2_flat)], axis=-1)
tau_init[:,3] = mag*np.array([np.cos(phi3_fixed), np.sin(phi3_fixed)])
tau_init[:,4] = mag*np.array([np.cos(phi4_fixed), np.sin(phi4_fixed)])
tau_init[:,5] = mag*np.array([np.cos(phi5_fixed), np.sin(phi5_fixed)])
tau_init[:,6] = mag*np.stack([np.cos(phi6_flat), np.sin(phi6_flat)], axis=-1)
tau_init[:,7] = mag*np.array([np.cos(phi7_fixed), np.sin(phi7_fixed)])
tau_init[:,8] = mag*np.array([np.cos(phi8_fixed), np.sin(phi8_fixed)])

H0=np.zeros((G0,N,d)); V0=np.zeros((G0,N,d)); P0=np.zeros((G0,N)); P0[:,0]=0.35*1.25
Hs,Vs,taus,Ps,done = run_to_kairos(H0,V0,tau_init,P0,A0,N)
H2,V2,tau2,P2,labels,i2 = jump_batch(Hs[done],Vs[done],taus[done],Ps[done],A0,N)
b246 = frozenset([2,4,6])
match = np.array([lab==b246 and i2v==0 for lab,i2v in zip(labels,i2)])
idx_done = np.flatnonzero(done)
match_global = idx_done[match]
p2m = phi2_flat[match_global]*180/np.pi; p6m = phi6_flat[match_global]*180/np.pi
print("Nb de points {2,4,6} trouves sur le scan (phi2 fin, phi6 in [0,24]) :", match.sum())
# regrouper en clusters separes par continuite en phi2 (distance circulaire)
order = np.argsort(p2m)
p2s = p2m[order]
gaps = np.diff(p2s)
breaks = np.flatnonzero(gaps > 3.0)
clusters = np.split(p2s, breaks+1)
print("Clusters en phi2 (deg) :")
for c in clusters:
    print("  [%.1f, %.1f]  (n=%d)" % (c.min(), c.max(), len(c)))
