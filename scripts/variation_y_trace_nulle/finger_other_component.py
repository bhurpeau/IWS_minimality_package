"""Controle : meme diagnostic en variant l'AUTRE composante de H(0) du noeud 0 (COMP=1), puis la composante 0 du noeud 3."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core'))
sys.argv = ['x', '1500']
import finger_critical as C, finger_y_variation as F
for node, comp in [(0, 1), (3, 0)]:
    F.NODE, F.COMP = node, comp
    for e in [-0.3, -0.15, 0.0, 0.15, 0.3]:
        set = C.set_window(200., 228., 1500)
        r = C.traces(e)
        if r is None:
            print("node %d comp %d eta=%+.2f : chemin de reference PERDU (bifurcation de mot)" % (node, comp, e), flush=True); continue
        m = C.measure(e, half=1.5, n_fine=4000)
        print("node %d comp %d eta=%+.2f dmin=%.5f side=%+d roots=%s width=%.4f c4max=%.4f" %
              (node, comp, e, m['dmin'], m['side'], [round(x, 3) for x in m['roots']], m['width'], m['c4max']), flush=True)
