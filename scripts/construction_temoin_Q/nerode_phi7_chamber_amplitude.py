"""
Benoit : meme carte R_{0,A}^(1,2) par chambre, mais coloree par AMPLITUDE du
protocole (rampe sequentielle continue) plutot que par k_min -- pour tester
si le gradient k=2/k>=3 observe le long de la bande diagonale (A1={1,4,5})
se superpose a un gradient d'amplitude. La forme du marqueur reste le
k_min (encodage secondaire), pour lire les deux dimensions a la fois.

Source : memes caches que nerode_phi7_chamber_maps.py + phi7_amps.npy
(meme grille, memes indices).
"""
import sys, pickle, pathlib, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

_HERE = pathlib.Path(__file__).resolve().parent
def _lp(name): return str(_HERE / name)
_FIGDIR = _HERE / "figures"
_FIGDIR.mkdir(exist_ok=True)

theta1 = np.load(_lp('phi7_theta1.npy')); theta2 = np.load(_lp('phi7_theta2.npy'))
alive = np.load(_lp('phi7_alive.npy'))
amps = np.load(_lp('phi7_amps.npy'))
d = pickle.load(open(_lp('phi7_delta60_chambers.pkl'), 'rb'))
fd = d['fd']; chamber1_x = d['chamber1_x']

ks = np.array([k if k is not None else -1 for k in fd])
chambers_key = np.empty(len(chamber1_x), dtype=object)
for _i, _c in enumerate(chamber1_x):
    chambers_key[_i] = tuple(sorted(_c)) if _c else None
valid = alive & ~np.isnan(theta1) & ~np.isnan(theta2)

PANELS = [((1,4,5), "A_1=\\{1,4,5\\}"), ((2,4,5), "A_1=\\{2,4,5\\}"), ((2,4,6), "A_1=\\{2,4,6\\}\\ (temoin\\ negatif)")]

# rampe sequentielle bleue (palette.md, 100->700), une seule teinte, continue
SEQ_HEX = ["#cde2fb","#9ec5f4","#6da7ec","#3987e5","#1c5cab","#0d366b"]
cmap = LinearSegmentedColormap.from_list("seq_blue", SEQ_HEX)

MARK = {"non-sep": dict(marker="o", label="non separe (k$\\leq$4)"),
        "leak_k1": dict(marker="x", label="separe k=1 (fuite)"),
        "k2":      dict(marker="^", label="separe k=2"),
        "k3p":     dict(marker="s", label="separe k$\\geq$3")}

def chamber_mask(chamber):
    return np.array([c == chamber for c in chambers_key])

def circ_center(deg):
    ang = np.radians(deg)
    return np.degrees(np.arctan2(np.mean(np.sin(ang)), np.mean(np.cos(ang)))) % 360

def unwrap_around(deg, center):
    return ((deg - center + 180) % 360) - 180 + center

fig, axes = plt.subplots(1, 3, figsize=(17.5, 5.8), dpi=150)
vmin, vmax = amps.min(), amps.max()

for ax, (chamber, title) in zip(axes, PANELS):
    m_ch = valid & chamber_mask(chamber)
    n_tot = m_ch.sum()
    c1 = circ_center(theta1[m_ch]); c2 = circ_center(theta2[m_ch])
    theta1_p = unwrap_around(theta1, c1); theta2_p = unwrap_around(theta2, c2)

    masks = {"non-sep": m_ch & (ks == -1), "leak_k1": m_ch & (ks == 1),
             "k2": m_ch & (ks == 2), "k3p": m_ch & (ks >= 3)}

    sc = None
    for key in ["non-sep", "leak_k1", "k2", "k3p"]:
        mask = masks[key]
        if mask.sum() == 0:
            continue
        spec = MARK[key]
        edge = "black" if key in ("k2","k3p") else ("none" if key=="non-sep" else None)
        sc = ax.scatter(theta1_p[mask], theta2_p[mask], c=amps[mask], cmap=cmap,
                         vmin=vmin, vmax=vmax, marker=spec["marker"],
                         s=46 if key!="non-sep" else 30,
                         alpha=0.95 if key!="non-sep" else 0.8,
                         edgecolors=edge, linewidths=0.9, zorder=3 if key!="non-sep" else 1)

    if sc is not None:
        cb = fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
        cb.set_label("amplitude", fontsize=9)

    pad = 8
    if n_tot>0:
        ax.set_xlim(theta1_p[m_ch].min()-pad, theta1_p[m_ch].max()+pad)
        ax.set_ylim(theta2_p[m_ch].min()-pad, theta2_p[m_ch].max()+pad)
    ax.set_title("$%s$\n(n=%d, recentre autour de %.0f°/%.0f°)" % (title, n_tot, c1, c2), fontsize=10)
    ax.set_xlabel(r"$\theta_1$ (deg, recentre)")
    ax.grid(True, color="#e8e8e5", linewidth=0.6, zorder=0)
    for spine in ax.spines.values():
        spine.set_color("#cfcfcb")

axes[0].set_ylabel(r"$\theta_2$ (deg, recentre)")

handles = [plt.Line2D([0],[0], marker=MARK[k]["marker"], color="none",
                       markerfacecolor="#6da7ec", markeredgecolor="black" if k in ("k2","k3p") else "#6da7ec",
                       markersize=8, label=MARK[k]["label"]) for k in ["non-sep","k2","k3p","leak_k1"]]
fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=9.5, bbox_to_anchor=(0.5,-0.04))
fig.suptitle(r"$\mathcal{R}_{0,A_1}^{(1,2)}$ colore par amplitude du protocole (forme = $k_{min}$) — temoin $\varphi_7$, $\delta=60°$",
             fontsize=11.5, y=1.03)
fig.tight_layout(rect=[0,0.05,1,0.97])
fig.savefig(str(_FIGDIR / 'R0_A1_amplitude_colored.png'), bbox_inches="tight", dpi=150)
print("Figure sauvegardee ->", _FIGDIR / 'R0_A1_amplitude_colored.png')

# test quantitatif : amplitude moyenne par categorie, par chambre (le gradient
# visuel doit se traduire par un ordre net des moyennes si l'hypothese tient)
print("\nAmplitude moyenne (+/- ecart-type) par categorie et par chambre :")
for chamber, title in PANELS:
    m_ch = valid & chamber_mask(chamber)
    if m_ch.sum()==0: continue
    print(" ", chamber)
    for key in ["non-sep","k2","k3p","leak_k1"]:
        mask = m_ch & ({"non-sep": ks==-1, "leak_k1": ks==1, "k2": ks==2, "k3p": ks>=3}[key])
        if mask.sum()==0: continue
        print("    %-9s n=%3d  amp_moy=%.2f  amp_std=%.2f  [amp_min=%.2f amp_max=%.2f]" %
              (key, mask.sum(), amps[mask].mean(), amps[mask].std(), amps[mask].min(), amps[mask].max()))
