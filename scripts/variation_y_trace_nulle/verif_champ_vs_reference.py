"""Controle de FIDELITE DU MODELE : les champs de vecteurs codes en arithmetique de boules (certif_episodes.Model et certif_independant.Graph) coincident avec
le champ de reference double precision zero_V0_lib.make_rhs (utilise par toutes les mesures V2.x) en des points aleatoires, pour les graphes kept1 et ses images par les sauts.
Les pressions : dP_j = k1 ||H_j|| + k2 ||V_j|| - k3 P_j sont controlees contre la meme reference."""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import arb, ctx
import iws_kairos_core as core, zero_V0_lib as Z
import certif_episodes as C
import certif_independant as I
rng = np.random.default_rng(7)
U = np.array([core.Ux, core.Uy])
worst = {'V1': 0.0, 'V2': 0.0, 'P': 0.0}
graphs = [core.A1_kept1.copy()]
A = core.A1_kept1.copy()
# quelques graphes issus des sauts de reference
y = Z.initial_state(__import__('verif_profondeur_propagation').tau0)
for r in range(8):
    sol, Td, yT = Z.episode(y, A, 0.0, 0.0, U)
    y, key, A = Z.apply_jump(yT, A); graphs.append(A.copy())
for g in graphs:
    f = Z.make_rhs(core.Atilde(g), 0.0, 0.0, U)
    m1 = C.Model(g); m2 = I.Graph(g)
    for t in range(5):
        y = rng.normal(size=42) * 0.8; y[36:] = rng.uniform(0, 1.2, 6)
        ref = f(0.0, y)
        x = [arb(float(v)) for v in y[:36]]
        o1 = m1.Fsca(x); o2 = m2.field(x, lambda z: z.tanh())
        worst['V1'] = max(worst['V1'], max(abs(float(o1[k].mid()) - ref[k]) for k in range(36)))
        worst['V2'] = max(worst['V2'], max(abs(float(o2[k].mid()) - ref[k]) for k in range(36)))
        H = y[0:12].reshape(6, 2); V = y[12:24].reshape(6, 2); P = y[36:42]
        dP = 0.6 * np.linalg.norm(H, axis=1) + 0.4 * np.linalg.norm(V, axis=1) - 0.5 * P
        worst['P'] = max(worst['P'], np.max(np.abs(dP - ref[36:42])))
print("ecart max champ (H,V,tau) : certif_episodes %.2e ; certif_independant %.2e ; pressions %.2e  (sur %d graphes x 5 points)" % (worst['V1'], worst['V2'], worst['P'], len(graphs)))
assert max(worst.values()) < 1e-12
print("OK : les deux champs en boules coincident avec la reference double precision.")
