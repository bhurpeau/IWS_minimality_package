"""Cas adverse du lemme de Cauchy : q(s) = 1 + s^2/z0^2 (zeros a +- i z0, rayon de convergence de sqrt(q) egal a z0 exactement) ; le reste vrai (formule binomiale exacte) doit rester <= R."""
import sys; sys.path.insert(0,'.')
import certif_episodes as C
from certif_episodes import *
import mpmath as mp
mp.mp.dps=100
K=C.ORD
# q = 1 + z^2/z0^2 (zeros at +-i z0), sqrt(q) radius of convergence z0 ; x=1, y=z/z0
for z0f in (fmpq(1,10), fmpq(1,3), fmpq(2,1)):
  for hh in (fmpq(1,100),fmpq(1,50), fmpq(1,20)):
    z0=arb(z0f)
    cx=[arb(1)]+[arb(0)]*K
    cy=[arb(0), 1/z0]+[arb(0)]*(K-1)
    try:
        g,R,mult=C.norm_taylor(cx,cy,0,hh,K)
    except C.PressureUnsound:
        print(z0f,hh,'unsound'); continue
    h=mp.mpf(int(hh.numerator))/int(hh.denominator); z=mp.mpf(int(z0f.numerator))/int(z0f.denominator)
    # exact series of sqrt(1+w^2), w=s/z : sum binom(1/2,k) w^{2k}
    poly=sum(mp.binomial(mp.mpf(1)/2,k)*(h/z)**(2*k) for k in range(K//2+1))
    exact=mp.sqrt(1+(h/z)**2)
    rem=abs(exact-poly)
    Rf=mp.mpf(R.upper().mid().str(60,radius=False))
    print("z0=%s h=%s mult=%d  vrai reste %.3e  <= R %.3e  %s"%(z0f,hh,mult,float(rem),float(Rf),'OK' if rem<=Rf else 'VIOLATION'))
