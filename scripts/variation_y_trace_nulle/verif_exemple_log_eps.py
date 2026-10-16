"""Exemple de netteté de l'echelle eps^2 |ln eps| : a_eps(th)=eps(1+th), |th|<1/2 (aucun zero => (U3) triviale).
F_eps(th)=Phi(a_eps(th)), F''(0)=Phi''(eps)*eps^2 avec Phi''(a)=2 arsinh(1/a)-2/sqrt(1+a^2) (formule de la note ordre).
On compare a 2 eps^2 ln(1/eps) ; difference attendue O(eps^2). Verification aussi par differences finies de Phi(eps(1+th)) (mpmath 40 chiffres)."""
from mpmath import mp, mpf, asinh, sqrt, log, quad
mp.dps=40
Phi=lambda a: quad(lambda t: sqrt(t*t+a*a),[-1,0,1])
def Phi2(a): return 2*asinh(1/a)-2/sqrt(1+a*a)
print("eps, F''(0) formule, F''(0) diff. finies, 2 eps^2 ln(1/eps), (F''-2eps^2 ln(1/eps))/eps^2")
for e in [mpf(10)**(-k) for k in (1,2,3,4)]:
    F=lambda th: Phi(e*(1+th)); h=mpf(10)**(-8)
    fd=(F(h)-2*F(0)+F(-h))/h**2
    f=Phi2(e)*e*e; ref=2*e*e*log(1/e)
    print(f"{float(e):8.0e}  {float(f):.6e}  {float(fd):.6e}  {float(ref):.6e}  {float((f-ref)/e**2):.4f}")
