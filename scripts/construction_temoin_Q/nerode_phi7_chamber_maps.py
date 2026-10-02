"""
Benoit : cartes R_{0,A}^(1,2) conditionnees par chambre A1, separant/non
separant, pour A1={1,4,5}, A1={2,4,5} (les deux chambres separantes) et
A1={2,4,6} (temoin negatif, 0/327 separe) -- cote a cote pour comparaison.

Les fuites a k=1 sont isolees (marqueur distinct, exclues de la lecture
principale "sequentielle"). k_min=2 est la categorie cible ; k_min>=3 est
distinguee separement (Benoit : "ou eventuellement >2, distingue separement").

Source : phi7_delta60_chambers.pkl (fd, chamber1_x) + phi7_theta1/2.npy,
phi7_alive.npy (meme grille 800 points, memes indices).
"""
import sys, pickle, pathlib, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = pathlib.Path(__file__).resolve().parent
def _lp(name): return str(_HERE / name)
_FIGDIR = _HERE / "figures"
_FIGDIR.mkdir(exist_ok=True)

theta1 = np.load(_lp('phi7_theta1.npy')); theta2 = np.load(_lp('phi7_theta2.npy'))
alive = np.load(_lp('phi7_alive.npy'))
d = pickle.load(open(_lp('phi7_delta60_chambers.pkl'),'rb'))
fd = d['fd']; chamber1_x = d['chamber1_x']

ks = np.array([k if k is not None else -1 for k in fd])
chambers_key = np.empty(len(chamber1_x), dtype=object)
for _i, _c in enumerate(chamber1_x):
    chambers_key[_i] = tuple(sorted(_c)) if _c else None
valid = alive & ~np.isnan(theta1) & ~np.isnan(theta2)

PANELS = [((1,4,5), "A_1=\\{1,4,5\\}  (separante)"),
          ((2,4,5), "A_1=\\{2,4,5\\}  (separante)"),
          ((2,4,6), "A_1=\\{2,4,6\\}  (temoin negatif, 0/327)")]

# categories (couleur = identite, forme = encodage secondaire, teste colorblind-safe)
CAT = {
    "non-sep":  dict(color="#b5b5b2", marker="o", s=26, alpha=0.75, edgecolor="none",
                      label="non separe (k$\\leq$4)", z=1),
    "leak_k1":  dict(color="#E69F00", marker="x", s=46, alpha=0.95, edgecolor="#E69F00",
                      label="separe k=1 (fuite, hors lecture principale)", z=2),
    "k2":       dict(color="#D55E00", marker="^", s=40, alpha=0.95, edgecolor="black",
                      label="separe k=2 (cible sequentielle)", z=3),
    "k3p":      dict(color="#0072B2", marker="s", s=34, alpha=0.95, edgecolor="black",
                      label="separe k$\\geq$3", z=3),
}

fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.6), dpi=150)

def chamber_mask(chamber):
    return np.array([c == chamber for c in chambers_key])

def circ_center(deg):
    ang = np.radians(deg)
    m = np.degrees(np.arctan2(np.mean(np.sin(ang)), np.mean(np.cos(ang)))) % 360
    return m

def unwrap_around(deg, center):
    return ((deg - center + 180) % 360) - 180 + center

for ax, (chamber, title) in zip(axes, PANELS):
    m_ch = valid & chamber_mask(chamber)
    n_tot = m_ch.sum()
    # recentrage circulaire par panneau (independant sur chaque axe) pour ne
    # pas scinder artificiellement un amas a cheval sur 0/360
    c1 = circ_center(theta1[m_ch]); c2 = circ_center(theta2[m_ch])
    theta1_p = unwrap_around(theta1, c1); theta2_p = unwrap_around(theta2, c2)
    m_non = m_ch & (ks == -1)
    m_k1  = m_ch & (ks == 1)
    m_k2  = m_ch & (ks == 2)
    m_k3p = m_ch & (ks >= 3)

    for key, mask in [("non-sep", m_non), ("leak_k1", m_k1), ("k2", m_k2), ("k3p", m_k3p)]:
        c = CAT[key]
        if mask.sum() == 0:
            continue
        ax.scatter(theta1_p[mask], theta2_p[mask], c=c["color"], marker=c["marker"],
                   s=c["s"], alpha=c["alpha"], edgecolors=c["edgecolor"],
                   linewidths=0.8, zorder=c["z"])

    pad = 8
    ax.set_xlim(theta1_p[m_ch].min()-pad, theta1_p[m_ch].max()+pad)
    ax.set_ylim(theta2_p[m_ch].min()-pad, theta2_p[m_ch].max()+pad)
    ax.set_title("$%s$\n(n=%d points, k2:%d k$\\geq$3:%d k1:%d non-sep:%d)\n[recentre : $\\theta_1$ mod autour de %.0f°, $\\theta_2$ autour de %.0f°]" %
                 (title, n_tot, m_k2.sum(), m_k3p.sum(), m_k1.sum(), m_non.sum(), c1, c2),
                 fontsize=9.5)
    ax.set_xlabel(r"$\theta_1$ (deg, recentre)")
    ax.grid(True, color="#e8e8e5", linewidth=0.6, zorder=0)
    for spine in ax.spines.values():
        spine.set_color("#cfcfcb")

axes[0].set_ylabel(r"$\theta_2$ (deg, recentre)")

handles = [plt.Line2D([0],[0], marker=CAT[k]["marker"], color="none",
                       markerfacecolor=CAT[k]["color"], markeredgecolor=CAT[k]["edgecolor"] if CAT[k]["edgecolor"]!="none" else CAT[k]["color"],
                       markersize=8, label=CAT[k]["label"])
           for k in ["non-sep","k2","k3p","leak_k1"]]
fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=9.5,
           bbox_to_anchor=(0.5, -0.04))

fig.suptitle(r"$\mathcal{R}_{0,A_1}^{(1,2)}$ conditionne par la chambre $A_1$ (temoin $\varphi_7$, $\delta=60°$, N=9, grille 800 protocoles $\mathcal{U}_4$)",
             fontsize=11.5, y=1.02)
fig.tight_layout(rect=[0,0.05,1,0.98])
fig.savefig(str(_FIGDIR / 'R0_A1_chamber_conditioned.png'), bbox_inches="tight", dpi=150)
print("Figure sauvegardee ->", _FIGDIR / 'R0_A1_chamber_conditioned.png')

# resume numerique pour le compte-rendu
for chamber, title in PANELS:
    m_ch = valid & chamber_mask(chamber)
    m_non = m_ch & (ks == -1); m_k1 = m_ch & (ks==1); m_k2 = m_ch & (ks==2); m_k3p = m_ch & (ks>=3)
    print("A1=%s : n=%d | non-sep=%d k1=%d k2=%d k>=3=%d" %
          (chamber, m_ch.sum(), m_non.sum(), m_k1.sum(), m_k2.sum(), m_k3p.sum()))
