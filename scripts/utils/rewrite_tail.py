# -*- coding: utf-8 -*-
path = "/mnt/user-data/outputs/IWS_classe_axiomes_reflexions.md"
with open(path, encoding="utf-8") as f:
    text = f.read()

anchor = "## 5. Questions ouvertes consolidées"
idx = text.find(anchor)
if idx == -1:
    raise SystemExit("ancre introuvable")
head = text[:idx]

new_tail = """## 5. Questions ouvertes consolidées

Liste refondue : les renvois pointaient auparavant sur la numérotation interne du .tex v4, aujourd'hui sans objet (le texte en est à la V5.3.2). Ce qui suit distingue ce qui reste vraiment ouvert de ce qui est réglé depuis, pour ne plus rouvrir ce qui ne l'est plus.

**Socle et sémantique du noyau (Tome I — hors périmètre strict du candidat de classe)**
1. Kairos au contact plutôt qu'à la sortie : ce choix doit-il être assumé explicitement dans le Tome I, avec la discontinuité aux contacts tangents qu'il entraîne ?
2. Les hypothèses de la proposition d'invariance suffisent-elles en général, ou le noyau est-il un cas favorable (C fermé, garde scalaire) ?

**Candidat de classe (V5.3.2) — ce qui reste réellement ouvert**
3. **C5** (fermeture de la boucle historique) : la piste actuelle passe par le préordre de simulation ⪯ sur F_y plutôt que l'égalité stricte ∼_N (§4.1) ; les quantificateurs exacts ne sont pas encore stabilisés.
4. **G₂** (temps intrinsèque) : différé tant qu'aucun témoin ne l'exige — inchangé depuis la V5.3.2.
5. Structure du monoïde 𝔐 : libre sur les épisodes, ou quotienté par des relations temporelles (fusion des délais) ? Question indépendante du candidat C23, toujours ouverte.
6. Unification catégorique (inclusions, écritures/lectures, quotients comme une même structure) : la charpente existe (𝔥_G, 𝔥_G^obs, flèches structurelles/événementielles), mais aucun énoncé ne dit encore qu'il s'agit d'une seule structure catégorique au sens fort.
7. Distinguer une réduction suffisante sous protocole d'un quotient de Nerode complet : ce n'est plus une question isolée, c'est l'objet même du chantier §4 (∼_N, préordre ⪯, stratification par Aut(A), lemme combinatoire de sélection équivariante).
8. À quel moment la stratification, l'o-minimalité ou le temps propre deviennent-ils nécessaires : en cours de test au §4 (crash-tests d'équivariance sur le témoin N=6), pas encore tranché — mais la question a maintenant un terrain concret plutôt que rhétorique.
9. S_𝒜 et Ω_{𝒫,ρ} (Annexe H, construction écrire/lire) comme deux types de flèches composables catégoriquement : en réserve, non repris depuis que le candidat passe par ρ_X = (π_s, ρ_int) — à réexaminer seulement si un défaut précis le demande.

**Résolu depuis — à ne plus rouvrir**
- Le cadre I1/I2/I3 comme axiomes constitutifs est abandonné depuis la V5.2, remplacé par C0, C1, C23^pot, C4 (§3.13 et suivantes). Les anciennes questions d'architecture qui en dépendaient (choix entre deux architectures de définition, clause causale d'I2, notation d'une valeur propre, statut de S_Δ vis-à-vis d'I2) n'ont plus d'objet : I1_ρ et I2 ne sont plus que la taxonomie diagnostique de la §6 du .tex (I1_ρ^F/D/K*, I2^F/D/K*), explicitement non constitutive.
- Transport de la composante historique par les morphismes : répondu — une flèche structurelle transporte la divergence de H^{s,ord} (Proposition, § Morphismes du .tex) ; C23^pot n'est en revanche invariant que sous isomorphisme structurel observationnel.
- Entrée d'une condition observationnelle (ψ) dans les flèches : répondu, ψ_X fait partie de la définition même de flèche observationnelle depuis la V5.3.
- Convention π_s = r_s ∘ ρ_X : adoptée (§3.10).
- Un graphe relationnel est-il constitutif ? Non, c'est un choix de réalisation du noyau — inchangé.
- La bornitude appartient-elle à la classe ? Non, conséquence de la saturation tanh du noyau — inchangé.
- Fermeture par composition et identités des catégories 𝔥_G : résolue, §2.3.
- Stabilité de X^adm : pas d'hypothèse séparée, l'invariance fait partie de la définition d'« admissible », §2.5.
- Départage par indice (Kairos simultanés, classement de similarité) : n'est pas un artefact d'implémentation, c'est une nécessité combinatoire dès qu'une multiplicité de nœuds coïncide (§4.3).

**Corrections éditoriales encore à vérifier dans le Tome I / v4**
- 𝒢_N → 𝔊_N (notation du graphe dans l'espace des états).
- Harmonisation de la règle de saut (r_P Θ) entre le Tome I et l'Annexe A — à confirmer si déjà reportée.

## 6. Piste Lean (mise à jour, V5.3.2)

```
structure HybridCore where
  X : Type*
  C D : Set X                -- C flot, D saut ; C ∩ D = frontière, saut prioritaire
  F : ...                    -- générateur continu, défini au voisinage de C
  K : D → X                  -- saut ponctuel (granularité G₀)
  exec : ...                 -- priorité au premier contact, départage déterministe
  h1_exist_unique : ...
  h2_det_simultane : ...     -- inclut le départage par indice, cf. §4.3
  h3_priorite_saut : ...
  h4_nonZeno : ...
  h_adm_invariant :          -- invariance d'admissibilité (encadré du socle)
    ∀ x₀ ∈ C, ∀ H ∈ Madm x₀, ∀ t j, γ x₀ H t j ∈ C

-- La lecture ρ_X n'est plus un champ de HybridCore : c'est la donnée
-- d'une Présentation, distincte de S (C0 ne porte que sur S).
structure Presentation (S : HybridCore) where
  Sstruct Yint : Type*
  π_s    : S.X → Sstruct
  ρ_int  : S.X → Yint
  Madm   : (x : S.X) → x ∈ S.C → Set Monoid.M
  h_pis_const_flot : ...                         -- π_s constante pendant le flot
  h_prefix_compat :                              -- H₀⁻¹ Madm x₀ = Madm (End x₀ H₀)
    ∀ x₀ H₀, Madm.continuations x₀ H₀ = Madm (End x₀ H₀)

def responseInterne (P : Presentation S) (x : S.X) :
    Madm x → Traj P.Yint :=
  fun H => P.ρ_int ∘ (γ x H)                     -- application partielle R_x^{ρ_int}

def RepMax (P : Presentation S) (s : P.Sstruct) : Set (Madm-indexed → Traj P.Yint) :=
  { R | ∃ x, P.π_s x = s ∧ x ∈ S.C ∧ R = responseInterne P x }

structure IWSCandidate (S : HybridCore) (P : Presentation S) where
  -- C0 : porté par HybridCore lui-même, rien à ajouter ici
  -- C1 : porté par h_pis_const_flot de Presentation
  h_C23pot :                                     -- témoin de H_ρ^{s,ord,max}
    ∃ x₀ H₁ H₂ H', divergence_ordinale (mot P x₀ H₁) (mot P x₀ H₂) ∧
      RepMax P (mot_k 1) ≠ RepMax P (mot_k 2)     -- à la première position de divergence
  -- C4 : fait définitionnel — aucun champ objectif/récompense/cible n'apparaît
  --      dans la signature de HybridCore ni de Presentation

-- Chantier ouvert (§4) : formaliser ∼_N sur une fibre d'opacité ρ_X⁻¹ y
-- comme égalité de responseInterne à domaine égal, puis le préordre ⪯
-- (inclusion de domaine + restriction égale) pressenti pour C5.
def NerodeEquiv (P : Presentation S) (x x' : S.X) : Prop :=
  P.ρ_X x = P.ρ_X x' ∧
  ∃ (h : Madm x = Madm x'), responseInterne P x = responseInterne P x' ∘ (cast h)
```

Changements par rapport à la version précédente de cette esquisse : `ρ` quitte `HybridCore` pour devenir un champ de `Presentation`, distinct de `S` (exactement la distinction C0/C1 de la V5.3.2) ; `h_I1`, `h_I2`, `Experiment`, `Hom` disparaissent avec le cadre I1/I2/I3 ; `RepMax` et `responseInterne` remplacent l'ancien couple observation/lecture ; le chantier `NerodeEquiv` est ajouté comme prochaine cible naturelle, non encore formalisée dans le .tex lui-même. Les morphismes structurels (f, ψ_s, ψ_int bijectifs) restent à écrire ; ils suivent directement la définition du .tex (§ Morphismes) et n'ont pas encore été portés ici faute d'un besoin de preuve qui les exige — cohérent avec la méthode « ne rien ajouter tant qu'un défaut précis ne l'exige pas ».
"""

text = head + new_tail
with open(path, "w", encoding="utf-8") as f:
    f.write(text)
print("Nouvelle longueur :", len(text.splitlines()), "lignes")
