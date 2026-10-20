# Audit du reste de Cauchy de `certif_episodes.py` (norm_taylor / PTaylor)

Statut : preuve écrite et relue ligne à ligne contre le code ; confirmée par trois contrôles numériques indépendants (cf. `sortie_audit_cauchy.txt`, `sortie_comparaison_V1_V2.txt`). Non relue par une personne tierce.

## 1. Énoncé

**Lemme A (racine d'un polynôme).** Soient `x̂(s) = Σ_{k=0}^{n-1} a_k s^k` et `ŷ(s) = Σ b_k s^k` à coefficients réels (ici : boules), `q = x̂² + ŷ² = Σ q_k s^k` (degré ≤ 2n−2), `q_0 > 0`, `a ∈ ℕ`. Soit `r > 0` tel que
`S(r) := Σ_{k≥1} |q_k| r^k ≤ q_0 / 2`.
Alors, pour `0 ≤ s ≤ h < r`, `g(s) := s^a √q(s)` (norme de `s^a (x̂, ŷ)`) vérifie, avec `x = h/r`, `M = √(3 q_0 / 2)` et `g_j` les coefficients de Taylor de `s ↦ s^a √q(s)` à l'origine :

`| g(s) − Σ_{j ≤ K} g_j s^j | ≤ h^a · M · x^{K−a+1} / (1 − x).`

*Preuve.* (i) Pour `|s| ≤ r` (complexe), `|q(s) − q_0| ≤ S(r) ≤ q_0/2` : `q(s)` reste dans le disque de centre `q_0` et de rayon `q_0/2`, donc dans le demi-plan `Re > 0` où la racine principale est holomorphe ; `√q` est donc holomorphe sur le disque fermé `|s| ≤ r`. (ii) Sur ce disque `|q| ≤ q_0 + q_0/2`, donc `|√q| ≤ M`. (iii) Estimée de Cauchy : les coefficients `c_j` de `√q` vérifient `|c_j| ≤ M / r^j`. (iv) Sur `ℝ_+`, `q > 0` et la racine principale est la racine positive : `√q(s) = ‖(x̂, ŷ)(s)‖`. (v) Pour `s ∈ [0, h]` : `|√q(s) − Σ_{j ≤ K−a} c_j s^j| ≤ Σ_{j>K−a} M (s/r)^j ≤ M x^{K−a+1}/(1−x)`. Multiplication par `s^a ≤ h^a`. ∎

Les coefficients `c_j` (`j ≤ K−a`) ne dépendent que de `q_0, …, q_{K−a}` : le code les calcule par `arb_series(qc[:kk+1]).sqrt()`.

**Proposition B (pression).** Sur un pas `[0,h]` où l'état vérifie `x(s) = Σ_{k ≤ ORD} c_k s^k + ρ_L s^{ORD+1}` (Lagrange sur la boîte d'enclosure a priori), posons `H_poly`, `V_poly` les polynômes, `e_H = ‖ρ_L^H‖ h^{ORD+1}`, `e_V` idem. Soit `P_poly` le polynôme de Taylor de degré `K+1` de `P' = g_K − k₃ P` (`g_K` = troncature de `k₁‖H_poly‖ + k₂‖V_poly‖`, coefficients du lemme A, `P_{k+1} = (g_k − k₃ P_k)/(k+1)`). Alors pour `s ∈ [0,h]`
`|P_vrai(s) − P_poly(s)| ≤ s · [ k₁(R_H + e_H) + k₂(R_V + e_V) + k₃ |P_{K+1}| h^{K+1} ]`.

*Preuve.* `E := P_vrai − P_poly` vérifie `E' = −k₃ E + (g_vrai − g_K) − ρ` avec `E(0)=0` (la boule `P(0)` est portée par le coefficient `P_0`) et `ρ = k₃ P_{K+1} s^{K+1}` (résidu de la troncature, calculé en dérivant `P_poly`). Posons `η := (g_vrai − g_K) − ρ`, de sorte que `E' = −k₃ E + η`. Comme `|g_vrai − g_poly| ≤ k₁ e_H + k₂ e_V` (la norme euclidienne est 1‑lipschitzienne) et `|g_poly − g_K| ≤ k₁ R_H + k₂ R_V` (lemme A), on a `|η(u)| ≤ δ` pour tout `u ∈ [0,h]`, avec `δ := k₁(R_H+e_H) + k₂(R_V+e_V) + k₃|P_{K+1}|h^{K+1}`. Par variation des constantes, `E(0)=0` donne `E(s) = ∫₀ˢ e^{−k₃(s−u)} η(u) du`, donc `|E(s)| ≤ (δ/k₃)(1 − e^{−k₃ s}) ≤ s δ`. ∎

*Correction de rédaction (relecture de Benoit) : une version antérieure écrivait « `|E'| ≤ −k₃E + δ` », inégalité injustifiée quand `E < 0`. L'argument ci‑dessus ne l'utilise pas ; la borne et le code sont inchangés.*

## 2. Points de contrôle (écart éventuel entre énoncé et code)

| Point | Verdict |
|---|---|
| Critère `S(r) ≤ q_0/2` : `q_0` doit être un **minorant** de `q_0` sur la boule, `|q_k|` des **majorants** | code : `q0lo` par `abs_lower`, `qabs` par `abs_upper` ✓ |
| `M` doit majorer `|√q|` sur le disque : `√(q_0 + q_0/2)` avec `q_0` **majorant** | code : `q0up = qc[0].abs_upper()` ✓ |
| Coefficients de `q` jusqu'au degré `2n−2` (pas de troncature du produit) | `ctx.cap = 2n+2` ✓ |
| Décalage `s^a` (départ au repos) : coefficients d'indice `< a` exactement nuls | vérifié par `is_zero()` dans `episode1_start` ✓ ; `x = 1/mult` avec `mult ≥ 8` ✓ |
| Reste `h^a M x^{K−a+1}/(1−x)` | code : `R = h^shift * M * x**(kk+1)/(1-x)`, `kk = K − shift` ✓ |
| Reste de Lagrange de l'état : `‖ρ_L‖ h^{ORD+1}` majore l'écart `‖x_vrai − x_poly‖` | `norm_hi(rem)*h^(ORD+1)` ✓ (la norme est prise sur le couple de composantes) |
| Résidu `k₃ P_{K+1} h^{K+1}` | code : `resid` ✓ |
| Concurrents (`pressures_others`, `h = s_end`) : le lemme vaut sur `[0, s_end] ⊂ [0, h]` | ✓ |
| Hypothèse « `P'` ≥ 0 sur le pas » pour la monotonie | `dP_lo = k₁ lo‖H‖ + k₂ lo‖V‖ − k₃ sup P > 0` avec `sup P` = évaluation de `P_poly` sur `[0,h]` ✓ |

Aucun écart trouvé. Deux remarques sans conséquence : (a) le critère de Cauchy est conservateur (rapport reste vrai / R observé ≤ 2·10⁻⁵) ; (b) pour les nœuds non déclencheurs on tolère `mult ≥ 3` (x = 1/3, reste ≈ 10⁻¹²·M) ; les rayons ≈ 10⁻⁸ des pressions des nœuds 2 et 3 dans la sortie viennent, eux, du repli par quadrature de Duhamel (rayon de Cauchy insuffisant pour ces nœuds de très petite norme), qui n'a pas été auditée ligne à ligne ici : elle ne sert qu'à borner des pressions loin de Θ (< 0,83) et n'intervient dans aucune marge critique, à l'exception du concurrent du rang 8 où la seconde implémentation donne une marge indépendante (≥ 0,0043).

## 3. Contrôles indépendants réalisés

1. **Tests unitaires** (`audit_cauchy.py`, partie A) : 80 polynômes aléatoires (66 acceptés par le critère, 14 refusés à juste titre) + 9 cas adverses (q = 1 + s²/z₀², zéros à ±i z₀ ; 5 acceptés, 4 refusés), contre `mpmath` à 120 chiffres : 0 violation du reste, coefficients `g_k` identiques, hypothèse du lemme vérifiée sur le cercle `|s| = r`.
2. **Validation croisée sur les pas réels** (partie B) : 6203 objets `PTaylor` construits par la vraie exécution des huit épisodes ; pour chacun, `P(h)` recalculé par `acb.integral` de FLINT (autre algorithme, contrôle d'analyticité `Re q > 0` écrit à part). Enclosures disjointes : **0** ; plus grand écart de milieux : 3,9·10⁻³¹.
3. **Seconde implémentation complète** (`certif_independant.py`) sans reste de Cauchy écrit à la main ni enclosure de Picard : tube de Gronwall + Cauchy–Kovalevskaya pour l'état, intégrateur de FLINT pour les pressions. Mêmes `T_r`, mêmes mots, mêmes marges de recâblage (cf. `sortie_comparaison_V1_V2.txt`).
