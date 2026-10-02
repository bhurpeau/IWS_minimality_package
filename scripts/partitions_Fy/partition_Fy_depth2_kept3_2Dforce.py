import pathlib as _pathlib
import numpy as np, itertools, time

# Meme experience que partition_Fy_depth2_kept3.py, mais avec un forcage 2D
# generique sur le noeud 0 : u0=(Ux,Uy), Uy != 0, rapport non particulier.
# sigma=(1 2)(4 5) fixe le noeud 0, donc pousser 0 dans une direction
# quelconque ne casse pas sigma. On verifie : la diagonale Fix(sigma) doit
# rester un tie exact ; l'antidiagonale (artefact du forcage 1D precedent)
# doit disparaitre ou se deformer.

N, d = 6, 2
zeta, alpha, beta = 0.8, 0.45, 0.12
gamma0 = 0.25
k1c, k2c, k3c = 0.6, 0.4, 0.5
Theta, rP, rV = 1.25, 0.35, 0.5

edges0 = [(0,1),(0,2),(0,3),(1,4),(2,5),(3,4),(3,5),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges0: A0[i,j]=A0[j,i]=1
A1 = A0.copy()
A1[0,1]=A1[1,0]=0; A1[0,2]=A1[2,0]=0; A1[0,4]=A1[4,0]=1; A1[0,5]=A1[5,0]=1
At1 = (A1+np.eye(N)); At1 = At1/At1.sum(axis=1,keepdims=True)

def automorphisms(A):
    return [p for p in itertools.permutations(range(N)) if np.array_equal(A[np.ix_(p,p)],A)]
auts1 = automorphisms(A1)
sigma = (0,2,1,3,5,4)
print("sigma dans Aut(A1) ?", sigma in auts1, " |Aut(A1)| =", len(auts1))

# forcage 2D generique, rapport non particulier (U=2.5, angle 37 deg, ni 0 ni 45 ni 90...)
Uang = np.radians(37.0)
Uamp = 2.5
Ux, Uy = Uamp*np.cos(Uang), Uamp*np.sin(Uang)
print("u0 = (%.4f, %.4f)  (Uy != 0 : %s)" % (Ux, Uy, Uy != 0))

def u_cont_batch(t, G):
    u = np.zeros((G,N,d)); u[:,0]=(Ux,Uy); return u

def rhs_batch(H,V,tau,P,A_t,u):
    th = np.tanh(np.einsum('ij,gjd->gid', A_t, H))
    dH = V
    dV = -gamma0*V - H + zeta*th + u
    dtau = alpha*th - beta*tau
    dP = k1c*np.linalg.norm(H,axis=-1) + k2c*np.linalg.norm(V,axis=-1) - k3c*P
    return dH,dV,dtau,dP

def rk4_batch(H,V,tau,P,A_t,t,dt,G):
    a1 = rhs_batch(H,V,tau,P,A_t,u_cont_batch(t,G))
    a2 = rhs_batch(H+dt/2*a1[0],V+dt/2*a1[1],tau+dt/2*a1[2],P+dt/2*a1[3],A_t,u_cont_batch(t+dt/2,G))
    a3 = rhs_batch(H+dt/2*a2[0],V+dt/2*a2[1],tau+dt/2*a2[2],P+dt/2*a2[3],A_t,u_cont_batch(t+dt/2,G))
    a4 = rhs_batch(H+dt*a3[0],V+dt*a3[1],tau+dt*a3[2],P+dt*a3[3],A_t,u_cont_batch(t+dt,G))
    H2=H+dt/6*(a1[0]+2*a2[0]+2*a3[0]+a4[0]); V2=V+dt/6*(a1[1]+2*a2[1]+2*a3[1]+a4[1])
    tau2=tau+dt/6*(a1[2]+2*a2[2]+2*a3[2]+a4[2]); P2=P+dt/6*(a1[3]+2*a2[3]+2*a3[3]+a4[3])
    return H2,V2,tau2,P2

def cos_sim(a,b):
    return (a*b).sum(axis=-1)/(np.linalg.norm(a,axis=-1)*np.linalg.norm(b,axis=-1))

n_grid = 60
phi4_range = np.linspace(0.0,360.0,n_grid,endpoint=False)
phi5_range = np.linspace(0.0,360.0,n_grid,endpoint=False)
PHI4,PHI5 = np.meshgrid(phi4_range,phi5_range,indexing='ij')
G = n_grid*n_grid
phi4_flat = np.radians(PHI4).ravel(); phi5_flat = np.radians(PHI5).ravel()

mag = 0.3
phi3_fixed = np.radians(10.0)
phi12_fixed = np.radians(140.0)

tau_init = np.zeros((G,N,d))
tau_init[:,0] = mag*np.array([1.0,0.0])
tau_init[:,1] = mag*np.array([np.cos(phi12_fixed), np.sin(phi12_fixed)])
tau_init[:,2] = tau_init[:,1].copy()
tau_init[:,3] = mag*np.array([np.cos(phi3_fixed), np.sin(phi3_fixed)])
tau_init[:,4] = mag*np.stack([np.cos(phi4_flat), np.sin(phi4_flat)], axis=-1)
tau_init[:,5] = mag*np.stack([np.cos(phi5_flat), np.sin(phi5_flat)], axis=-1)

c1=cos_sim(tau_init[:,0],tau_init[:,1]); c2=cos_sim(tau_init[:,0],tau_init[:,2]); c3=cos_sim(tau_init[:,0],tau_init[:,3])
assert np.all((c3>=c1)&(c3>=c2)), "hors de la chambre garde=3 !"

H=np.zeros((G,N,d)); V=np.zeros((G,N,d)); tau=tau_init.copy()
P=np.zeros((G,N)); P[:,0]=Theta
P[:,0]=rP*P[:,0]; V[:,0]=rV*V[:,0]

dt=2e-3; Tmax=20.0; nsteps=int(Tmax/dt)
done=np.zeros(G,dtype=bool)
H_snap=H.copy(); V_snap=V.copy(); tau_snap=tau.copy(); P_snap=P.copy()

t0=time.time(); t=0.0
for step in range(nsteps):
    H,V,tau,P = rk4_batch(H,V,tau,P,At1,t,dt,G)
    t += dt
    newly = (~done) & (P.max(axis=1)>=Theta)
    if newly.any():
        H_snap[newly]=H[newly]; V_snap[newly]=V[newly]; tau_snap[newly]=tau[newly]; P_snap[newly]=P[newly]
        done[newly]=True
    if done.all(): break
print("Temps : %.1fs, %d pas, %d/%d termines" % (time.time()-t0, step+1, done.sum(), G))

# verification directe : H_y, V_y restent-ils nuls ?
print("max|H_y| a la fin (echantillon) :", np.abs(H[:, :, 1]).max())
print("max|V_y| a la fin (echantillon) :", np.abs(V[:, :, 1]).max())

i2 = np.argmax(P_snap, axis=1)
print("i2* rencontres :", {int(v): int((i2==v).sum()) for v in np.unique(i2)})
nb0 = [j for j in range(N) if A1[0,j]==1]

kept_label = np.full(G, -1, dtype=int)
c4_arr = np.full(G, np.nan); c5_arr = np.full(G, np.nan)
for g in range(G):
    if i2[g] != 0 or not done[g]:
        continue
    sims = {j: cos_sim(tau_snap[g,0], tau_snap[g,j]) for j in nb0}
    order = sorted(sims, key=sims.get)
    kept_label[g] = order[-1]
    c4_arr[g] = sims[4]; c5_arr[g] = sims[5]

vals,counts = np.unique(kept_label, return_counts=True)
print("  classification (garde parmi {3,4,5}) :", dict(zip(vals.tolist(),counts.tolist())))

diff = np.abs(c4_arr - c5_arr)
tie_exact = diff < 1e-9
print("  points avec c4=c5 (<1e-9) :", np.nansum(tie_exact), "/", G)
if tie_exact.sum()>0:
    idxs = np.where(tie_exact)[0]
    d4 = phi4_flat[idxs]; d5 = phi5_flat[idxs]
    ddiag = np.degrees(np.abs(((d4-d5+np.pi)%(2*np.pi))-np.pi))
    dsum  = np.degrees(np.abs(((d4+d5+np.pi)%(2*np.pi))-np.pi))
    print("   -> sur diagonale (phi4=phi5) :", (ddiag<1.0).sum())
    print("   -> sur antidiagonale (phi4=-phi5) :", (dsum<1.0).sum())
    print("   -> ni l'un ni l'autre :", ((ddiag>=1.0)&(dsum>=1.0)).sum())

np.save(str(_pathlib.Path(__file__).resolve().parent / 'depth2_kept3_2D_grid.npy'),
        dict(PHI4=PHI4, PHI5=PHI5, kept_label=kept_label.reshape(n_grid,n_grid)),
        allow_pickle=True)
print("Sauvegardé.")
