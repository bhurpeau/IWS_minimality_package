import pathlib as _pathlib
def _lp(name): return str(_pathlib.Path(__file__).resolve().parent / name)
import sys, numpy as np, pickle, time
import pathlib as _pathlib
_SCRIPTS = _pathlib.Path(__file__).resolve().parents[1]
for _sub in ('core', 'utils', 'axiomes_crash_tests', 'partitions_Fy', 'genealogie_n9', 'minimalite_U5_U4_U3', 'R0_reachability', 'construction_temoin_Q'):
    sys.path.insert(0, str(_SCRIPTS / _sub))
from iws_kairos_core_gen import (automorphisms, run_to_kairos, jump_batch,
                                  build_A_from_label, d)

# Benoit : deuxieme point de zoom dans {2,4,6}, choisi sans rechercher une
# zone riche, pour savoir si (2 6) est une propriete locale robuste de la
# chambre ou seulement de l'entourage du premier point. Le scan complet
# (n9_find_second_center.py) montre que la region {2,4,6} au niveau k=1
# est un seul arc continu phi2 in [328,375]=[-32,15] (mod 360) x phi6 in
# [0,24] environ -- le premier centre (348,12) est pres du milieu. On choisit
# un second centre nettement deplace vers un bord de cet arc, sans optimiser
# pour la richesse : phi2=334, phi6=18.

N = 9
edges = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges: A0[i,j]=A0[j,i]=1
SIGMA_26 = tuple(6 if v==2 else (2 if v==6 else v) for v in range(N))

c2, c6 = 334.0, 18.0
print("Second centre choisi (sans recherche de richesse) : (phi2,phi6) = (%.1f,%.1f)" % (c2,c6))
print("  [rappel premier centre : (348.0, 12.0), distance ~%.1f deg en phi2]" % (348.0-334.0))

mag = 0.3
phi1_fixed, phi3_fixed = np.radians(15.0), np.radians(45.0)
phi4_fixed, phi5_fixed = np.radians(5.0), np.radians(355.0)
phi7_fixed, phi8_fixed = np.radians(200.0), np.radians(160.0)

def build_tau(phi2_flat, phi6_flat, G0):
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
    return tau_init

N_TARGET = 3600
b246 = frozenset([2,4,6])
radius, n_side = 15.0, 90
while True:
    phi2_range = (c2 + np.linspace(-radius, radius, n_side)) % 360
    phi6_range = (c6 + np.linspace(-radius, radius, n_side)) % 360
    PHI2,PHI6 = np.meshgrid(phi2_range,phi6_range,indexing='ij')
    G0 = n_side*n_side
    phi2_flat = np.radians(PHI2).ravel(); phi6_flat = np.radians(PHI6).ravel()
    tau_init = build_tau(phi2_flat, phi6_flat, G0)
    H0=np.zeros((G0,N,d)); V0=np.zeros((G0,N,d)); P0=np.zeros((G0,N)); P0[:,0]=0.35*1.25
    Hs,Vs,taus,Ps,done = run_to_kairos(H0,V0,tau_init,P0,A0,N)
    H2,V2,tau2,P2,labels,i2 = jump_batch(Hs[done],Vs[done],taus[done],Ps[done],A0,N)
    match = np.array([lab==b246 and i2v==0 for lab,i2v in zip(labels,i2)])
    print("  rayon=%.1f, grille=%dx%d : %d/%d points matchent {2,4,6}" % (radius,n_side,n_side,match.sum(),G0))
    if match.sum() >= N_TARGET: break
    radius *= 1.4; n_side = int(n_side*1.3)
sel = np.flatnonzero(match)[:N_TARGET]
print("Echantillon conditionne : %d points" % N_TARGET)

groups = [dict(idx=np.arange(N_TARGET), A=build_A_from_label(A0,0,b246,N),
               H=H2[sel], V=V2[sel], tau=tau2[sel], P=P2[sel], path=((0,b246),))]

def advance_instrumented(groups, depth, N):
    new_groups = []
    log = []
    for grp in groups:
        Hs,Vs,taus,Ps,done = run_to_kairos(grp['H'],grp['V'],grp['tau'],grp['P'],grp['A'],N)
        if not done.any(): continue
        H2,V2,tau2,P2, labels, i2 = jump_batch(Hs[done],Vs[done],taus[done],Ps[done],grp['A'],N)
        idx_done = grp['idx'][done]
        uniq = {}
        for k_local, lab in enumerate(labels):
            uniq.setdefault((lab, int(i2[k_local])), []).append(k_local)
        children = []
        for (lab, istar), pos_list in uniq.items():
            pos = np.array(pos_list)
            A_next = build_A_from_label(grp['A'], istar, lab, N)
            child = dict(idx=idx_done[pos], A=A_next, H=H2[pos], V=V2[pos], tau=tau2[pos], P=P2[pos],
                         path=grp['path']+((istar,lab),))
            children.append(child)
            new_groups.append(child)
        auts_parent = automorphisms(grp['A'], N)
        has_26_parent = SIGMA_26 in auts_parent
        if len(children) > 1:
            istar_common = children[0]['path'][-1][0]
            fixing = [p for p in auts_parent if p[istar_common]==istar_common]
            for a_i in range(len(children)):
                for b_i in range(a_i+1, len(children)):
                    Sa = set(children[a_i]['path'][-1][1])
                    Sb = set(children[b_i]['path'][-1][1])
                    witnesses = [p for p in fixing if set(p[j] for j in Sa)==Sb]
                    structural = len(witnesses) > 0
                    has_26_witness = SIGMA_26 in witnesses
                    log.append(dict(depth=depth, parent_path=grp['path'], parent_size=len(grp['idx']),
                                     istar=istar_common, child_a=Sa, child_b=Sb,
                                     structural=structural, n_witnesses=len(witnesses),
                                     has_26_witness=has_26_witness, has_26_in_parent_aut=has_26_parent))
        else:
            log.append(dict(depth=depth, parent_path=grp['path'], parent_size=len(grp['idx']),
                             structural=False, has_26_in_parent_aut=has_26_parent, no_split=True))
    return new_groups, log

all_log = []
t0 = time.time()
for depth in range(2, 7):
    groups, log = advance_instrumented(groups, depth, N)
    all_log.extend(log)
    n_groups = len({g['path'] for g in groups})
    print("depth=%d : %d groupes (temps cumule %.1fs)" % (depth, n_groups, time.time()-t0))

print("\n=== Scissions STRUCTURELLES, second centre ===")
any_structural = False
for e in all_log:
    if e.get('structural'):
        any_structural = True
        tag_26 = "AVEC (2 6)" if e['has_26_witness'] else "SANS (2 6) -- AUTRE SYMETRIE"
        print(f" k={e['depth']}  chemin parent={e['parent_path']}  "
              f"{sorted(e['child_a'])} <-> {sorted(e['child_b'])}  "
              f"(n_temoins={e['n_witnesses']}, parent_size={e['parent_size']})  {tag_26}")
if not any_structural:
    print(" (aucune scission structurelle trouvee jusqu'a k=6 a ce second centre)")

print("\n=== (2 6) dans Aut(A_parent), par profondeur (second centre) ===")
for depth in range(2,7):
    entries = [e for e in all_log if e['depth']==depth]
    n_with_26 = sum(1 for e in entries if e['has_26_in_parent_aut'])
    print(" k=%d : %d/%d groupes-parents ont (2 6) dans Aut(A)" % (depth, n_with_26, len(entries)))

with open(_lp('n9_246_deep_26_center2.pkl'),'wb') as f:
    pickle.dump(dict(all_log=all_log, center=(c2,c6)), f)
print("\nTemps total : %.1fs" % (time.time()-t0))
