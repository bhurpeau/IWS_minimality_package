"""Temoin numerique du lemme de Glaeser avec marge (complement transmission C^2).
Enonce teste : a in C^2(U'), U'=[-1,1]^2, Da=0 sur Z={a=0} dans U', L>=sup|D^2 a|, delta0 = marge.
Pour tout x avec B(x,delta0) dans U' :  |Da(x)|^2 <= 2 L |a(x)| + (2/delta0) |Da(x)| |a(x)|.
Fonctions : a = eps*(b - b_min + m), b trigonometrique aleatoire (derivees analytiques), b_min = minimum EXACT
(raffine par scipy) atteint a l'interieur de U' => si m=0 le zero est critique ; m>0 => aucun zero.
(Une premiere version utilisait le minimum de grille : le vrai minimum etait plus bas que celui de la grille,
 a avait alors des zeros non critiques, hypothese violee, d'ou un ratio > 1 artificiel.)
"""
import numpy as np
from scipy.optimize import minimize
rng=np.random.default_rng(7)
def make():
    k=rng.normal(size=(4,2))*1.5; ph=rng.uniform(0,6.28,4); am=rng.normal(size=4)
    def b(x,y): return sum(am[i]*np.cos(k[i,0]*x+k[i,1]*y+ph[i]) for i in range(4))
    def db(x,y):
        gx=sum(-am[i]*k[i,0]*np.sin(k[i,0]*x+k[i,1]*y+ph[i]) for i in range(4))
        gy=sum(-am[i]*k[i,1]*np.sin(k[i,0]*x+k[i,1]*y+ph[i]) for i in range(4)); return gx,gy
    def hb(x,y):
        c=[am[i]*np.cos(k[i,0]*x+k[i,1]*y+ph[i]) for i in range(4)]
        return (-sum(c[i]*k[i,0]**2 for i in range(4)),-sum(c[i]*k[i,0]*k[i,1] for i in range(4)),-sum(c[i]*k[i,1]**2 for i in range(4)))
    return b,db,hb
def test(eps,m,delta0=0.3,n=401,trials=60):
    xs=np.linspace(-1,1,n); X,Y=np.meshgrid(xs,xs,indexing='ij')
    inner=(np.abs(X)<=1-delta0)&(np.abs(Y)<=1-delta0)
    worst=0.0; worst_naif=0.0; cnt=0
    while cnt<trials:
        b,db,hb=make(); B=b(X,Y); i0=np.unravel_index(np.argmin(B),B.shape)
        if i0[0] in (0,n-1) or i0[1] in (0,n-1): continue
        res=minimize(lambda p:b(p[0],p[1]),[X[i0],Y[i0]],method='BFGS',tol=1e-14)
        if abs(res.x[0])>=1 or abs(res.x[1])>=1: continue
        bmin=res.fun
        a=eps*(B-bmin+m); gx,gy=db(X,Y); gx*=eps; gy*=eps
        hxx,hxy,hyy=hb(X,Y); L=eps*np.max(np.sqrt(hxx**2+2*hxy**2+hyy**2))
        g2=gx**2+gy**2; g=np.sqrt(g2); aa=np.abs(a)
        mask=inner&(aa>1e-14*eps)
        rhs=2*L*aa+(2/delta0)*g*aa
        worst=max(worst,np.max((g2/rhs)[mask])); worst_naif=max(worst_naif,np.max((g2/(2*L*aa))[mask])); cnt+=1
    return worst,worst_naif,cnt
print("max_x |Da|^2 / second membre ; attendu <= 1 :")
for eps in (1e-1,1e-2,1e-3):
    for m in (0.0,1e-6,1e-2):
        w,wn,c=test(eps,m)
        print(f"eps={eps:6.0e} m={m:6.0e}  avec marge: {w:.3f}   Glaeser nu (2L|a|): {wn:.3f}   ({c} fonctions)")
print("\nzero NON critique a distance d hors de U'=[-1,1] : a=eps*(x-1-d), au point x=1 ; ||Da||^2 ln(1/|a|)/eps = eps*ln(1/(eps*d))")
for eps in (1e-1,1e-2):
    for lnd in (-np.log(1e2),-np.log(1e6),-1.0/eps,-1.0/eps**2):
        print(f"eps={eps:6.0e}  ln d = {lnd:12.1f}   quotient = {eps*(-np.log(eps)-lnd):.3f}")
print("-> avec d = exp(-1/eps^2) le quotient vaut ~1/eps -> infini : sans marge (zero non critique tout pres hors de U') pas de borne O(eps).")
