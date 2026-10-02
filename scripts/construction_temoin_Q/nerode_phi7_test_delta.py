import sys, numpy as np, time
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from nerode_separating_families import run_pair_family
from iws_kairos_core_gen import d

N9 = 9
edges9 = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N9,N9))
for i,j in edges9: A0[i,j]=A0[j,i]=1

mag = 0.3
phi1_fixed, phi3_fixed = np.radians(15.0), np.radians(45.0)
phi4_fixed, phi5_fixed = np.radians(5.0), np.radians(355.0)
phi8_fixed = np.radians(160.0)
phi2_c, phi6_c = 348.0, 12.0

def tau9_pert7(phi7_deg):
    tau = np.zeros((N9, d))
    tau[0] = mag*np.array([1.0, 0.0])
    tau[1] = mag*np.array([np.cos(phi1_fixed), np.sin(phi1_fixed)])
    tau[2] = mag*np.array([np.cos(np.radians(phi2_c)), np.sin(np.radians(phi2_c))])
    tau[3] = mag*np.array([np.cos(phi3_fixed), np.sin(phi3_fixed)])
    tau[4] = mag*np.array([np.cos(phi4_fixed), np.sin(phi4_fixed)])
    tau[5] = mag*np.array([np.cos(phi5_fixed), np.sin(phi5_fixed)])
    tau[6] = mag*np.array([np.cos(np.radians(phi6_c)), np.sin(np.radians(phi6_c))])
    tau[7] = mag*np.array([np.cos(np.radians(phi7_deg)), np.sin(np.radians(phi7_deg))])
    tau[8] = mag*np.array([np.cos(phi8_fixed), np.sin(phi8_fixed)])
    return tau

amps_grid = np.load('phi7_amps.npy'); angs_grid = np.load('phi7_angs.npy')
theta1 = np.load('phi7_theta1.npy'); theta2 = np.load('phi7_theta2.npy'); alive_seq = np.load('phi7_alive.npy')
protocols = [(0, a*np.cos(np.radians(g)), a*np.sin(np.radians(g))) for a,g in zip(amps_grid,angs_grid)]

delta = float(sys.argv[1])
K = int(sys.argv[2]) if len(sys.argv)>2 else 4
tau_x  = tau9_pert7(200.0)
tau_xp = tau9_pert7(200.0+delta)
t0=time.time()
fd, px, pxp = run_pair_family(A0, N9, tau_x, tau_xp, protocols, K=K)
print("delta=%.1f K=%d : (%.1fs)" % (delta, K, time.time()-t0))
ks = np.array([k if k is not None else -1 for k in fd])
n_sep = (ks>0).sum()
print("  %d/%d separent ; k=1:%d k=2:%d k=3:%d k>=4:%d" %
      (n_sep, len(ks), (ks==1).sum(), (ks==2).sum(), (ks==3).sum(), (ks>=4).sum()))

sep_mask = ks>0
valid = alive_seq & ~np.isnan(theta1) & ~np.isnan(theta2)
v_sep = valid & sep_mask
v_non = valid & ~sep_mask
print("  parmi les %d protocoles valides (theta1,theta2 definis): %d separent, %d non" % (valid.sum(), v_sep.sum(), v_non.sum()))
if v_sep.sum()>0:
    print("  theta1[separent] : min=%.1f max=%.1f median=%.1f" % (theta1[v_sep].min(), theta1[v_sep].max(), np.median(theta1[v_sep])))
    print("  theta2[separent] : min=%.1f max=%.1f median=%.1f" % (theta2[v_sep].min(), theta2[v_sep].max(), np.median(theta2[v_sep])))
if v_non.sum()>0:
    print("  theta1[non-sep]  : min=%.1f max=%.1f median=%.1f" % (theta1[v_non].min(), theta1[v_non].max(), np.median(theta1[v_non])))
    print("  theta2[non-sep]  : min=%.1f max=%.1f median=%.1f" % (theta2[v_non].min(), theta2[v_non].max(), np.median(theta2[v_non])))

np.save('phi7_delta%d_ks.npy' % int(delta), ks)
