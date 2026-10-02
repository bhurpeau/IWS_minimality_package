"""
Premiere tentative de construction du temoin Nerode exploitant le trou
Q=[230,250]x[60,100] (Benoit) : deux noeuds p,q IDENTIQUES pour x et x',
places pour que leur mur (bissectrice) tombe a theta1~240 (centre de A1) ;
deux noeuds r=4 (DIFFERENT entre x et x') et s=5, dans la composante {4,5}
separee de A0, pour que leur eventuelle comparaison a k=2 (si elle existe)
tombe a theta2~80 (centre de A2).

Methode : construction empirique puis verification directe (pas de preuve
de gating a priori) -- on fait tourner la paire sur exactement la meme
grille dense de protocoles U4 utilisee pour cartographier R0^(1,2), on
enregistre (theta1,theta2) ET si la paire diverge a k<=4, et on regarde la
correlation. Si la paire ne diverge JAMAIS sous U4 dense alors que U3 (un
autre noeud force) la separe, c'est le temoin cherche -- que (theta1,theta2)
tombe exactement dans Q ou pas, la correlation donnera deja la lecture
mecanique.
"""
import sys, numpy as np, time
sys.path.insert(0, '/tmp/claude-0/-home-claude/19a067d9-7990-5feb-b2e1-1f9d9ba72bad/scratchpad')
from nerode_separating_families import run_pair_family, summarize
from iws_kairos_core_gen import automorphisms, d

N9 = 9
edges9 = [(0,1),(0,2),(0,3),(4,5)]
A0 = np.zeros((N9,N9))
for i,j in edges9: A0[i,j]=A0[j,i]=1
mag = 0.3

phi1,phi2,phi3,phi6 = 15.0, 100.0, 190.0, 10.0
phi_p, phi_q = 250.0, 230.0   # noeuds 7,8 : IDENTIQUES pour x et x', mur a 240
phi_r_s5 = 355.0              # noeud 5 : identique pour x et x'
phi_r4_x, phi_r4_xp = 5.0, 135.0   # noeud 4 : DIFFERENT entre x et x'

def tau9(phi4):
    tau=np.zeros((N9,d))
    tau[0]=mag*np.array([1.0,0.0])
    tau[1]=mag*np.array([np.cos(np.radians(phi1)),np.sin(np.radians(phi1))])
    tau[2]=mag*np.array([np.cos(np.radians(phi2)),np.sin(np.radians(phi2))])
    tau[3]=mag*np.array([np.cos(np.radians(phi3)),np.sin(np.radians(phi3))])
    tau[4]=mag*np.array([np.cos(np.radians(phi4)),np.sin(np.radians(phi4))])
    tau[5]=mag*np.array([np.cos(np.radians(phi_r_s5)),np.sin(np.radians(phi_r_s5))])
    tau[6]=mag*np.array([np.cos(np.radians(phi6)),np.sin(np.radians(phi6))])
    tau[7]=mag*np.array([np.cos(np.radians(phi_p)),np.sin(np.radians(phi_p))])
    tau[8]=mag*np.array([np.cos(np.radians(phi_q)),np.sin(np.radians(phi_q))])
    return tau

tau_x  = tau9(phi_r4_x)
tau_xp = tau9(phi_r4_xp)

print("Etape 1 : la paire diverge-t-elle sous un protocole de reference (depth<=6) ?")
ref_protocol = [(0, 2.5*np.cos(np.radians(37.0)), 2.5*np.sin(np.radians(37.0)))]
fd, px, pxp = run_pair_family(A0, N9, tau_x, tau_xp, ref_protocol, K=6)
print("  reference : %s (k=%s)" % ("SEPARE" if fd[0] is not None else "non-sep", fd[0]))
print("  path_x  =", px[0])
print("  path_xp =", pxp[0])
