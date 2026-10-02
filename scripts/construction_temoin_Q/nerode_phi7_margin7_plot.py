"""
Visualisation du mecanisme margin7 (verification de l'hypothese de Benoit) :
plan (margin7_x, margin7_xp) signes, par chambre. Le flip de signe (quadrants
haut-gauche / bas-droite) doit coincider EXACTEMENT avec k_min=2 ; la distance
a l'origine dans les quadrants "meme signe" doit ordonner k2 < k3p < non-sep.
"""
import pickle, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = pathlib.Path(__file__).resolve().parent
def _lp(name): return str(_HERE / name)
_FIGDIR = _HERE / "figures"; _FIGDIR.mkdir(exist_ok=True)

d = pickle.load(open(_lp('phi7_delta60_margin7_signed.pkl'), 'rb'))
fd = d['fd']; margin7_x = d['margin7_x']; margin7_xp = d['margin7_xp']
chamber1_x = d['chamber1_x']; chamber1_xp = d['chamber1_xp']
ks = np.array([k if k is not None else -1 for k in fd])
no_leak = np.array([cx==cxp for cx,cxp in zip(chamber1_x, chamber1_xp)])
chambers_key = np.empty(len(chamber1_x), dtype=object)
for i,c in enumerate(chamber1_x):
    chambers_key[i] = tuple(sorted(c)) if c else None
both_valid = no_leak & ~np.isnan(margin7_x) & ~np.isnan(margin7_xp)

def chamber_mask(chamber):
    return np.array([c==chamber for c in chambers_key])

CAT = {
    "non-sep": dict(color="#b5b5b2", marker="o", s=30, alpha=0.75, edgecolor="none", label="non separe (k$\\leq$4)", z=1),
    "k2":      dict(color="#D55E00", marker="^", s=46, alpha=0.95, edgecolor="black", label="separe k=2", z=3),
    "k3p":     dict(color="#0072B2", marker="s", s=38, alpha=0.95, edgecolor="black", label="separe k$\\geq$3", z=2),
}

fig, axes = plt.subplots(1, 2, figsize=(12.5, 6.0), dpi=150)
for ax, chamber in zip(axes, [(1,4,5),(2,4,5)]):
    mask = both_valid & chamber_mask(chamber)
    lim = max(np.abs(margin7_x[mask]).max(), np.abs(margin7_xp[mask]).max()) * 1.08
    ax.axhline(0, color="#898781", lw=0.8, zorder=0)
    ax.axvline(0, color="#898781", lw=0.8, zorder=0)
    ax.plot([-lim,lim],[-lim,lim], color="#e1e0d9", lw=0.8, zorder=0)
    for key, sel in [("non-sep", ks==-1), ("k2", ks==2), ("k3p", ks>=3)]:
        sub = mask & sel
        if sub.sum()==0: continue
        c = CAT[key]
        ax.scatter(margin7_x[sub], margin7_xp[sub], c=c["color"], marker=c["marker"],
                   s=c["s"], alpha=c["alpha"], edgecolors=c["edgecolor"], linewidths=0.8, zorder=c["z"])
    ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim)
    ax.set_xlabel(r"margin7($x$) = sim$_{nn}(7,x)$ $-$ seuil")
    ax.set_title(r"$A_1=\{%s\}$  (n=%d)" % (",".join(map(str,chamber)), mask.sum()), fontsize=10.5)
    ax.grid(True, color="#f0efec", linewidth=0.5, zorder=0)
    for spine in ax.spines.values(): spine.set_color("#cfcfcb")
axes[0].set_ylabel(r"margin7($x'$)")

handles = [plt.Line2D([0],[0], marker=CAT[k]["marker"], color="none", markerfacecolor=CAT[k]["color"],
                       markeredgecolor=CAT[k]["edgecolor"] if CAT[k]["edgecolor"]!="none" else CAT[k]["color"],
                       markersize=8, label=CAT[k]["label"]) for k in ["non-sep","k2","k3p"]]
fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=9.5, bbox_to_anchor=(0.5,-0.02))
fig.suptitle(r"Marge signee du noeud 7 au seuil d'ajout du 2e Kairos ($x$ vs $x'$) — temoin $\varphi_7$, $\delta=60°$"
             "\n" r"quadrants opposes (flip de signe) $\Leftrightarrow$ $k_{min}=2$ exactement (100%, n=771 hors fuite k=1)",
             fontsize=10.5, y=1.05)
fig.tight_layout(rect=[0,0.04,1,0.90])
fig.savefig(str(_FIGDIR/'margin7_signe_x_xp.png'), bbox_inches="tight", dpi=150)
print("Figure sauvegardee ->", _FIGDIR/'margin7_signe_x_xp.png')
