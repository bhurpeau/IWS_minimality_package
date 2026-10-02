"""
Verification numerique exacte du mecanisme invoque pour expliquer les cas
"NON SEPARE" sous U5 (mono-axe, Uy=0) dans la matrice de separation :

  (i)  si u_y=0 sur tous les noeuds forces et H(0)=V(0)=0, alors H_y(t)=V_y(t)=0
       identiquement sur TOUS les noeuds, a toute profondeur (invariant exact
       des ODE du noyau, puisque A~ ne melange jamais les composantes x/y) ;
  (ii) consequence : tanh(A~H)_y = 0 identiquement, donc tau_y obeit a
       tau_y_point = -beta * tau_y  -> decroissance exponentielle PURE,
       independante du graphe, du forcage, et du noeud force ;
  (iii) plus generalement (sans supposer Uy=0) : pour deux etats x,x' PARTAGEANT
       le meme graphe A courant et le meme protocole, H,V,P sont rigoureusement
       identiques (ne lisent jamais tau), donc tanh(A~H)(t) est une fonction du
       temps COMMUNE aux deux etats, et la difference Delta_tau = tau_x - tau_x'
       obeit a Delta_tau_point = -beta*Delta_tau (le terme de forcage s'annule
       dans la difference) -> Delta_tau(t) = Delta_tau(0) * exp(-beta t) EXACT,
       quel que soit le protocole.

On verifie (i)-(ii) deja fait dans la session (confirme a la machine pres :
max|H_y|=max|V_y|=0.0, ratio tau_y(T)/tau_y(0) = exp(-beta T) identique sur
tous les noeuds). Ici on verifie (iii), le fait general (pas de symetrie
miroir requise), sur la paire B (N=6) ET la paire C (N=9), sous un protocole
quelconque (y compris hors de U5, pour montrer que c'est bien general).
"""
import numpy as np
from iws_kairos_core_gen import rhs_batch, rk4_batch, Atilde, d

def check_delta_tau_decay(name, A1, N, tau_x0, tau_xp0, Ux, Uy, node, T=4.0, dt=2e-3):
    G = 2
    H = np.zeros((G,N,d)); V = np.zeros((G,N,d)); P = np.zeros((G,N)); P[:,0] = 0.35*1.25
    tau = np.stack([tau_x0, tau_xp0], axis=0)
    At = Atilde(A1, N)
    def ufun(t):
        u = np.zeros((G,N,d)); u[:,node] = (Ux,Uy); return u
    beta = 0.12
    dtau0 = tau_x0 - tau_xp0
    nsteps = int(T/dt)
    max_err = 0.0
    for step in range(nsteps):
        H,V,tau,P = rk4_batch(H,V,tau,P,At,step*dt,dt,ufun)
        t = (step+1)*dt
        dtau_now = tau[0] - tau[1]
        predicted = dtau0 * np.exp(-beta*t)
        err = np.abs(dtau_now - predicted).max()
        max_err = max(max_err, err)
    print(f"  [{name}] protocole (noeud={node}, Ux={Ux}, Uy={Uy}) : "
          f"erreur max |Delta_tau_numerique - Delta_tau(0)*exp(-beta t)| sur [0,{T}] = {max_err:.3e}")

N6 = 6
edges6 = [(0,1),(0,2),(0,3),(1,4),(2,5),(3,4),(3,5),(4,5)]
A1_6 = np.zeros((N6,N6))
for i,j in edges6: A1_6[i,j]=A1_6[j,i]=1
mag = 0.3
def tau6_B(phi4_deg, phi5_deg):
    tau = np.zeros((N6, d))
    tau[0] = mag*np.array([1.0, 0.0])
    tau[1] = mag*np.array([np.cos(np.radians(10.0)), np.sin(np.radians(10.0))])
    tau[2] = mag*np.array([np.cos(np.radians(40.0)), np.sin(np.radians(40.0))])
    tau[3] = mag*np.array([np.cos(2.0), np.sin(2.0)])
    tau[4] = mag*np.array([np.cos(np.radians(phi4_deg)), np.sin(np.radians(phi4_deg))])
    tau[5] = mag*np.array([np.cos(np.radians(phi5_deg)), np.sin(np.radians(phi5_deg))])
    return tau
tau_B, tau_Bp = tau6_B(-5.0, 0.08474576271186418), tau6_B(-5.0, 0.5932203389830502)

print("Paire B (N=6) -- verification de Delta_tau(t) = Delta_tau(0)*exp(-beta t) :")
check_delta_tau_decay("Pair B, Uy=0", A1_6, N6, tau_B, tau_Bp, Ux=3.0, Uy=0.0, node=0)
check_delta_tau_decay("Pair B, Uy!=0", A1_6, N6, tau_B, tau_Bp, Ux=2.0, Uy=1.2, node=0)
check_delta_tau_decay("Pair B, autre noeud", A1_6, N6, tau_B, tau_Bp, Ux=2.5, Uy=0.0, node=3)

N9 = 9
edges9 = [(0,1),(0,2),(0,3),(4,5)]
A1_9 = np.zeros((N9,N9))
for i,j in edges9: A1_9[i,j]=A1_9[j,i]=1
def tau9(phi2_deg, phi6_deg):
    tau = np.zeros((N9, d))
    tau[0] = mag*np.array([1.0, 0.0])
    tau[1] = mag*np.array([np.cos(np.radians(15.0)), np.sin(np.radians(15.0))])
    tau[2] = mag*np.array([np.cos(np.radians(phi2_deg)), np.sin(np.radians(phi2_deg))])
    tau[3] = mag*np.array([np.cos(np.radians(45.0)), np.sin(np.radians(45.0))])
    tau[4] = mag*np.array([np.cos(np.radians(5.0)), np.sin(np.radians(5.0))])
    tau[5] = mag*np.array([np.cos(np.radians(355.0)), np.sin(np.radians(355.0))])
    tau[6] = mag*np.array([np.cos(np.radians(phi6_deg)), np.sin(np.radians(phi6_deg))])
    tau[7] = mag*np.array([np.cos(np.radians(200.0)), np.sin(np.radians(200.0))])
    tau[8] = mag*np.array([np.cos(np.radians(160.0)), np.sin(np.radians(160.0))])
    return tau
tau_C  = tau9(341.64406779661016, 358.52542372881356)
tau_Cp = tau9(341.64406779661016, 359.03389830508473)

print("\nPaire C (N=9) -- verification de Delta_tau(t) = Delta_tau(0)*exp(-beta t) :")
check_delta_tau_decay("Pair C, Uy=0", A1_9, N9, tau_C, tau_Cp, Ux=2.5, Uy=0.0, node=0)
check_delta_tau_decay("Pair C, Uy!=0", A1_9, N9, tau_C, tau_Cp, Ux=1.5, Uy=2.0, node=4)
