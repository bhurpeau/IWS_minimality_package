"""
Cartographie de R_0 (Benoit) : l'ensemble des directions atteignables de
tau_0 au moment du premier Kairos, sous U4 (forcage 2D constant, noeud 0
uniquement), sur le temoin N=9 (chambre {2,4,6}).

Avant le premier Kairos, A0 est deconnecte en {0,1,2,3}/{4,5}/{6,7,8} ; le
premier saut ajoute toujours 2 noeuds de {4,...,8} a 0 (ils sont tous dans
nn(0)), donc c'est la SEULE fenetre ou la reduction geometrique de Benoit
s'applique tel quel (apres le saut, les composantes commencent a se
melanger). On balaie donc (amplitude, angle) du forcage au noeud 0, et on
enregistre l'angle de tau_0 au moment exact ou P[0] atteint Theta.

Question posee : R_0 (l'ensemble de ces angles, sur toute la grille) couvre-
t-il tout le cercle S^1, ou laisse-t-il un arc interdit ? Et cet arc (s'il
existe) persiste-t-il quand on densifie / elargit l'amplitude ?
"""
import sys, numpy as np, time
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from iws_kairos_core_gen import Atilde, rhs_batch, rk4_batch, d, Theta, rP

N9 = 9
edges9 = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N9,N9))
for i,j in edges9: A0[i,j]=A0[j,i]=1
At0 = Atilde(A0, N9)

mag = 0.3
phi1,phi2,phi3,phi4,phi5,phi6,phi7,phi8 = 15.0,348.0,45.0,5.0,355.0,12.0,200.0,160.0

def tau9_base():
    tau=np.zeros((N9,d))
    tau[0]=mag*np.array([1.0,0.0])
    for k,phi in zip(range(1,9),[phi1,phi2,phi3,phi4,phi5,phi6,phi7,phi8]):
        tau[k]=mag*np.array([np.cos(np.radians(phi)),np.sin(np.radians(phi))])
    return tau

tau0_base = tau9_base()

def tau0_angle_at_first_kairos_batch(amps, angs, dt=2e-3, Tmax=15.0):
    """Pour chaque (amp,ang) de la grille (meme taille, appaires), simule en
    batch jusqu'au premier Kairos et renvoie l'angle de tau_0 a cet instant
    (NaN si pas atteint dans Tmax)."""
    G = len(amps)
    H = np.zeros((G,N9,d)); V = np.zeros((G,N9,d)); P = np.zeros((G,N9)); P[:,0]=rP*Theta
    tau = np.repeat(tau0_base[None,:,:], G, axis=0)
    Ux = amps*np.cos(np.radians(angs)); Uy = amps*np.sin(np.radians(angs))
    def ufun(t):
        u = np.zeros((G,N9,d)); u[:,0,0]=Ux; u[:,0,1]=Uy; return u
    done = np.zeros(G, dtype=bool)
    tau0_snap = np.full((G,d), np.nan)
    nsteps = int(Tmax/dt)
    for step in range(nsteps):
        H,V,tau,P = rk4_batch(H,V,tau,P,At0,step*dt,dt,ufun)
        newly = (~done) & (P.max(axis=1) >= Theta)
        if newly.any():
            tau0_snap[newly] = tau[newly,0,:]
            done[newly] = True
        if done.all():
            break
    angles = np.degrees(np.arctan2(tau0_snap[:,1], tau0_snap[:,0])) % 360
    angles[~done] = np.nan
    return angles, done

# --------------------------------------------------------------- balayage 1
# grille large : 25 amplitudes (0.5 a 12) x 90 angles (pas de 4 deg) = 2250 pts
amps_grid = np.repeat(np.linspace(0.5, 12.0, 25), 90)
angs_grid = np.tile(np.linspace(0, 356, 90), 25)
print("Balayage 1 : %d protocoles (60 amplitudes x 180 angles)" % len(amps_grid))
t0=time.time()
reached_angles, done = tau0_angle_at_first_kairos_batch(amps_grid, angs_grid)
print("  (%.1fs), %d/%d ont atteint un premier Kairos" % (time.time()-t0, done.sum(), len(done)))

valid = reached_angles[done]
bins = np.zeros(360, dtype=int)
for a in valid:
    bins[int(a) % 360] += 1
empty_bins = np.where(bins == 0)[0]
print("Bins de 1 deg jamais atteints (sur 360) : %d" % len(empty_bins))
if len(empty_bins) > 0 and len(empty_bins) < 360:
    # regrouper en arcs contigus pour lisibilite
    arcs = []
    start = empty_bins[0]; prev = empty_bins[0]
    for b in empty_bins[1:]:
        if b != prev+1:
            arcs.append((start,prev)); start=b
        prev=b
    arcs.append((start,prev))
    print("  Arcs vides : %s" % arcs)
print("  couverture : min angle=%.1f max angle=%.1f (sur les valides)" % (valid.min(), valid.max()) if len(valid) else "aucun")
