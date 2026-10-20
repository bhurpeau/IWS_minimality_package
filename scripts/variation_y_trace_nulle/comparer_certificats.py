"""Compare les deux certificats (certif_episodes.py vs certif_independant.py) en arithmetique rationnelle exacte (fractions.Fraction) :
 - les encadrements de T_r doivent se recouper (ils enclosent tous deux le meme T_r vrai) ;
 - les intervalles de cosinus doivent se recouper (idem) ;
 - les mots (retires/ajoutes/voisins) doivent coincider ;
 - on rapporte les minorants (pente, marges, ecarts de pression) des deux methodes ; chacun est un minorant de la meme quantite vraie."""
import json, os
from fractions import Fraction as Fr
d = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(d, 'certificat_episodes.json')))['episodes']
B = json.load(open(os.path.join(d, 'certificat_independant.json')))['episodes']
f = lambda s: Fr(s)
ok = True
print("%-3s %-6s %-9s %-9s | %-10s %-10s | %-10s %-10s | %-10s %-10s | %s" % ("r", "T-recoup", "cos-recoup", "mot", "pente V1", "pente V2", "marge V1", "marge V2", "ecart V1", "ecart V2", "largeurs T (V1 / V2)"))
for a, b in zip(A, B):
    r = a['rank']
    ta = (f(a['T_lo']), f(a['T_hi'])); tb = (f(b['T_lo']), f(b['T_hi']))
    t_ok = max(ta[0], tb[0]) <= min(ta[1], tb[1])
    cos_ok = True
    for key in ('cos_neighbours', 'cos_nonneighbours'):
        for j in a[key]:
            ia = (f(a[key][j][0]), f(a[key][j][1])); ib = (f(b[key][j][0]), f(b[key][j][1]))
            cos_ok &= max(ia[0], ib[0]) <= min(ia[1], ib[1])
    word_ok = (a['removed'] == b['removed'] and a['added'] == b['added'] and a['new_neighbours'] == b['new_neighbours'] and a['trigger'] == b['trigger'])
    ok &= t_ok and cos_ok and word_ok
    mA = a['margin_removal_lower_dec'] or a['margin_addition_lower_dec']; mB = b['margin_removal_lower_dec'] or b['margin_addition_lower_dec']
    print("%-3d %-8s %-10s %-9s | %-10s %-10s | %-10s %-10s | %-10s %-10s | %.2e / %.2e" % (r, t_ok, cos_ok, word_ok, a['slope_lower_dec'], b['slope_lower_dec'], mA, mB,
          a['pressure_gap_lower_dec'], b['pressure_gap_lower_dec'], float(ta[1] - ta[0]), float(tb[1] - tb[0])))
print("TOUT COHERENT" if ok else "INCOHERENCE")
