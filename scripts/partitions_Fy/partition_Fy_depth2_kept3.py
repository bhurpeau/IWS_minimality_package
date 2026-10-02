import numpy as np, itertools, time

# Chambre "garde=3" du temoin N=6 : retires={1,2}, ajoutes={4,5} au Kairos 1.
# Prediction de Benoit : A1 conserve sigma=(1 2)(4 5) (fixant 0,3).
# On choisit tau1=tau2 (partie de Fix(sigma) deja satisfaite), et on scanne
# (phi4,phi5) : la droite phi4=phi5 doit alors etre EXACTEMENT Fix(sigma)
# restreint a cette coupe, et coincider avec une egalite de scores EXACTE
# (tie orbital reel), tandis qu'ailleurs les egalites de scores (s'il y en a)
# doivent etre transverses.

N, d = 6, 2
zeta, alpha, beta = 0.8, 0.45, 0.12
gamma0 = 0.25
k1, k2, k3 = 0.6, 0.4, 0.5
Theta, rP, rV = 1.25, 0.35, 0.5

edges0 = [(0,1),(0,2),(0,3),(1,4),(2,5),(3,4),(3,5),(4,5)]
A0 = np.zeros((N,N))
for i,j in edges0: A0[i,j]=A0[j,i]=1

def Atilde(A):
    B = A + np.eye(N); return B / B.sum(axis=1, keepdims=True)

A1 = A0.copy()
A1[0,1]=A1[1,0]=0
A1[0,2]=A1[2,0]=0
A1[0,4]=A1[4,0]=1
A1[0,5]=A1[5,0]=1
At1 = Atilde(A1)

def automorphisms(A):
    return [p for p in itertools.permutations(range(N)) if np.array_equal(A[np.ix_(p,p)],A)]
auts1 = automorphisms(A1)
print("Aut(A1) [chambre garde=3] :", auts1, " |Aut| =", len(auts1))
sigma = (0,2,1,3,5,4)
print("sigma=(1 2)(4 5) dans Aut(A1) ?", sigma in auts1)

def u_cont_batch(t, G, U=2.5):
    u = np.zeros((G,N,d)); u[:,0]=(U,0.0); return u

def rhs_batch(H,V,tau,P,A_t,u):
    th = np.tanh(np.einsum('ij,gjd->gid', A_t, H))
    dH = V
    dV = -gamma0*V - H + zeta*th + u
    dtau = alpha*th - beta*tau
    dP = k1*np.linalg.norm(H,axis=-1) + k2*np.linalg.norm(V,axis=-1) - k3*P
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
phi3_fixed = np.radians(10.0)   # domine largement -> garde=3 au Kairos1
phi12_fixed = np.radians(140.0)  # tau1=tau2 EXACTEMENT (precondition Fix(sigma))

tau_init = np.zeros((G,N,d))
tau_init[:,0] = mag*np.array([1.0,0.0])
tau_init[:,1] = mag*np.array([np.cos(phi12_fixed), np.sin(phi12_fixed)])
tau_init[:,2] = mag*np.array([np.cos(phi12_fixed), np.sin(phi12_fixed)])   # = tau_1 exactement
tau_init[:,3] = mag*np.array([np.cos(phi3_fixed), np.sin(phi3_fixed)])
tau_init[:,4] = mag*np.stack([np.cos(phi4_flat), np.sin(phi4_flat)], axis=-1)
tau_init[:,5] = mag*np.stack([np.cos(phi5_flat), np.sin(phi5_flat)], axis=-1)

c1=cos_sim(tau_init[:,0],tau_init[:,1]); c2=cos_sim(tau_init[:,0],tau_init[:,2]); c3=cos_sim(tau_init[:,0],tau_init[:,3])
assert np.all((c3>=c1)&(c3>=c2)), "hors de la chambre garde=3 !"
assert np.allclose(tau_init[:,1], tau_init[:,2]), "tau1 != tau2 !"
print("Chambre garde=3 et tau1=tau2 confirmés sur les %d points." % G)

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

i2 = np.argmax(P_snap, axis=1)
print("i2* rencontres :", {int(v): int((i2==v).sum()) for v in np.unique(i2)})
nb0 = [j for j in range(N) if A1[0,j]==1]
print("  nb(0) dans A1 =", nb0)

kept_label = np.full(G, -1, dtype=int)
tie_exact = np.zeros(G, dtype=bool)
for g in range(G):
    if i2[g] != 0 or not done[g]:
        continue
    sims = {j: cos_sim(tau_snap[g,0], tau_snap[g,j]) for j in nb0}
    order = sorted(sims, key=sims.get)
    kept_label[g] = order[-1]
    if abs(sims[4]-sims[5]) < 1e-10:
        tie_exact[g] = True

vals,counts = np.unique(kept_label, return_counts=True)
print("  classification (garde parmi {3,4,5}) :", dict(zip(vals.tolist(),counts.tolist())))
print("  points avec c4=c5 EXACTEMENT (a 1e-10 pres) :", tie_exact.sum(), "/", G)
# ces points devraient etre alignes sur phi4=phi5
if tie_exact.sum() > 0:
    idx = np.where(tie_exact)[0]
    d4 = phi4_flat[idx]; d5 = phi5_flat[idx]
    print("  écart max |phi4-phi5| parmi ces points (deg) :", np.degrees(np.abs(((d4-d5+np.pi)%(2*np.pi))-np.pi)).max())

np.save("/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad/depth2_kept3_grid.npy",
        dict(PHI4=PHI4, PHI5=PHI5, kept_label=kept_label.reshape(n_grid,n_grid),
             tie_exact=tie_exact.reshape(n_grid,n_grid), i2=i2.reshape(n_grid,n_grid)),
        allow_pickle=True)
print("Sauvegardé.")
