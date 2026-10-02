import io, contextlib, re, numpy as np
src = open('../axiomes_crash_tests/temoin_C23_noyau.py').read()
src = src.split("# ---------------- 3.")[0]
def run(amp, U, beta=None, zeta=None):
    s = src.replace("amp = 0.2", f"amp = {amp}").replace("U = 2.5", f"U = {U}")
    if zeta is not None: s = s.replace("zeta, alpha, beta = 0.8, 0.45, 0.12", f"zeta, alpha, beta = {zeta}, 0.45, 0.12")
    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(s, g)
    o1, o2 = g['out'][1], g['out'][-1]
    nth = [int((o['pre'][3] >= g['Theta']).sum()) for o in (o1, o2)]
    sim = o1['info']['sim']; marg = abs(sim[1]-sim[2]) if o1['info']['i']==0 else np.nan
    return dict(Pmax=max(g['res'][1]['Pmax'], g['res'][-1]['Pmax']), diff=bool((g['A1']!=g['A2']).any()),
                istar=(o1['info']['i'], o2['info']['i']), nth=nth, marg=round(marg,4), t=round(o1['t'],3),
                gap12=round(sim[1]-sim[3],3) if o1['info']['i']==0 else None)
print("base", run(0.2, 2.5))
for amp in (0.05, 0.1, 0.2, 0.3):
    for U in (1.5, 2.5, 4.0):
        print(amp, U, run(amp, U))
for z in (0.4, 1.2):
    print("zeta", z, run(0.2, 2.5, zeta=z))
