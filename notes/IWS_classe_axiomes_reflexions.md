# Classe IWS — axiomes, objets, transformations (carnet courant)

*Document compagnon du Volume II. **État courant : manuscrit v5.16** (octobre 2026). Ce carnet ne contient que l'état à jour : définitions retenues, résultats acquis, corrections prises en compte, questions réellement ouvertes. Tout l'historique (versions intermédiaires, pistes abandonnées, calculs préliminaires, relectures successives du .tex) est conservé tel quel dans `IWS_classe_axiomes_reflexions_ARCHIVE_chronologique.md`; les renvois « arch. §x.y » y pointent.*

*Statuts épistémiques : [DEF] définition, [CHOIX] choix de modélisation, [PROP] proposition démontrée dans le .tex, [PROP, num.] établie numériquement ou analytiquement dans le carnet mais pas (encore) rédigée comme théorème, [CONJ] conjecture, [OUVERT].*

*Garde-fou épistémique permanent : **✓ est un témoin ; ✗ n'est une preuve que s'il vient d'une obstruction analytique.** Il faut toujours distinguer la famille mathématique 𝒰_j de son échantillon numérique 𝒰̂_j⊂𝒰_j : un ✓ sur 𝒰̂_j est un vrai témoin, un ✗ sur 𝒰̂_j ne dit rien sur 𝒰_j sans argument analytique séparé ou stress-test (densification, profondeur).*

---

## Index

| § | Contenu | Anciens renvois (archive) |
|---|---|---|
| 1 | Définition de la classe : présentation, C0–C4, taxonomie diagnostique | 1.1–1.5, 3.1–3.2, 3.8–3.19 |
| 2 | Socle hybride, admissibilité, granularités, flèches, catégories | 1.2, 1.6–1.11, 2.1–2.5, 3.3–3.7 |
| 3 | Le noyau IWS comme témoin : équations, identifiabilité, atteignabilité, témoin N=6 | 3.20–3.25 |
| 4 | Programme F_y/∼_N : définitions, théorème de complétude, familles séparantes, minimalité | arch. §5 item 12, 4 (intro), 4.17 |
| 5 | Géométrie des partitions 𝒫_k à profondeur finie; §5.8 programme de soustraction (γ₁=λ=0 → condition intrinsèque) | 4.1–4.16, 4.18–4.32 |
| 6 | Manuscrit : état du .tex et points rédactionnels | 4.25–4.29, 4.33–4.34 |
| 7 | Questions ouvertes | arch. §5 |
| 8 | Corrections et affirmations retirées | divers |
| 9 | Notations réservées, scripts et données | — |
| 10 | Esquisse Lean | arch. §6 |

---

## 1. Définition de la classe

### 1.1 Principe et objet présenté

- [CHOIX] Le noyau du Tome I est une **instance** ; la classe 𝔍𝔚𝔖 doit contenir ce que l'appareil des Tomes I–III exige, pas tout ce que le noyau vérifie. Principe de minimalité : objet → obstacle → structure minimale nécessaire.
- [DEF] **IWS présenté** : 𝐒 = (S, ρ_X, π_s, 𝔐^adm), avec
  - S ∈ 𝔥 le système hybride (§2.1) ;
  - ρ_X : 𝒳 → Y la **lecture constitutive d'état**, séparée en ρ_X = (π_s, ρ_int), Y = 𝒮 × Y_int, r_s = pr₁, donc π_s = r_s∘ρ_X (la lecture voit la structure) ;
  - 𝔐^adm = (𝔐^adm_x)_{x∈C} la **famille indexée par l'état** des histoires admissibles (l'union perd l'information d'exécutabilité) ; propriété markovienne ℋ₀⁻¹𝔐^adm_{x₀} = 𝔐^adm_{End(x₀,ℋ₀)}.
  Être IWS est une propriété de l'IWS *présenté*, pas du champ nu (classe non stable par isomorphisme de 𝔥_G, assumé : cohérent avec l'anti-essentialisme). La lecture d'exécution ω̂ n'est pas constitutive (monotonie : le test prend ω̂ = id) ; elle relève des expériences particulières.
- Tour de projections : I × 𝔐^adm —End→ 𝒳 —ρ_X→ Y —r_s→ 𝒮. Fibres de ρ_X = **opacité** ; fibres de π_s = **organisation**. L'historicité H vit dans les fibres de ρ_X (partition de Nerode, §4).
- [CHOIX] La structure est **déclarée**, non restreinte à un mode dénombrable (option (b)) : un poids W ∈ ℝ^{N×N} constant en flot et réécrit aux Kairos est admissible. L'identification des fibres (connexion) n'est pas requise : on compare des fibres par des ensembles de comportements (répertoires), avec quantificateurs ∃/∀.

### 1.2 Historicité effective

- [DEF] **H_{ρ,I,𝔅}** : ∃ x₀∈I, ℋ₁,ℋ₂∈𝔅_{x₀}, ℋ'∈ℋ₁⁻¹𝔅_{x₀}∩ℋ₂⁻¹𝔅_{x₀}, avec x_k = End(x₀,ℋ_k), tels que ρ_X(x₁)=ρ_X(x₂) et les réponses lues R^{ρ}_{x₁}(ℋ') ≠ R^{ρ}_{x₂}(ℋ'). Réponses mesurées *à travers ρ_X* (ω = ω̂∘ρ_{X*}) ; sinon H serait triviale. Monotone en (I,𝔅) : « il existe un régime où H vaut » ⟺ « H vaut au régime maximal (C, 𝔐^adm) » ; on note H_ρ^max.
- Observabilité ≠ historicité : on ne définit pas l'historicité par la non-reconstructibilité.
- [PROP, candidate] H_ρ ⇒ (I1^F ∨ I1^D ∨ I1^{K*} sur le support) ∨ (dynamique lue mal posée). Contre-exemple de la « minuterie dormante » ṙ = 3r^{2/3} : factorisation exacte mais quotient non unique (défaut de détermination), non exclu par une hypothèse lipschitzienne.
- [DEF] **H^{s,ord}** (historicité structurelle d'ordre). Word_s(γ) = red(s∘γ) (suppression des répétitions consécutives). Le cœur : Word_s(γ₁) ⊥ Word_s(γ₂) (**incomparabilité pour l'ordre préfixe**) — le passé peut faire *bifurquer* le mot structurel futur, pas seulement l'accélérer. Invariante par reparamétrisation et par horizon (prolonger la continuation ne défait pas une divergence). Premier temps intrinsèque, sans G₂ ; le compteur y échoue (tous ses mots sont des préfixes de 0,1,2,…). L'injectivité de ψ_s est exactement ce qui empêche une abstraction de recoller deux branches distinctes. H^{s,ord} ⇒ H^s_t (calendrier) ; réciproque réfutée par le compteur.
- [DEF] **H^{s,ord,max}** : version au régime maximal. Les positions 0 coïncident (π_s = r_s∘ρ_X), donc la divergence est à une position k ≥ 1 ; avec ṡ=0 en flot, chaque futur contient un Kairos avec s⁺≠s⁻.

### 1.3 Répertoires et le candidat C0–C4

- [DEF] **Répertoire** : Rep^max(s) = {R_x^{ρ_int} : x ∈ X_s ∩ C} (régime maximal ; ce choix n'est pas justifié par monotonie, il est assumé — C3^rep n'est pas monotone en régime). Rep compare ce qu'une organisation *peut* faire, lu hors de s.
- [DEF] **C23^pot** (efficacité structurelle potentielle) : témoin de H^{s,ord,max} tel qu'à la première position de divergence k, Rep^max(s_k^{(1)}) ≠ Rep^max(s_k^{(2)}). L'histoire choisit entre deux organisations *distinctes* (corrige la « juxtaposition interne », où les branches ne diffèrent que par des modes décoratifs).
- [DEF] **C23^act** (efficacité actualisée) : R^{ρ_int}_{x_k^{(1)}} ∉ Rep^max(s_k^{(2)}) (ou symétriquement) : le comportement de l'état réellement produit est impossible sous l'autre organisation. C23^act ⇒ C23^pot strictement ; le cas de la permutation de contenus cachés est exclu. *Pas axiomatisée* ; IWS exige-t-il l'actualisée, ou la capacité de l'organisation suffit-elle ? (ouvert)
- [CHOIX] **Candidat constitutif retenu** : 𝐒 ∈ 𝔍𝔚𝔖 ssi
  - **C0** — S ∈ 𝔥 (H1–H4) ;
  - **C1** — s est une composante structurelle discrète, π_s = r_s∘ρ_X, ṡ=0 en flot ;
  - **C23^pot** — comme ci-dessus (C2 et C3 fusionnés) ;
  - **C4** — aucun telos primitif (fait définitionnel : aucun champ objectif/récompense/cible dans la signature). L'absence de telos primitif est un axiome de classe ; la non-téléologie dynamique est une propriété étudiée sur des réalisations. Elle n'exclut ni telos locaux, ni environnement téléologique via u(t).
- **C5** reste **volontairement non rouvert** : « la restructuration change-t-elle la manière dont le futur deviendra à son tour passé ? ». Le chantier F_y/∼_N doit d'abord dire ce que C5 devrait mesurer. Candidat pressenti : préordre de simulation x ⪯ x′ ssi 𝔐^adm_x ⊆ 𝔐^adm_{x′} et R_{x′}|_{𝔐^adm_x} = R_x (plutôt que l'égalité stricte ∼_N) ; version « sans identification » : quantifier universellement sur l'autre fibre. Quantificateurs non stabilisés.

### 1.4 Taxonomie diagnostique (non constitutive)

Les anciens axiomes I1/I2/I3 sont **abandonnés comme axiomes depuis la V5.2** (le test de présentation ỹ = y(1+s) montre que I1 existentiel sur les décompositions est quasi vide ; I2 « π_{¬s}𝒦 » mal typé pour le noyau). Il reste une **taxonomie à trois canaux** — F (flot), D (garde / déclenchement), K* (résultat du saut) — qui explique *comment* l'agrégation par ρ_X échoue :

| information causalement efficace | par F | par D | par K* |
|---|---|---|---|
| cachée pour ρ_X | I1^F_ρ | I1^D_ρ | I1^{K*}_ρ |
| structure s écrite discrètement | I2^F | — | I2^{K*} |

- Les lignes structurelles sont retypées par la lecture : I2^F : ∃x₁,x₂, ρ_int(x₁)=ρ_int(x₂), π_s(x₁)≠π_s(x₂), ℒ_Fρ_int(x₁)≠ℒ_Fρ_int(x₂) (idem D, K*). Réserve : x₁,x₂ peuvent aussi différer en contenu caché ; l'attribution à s n'est pas ponctuelle (acceptable pour une taxonomie explicative).
- Deux formes de mémoire silencieuse : **noyau à γ₁=λ=0** = défaut de factorisation, colonne K* (muette dans le flot, décisive au saut ; I1^D vide puisque D est lu par ρ) ; **minuterie dormante** = défaut de détermination (factorisation exacte, quotient non unique). Un défaut de détermination n'est pas un quatrième canal causal.
- Lecture noyau : ρ_ker = (A ; H, V, P) avec π_s = A. [PROP] I1^F_{ρ_ker} ⟺ (γ₁>0 ∨ λ>0). À γ₁=λ=0 le noyau n'a pas de mécanisme caché par F ; il est conservé dans la classe grâce à K*.
- Slogan : *une trace n'a pas besoin d'influencer continûment le présent pour être historiquement causale : elle peut rester silencieuse pendant le flot et devenir décisive au Kairos.*

### 1.5 Contre-exemples de référence (crash-tests de la définition)

| Système | Verdict | Raison |
|---|---|---|
| Témoin continu ẏ=−y+h, ḣ=y−h (autonome) | H échoue | variable cachée mais aucune histoire ne l'écrit différemment ; h = y+ẏ « inertie déguisée » |
| Même témoin avec entrée u | H vaut | commandable ; h devient trace exponentielle du passé de y (verdict dépend de 𝔐^adm) |
| Témoin discret (y,s), ρ_X = id | H échoue | système entièrement lu |
| Compteur (h intégrateur, Kairos à h≥1) | échoue H^{s,ord} | les mots sont des préfixes ; historicité seulement chronologique |
| Juxtaposition S₁×S₂ (mémoire continue × relais hybride lu) | échoue H^s | l'histoire de S₁ ne choisit pas la structure de S₂ |
| Juxtaposition interne (modes a→b ou a→c, Rep(b)=Rep(c)) | échoue C23 | branches décoratives |
| Pendule fatigué (action-angle, s=E) | passe C0–C4 sous option (b) | oblige à déclarer la structure ; « structure » = intégrale première promue par coordonnées |
| S_Δ (réduction homogène du noyau) | ∉ 𝔍𝔚𝔖 | ÃH=H quel que soit A : le graphe est causalement muet, la restructuration décorative ; ι : S_Δ → S reste une flèche légitime de 𝔥_G. Une réduction exacte peut cesser d'être un IWS précisément parce qu'elle a quotienté le mécanisme qui en faisait un IWS |
| Noyau, γ₁=λ=0, ζ>0, u_max>u_crit | IWS (C23^pot et C23^act) | §3 |
| Noyau, u_max<u_crit | pas IWS pour cette présentation | pas de Kairos accessible : τ mémoire morte, π_s constante, H échoue |

*Le noyau n'est pas la définition : un témoin parmi d'autres.*

---

## 2. Socle hybride, granularités, flèches

### 2.1 Socle 𝔥 et admissibilité

- [DEF] S = (𝒳, C, F, D, 𝒦) avec (H1) structure bien définie, (H2) existence et unicité locale du flot, (H3) déterminisme de l'exécution (événements simultanés compris), (H4) non-Zénon. 𝔍𝔚𝔖 ⊆ 𝔥. Ces hypothèses ne caractérisent pas un IWS.
- [CHOIX] **Priorité au saut au premier contact avec D** : règle de sémantique de Exec (dans le cadre hybride standard, flot et saut sont tous deux permis sur C∩D). Statut de Exec : défini extérieurement ou donnée de S — **à inclure dans S lorsqu'il ne se déduit pas de (C,F,D,𝒦)** (retenu en V5).
- [CHOIX] **Kairos au contact** : dans le noyau D ⊋ ∂_exit C possible ; un point P_i=Θ avec Ṗ_i<0 déclenche quand même. Conséquence : dépendance en la condition initiale **discontinue** lorsqu'un événement apparaît/disparaît par contact tangent (seconde source de discontinuité, distincte des changements d'ordre entre Kairos).
- **Admissibilité abstraite** : (X^adm, 𝔐^adm) déclarée, soumise à (a) bonne position H2–H4 depuis X^adm sous 𝔐^adm ; (b) clôture : états atteints dans X^adm, histoires stables par restriction, décalage, concaténation. L'invariance fait partie de la définition d'« admissible » (pas d'axiome H5). Propriété requise : x₀∈C, ℋ∈𝔐^adm_{x₀} ⇒ γ_{x₀,ℋ}(t,j)∈C sur tout le domaine ; alors Supp^max = C et Rep^max(s) = {R_x : x∈X_s∩C}. Option écartée : l'ensemble maximal de bonne position W.
- **Sortie** : x∈∂^𝔅_exit C ⟺ ∃u∈𝔅 ∀ε>0 ∃t∈(0,ε) : φ(t;x,u)∉C. [PROP, candidate] Invariance de C : C, D fermés, flot continu, entrées stables par décalage, ∂_exit C ⊆ D, 𝒦(C∩D) ⊆ C, priorité au premier contact, H4.
- **Règle de saut** : P⁺_{i*} = r_P P⁻_{i*} (général), qui se réduit à r_PΘ sur une exécution admissible (Annexe A à harmoniser).
- **Convention sur u** : L^∞ ; u_max = ess sup d'une entrée donnée, pas un paramètre du modèle.

### 2.2 Granularités et flèches

- **G₀** : f∘γ ∈ Exec(T) sur un même domaine hybride. **G₁** : trajectoire post-cascade γ̄ (par H3–H4, la fermeture de cascade K*(x) est bien définie) *avec ses limites à gauche* : G₁ oublie l'intérieur d'une cascade mais pas ses deux bords (Reach¹ contient les γ̄(t⁻) ; condition de flèche f(γ̄_S(t⁻)) = γ̄_T(t⁻)). **G₂** (reparamétrisation) : **différé** — horloge uniforme ⇒ λ(t)=ct (simple unité de temps) ; horloge propre à chaque exécution ⇒ incompatible avec un η indépendant de x₀ (ressusciterait η̃). 𝔥_{G₀} ⊆ 𝔥_{G₁} ; G₁ canonique (aucun choix de témoin, exact pour la réduction homogène, maniable en Lean).
- **Histoires** : η : 𝔐_S → 𝔐_T morphisme de monoïdes sur les monoïdes ambiants (η(ε)=ε, η(ℋ₁ℋ₂)=η(ℋ₁)η(ℋ₂)), η(𝔅_S) ⊆ 𝔅_T, η indépendant de x₀ ; au niveau de la présentation, η(𝔐^adm_{S,x}) ⊆ 𝔐^adm_{T,f(x)}.
- **Flèche observationnelle** (f, η, ψ_X) : f(C_S) ⊆ C_T, préserve les exécutions (en G_i), ρ_T∘f = ψ_X∘ρ_S, avec **ψ_X = ψ_s × ψ_int et ψ_int indépendant de s** (sinon un ré-étiquetage dépendant de s pourrait égaliser dans T des répertoires distincts dans S). Les commutations f∘Φ=Φ∘f, f∘𝒦=𝒦∘f ne sont que des conditions suffisantes (si f préserve *et réfléchit* les gardes).
- **Hiérarchie G₁** : générales (peuvent effacer tout événement, version ponctuelle) ⊃ **structurelles** (ψ_X produit, ψ_s injective ; n'effacent que les événements avec s⁻=s⁺) ⊃ **événementielles** (préservent les macro-transitions K*). La commutation r_{s,T}∘ψ_X = ψ_s∘r_{s,S} est automatique pour ψ_X produit.
- **Transport** : une flèche structurelle transporte la divergence de H^{s,ord} (injectivité de ψ_s : red∘ψ_s = ψ_s∘red). C23^pot n'est invariant que sous **isomorphisme structurel observationnel** (f, ψ_s, ψ_int bijectifs), pas transporté vers l'avant en général (la cible peut égaliser les répertoires). H se transporte vers l'avant si ψ_ω injective.
- **Catégories** : **IWS**_G (et plus largement 𝔥_G^obs, flèches portant ψ, foncteur d'oubli U vers 𝔥_G) est une catégorie (identité (id,id), composition (g,θ)∘(f,η) = (g∘f, θ∘η)) ; 𝔍𝔚𝔖_G en est la sous-catégorie pleine. On obtient une famille de catégories de *descriptions* indexées par la résolution.
- **Support et quotient** : Reach^G_𝔅(I), Supp^G = I ∪ Reach ; f ∼_G f′ ssi f, f′ coïncident sur Supp (congruence pour la composition). Condition de contenu : Supp ⊊ C_S.
- **Quatre opérations** : inclure, écrire, lire, quotienter. L'annexe H (« écrire puis lire ») est une réduction *suffisante* sous protocole, pas le quotient de Nerode.
- **Cas Δ** : ι : S_Δ → S n'est un morphisme que pour les entrées uniformes (Δ n'est invariante que sous entrée uniforme), et aucun carré commutatif saut par saut n'existe (chaque Kairos homogène = cascade de N sauts dans S).

---

## 3. Le noyau IWS comme témoin (γ₁ = λ = 0)

### 3.1 Équations et règle de Kairos

Ḣ=V ; V̇=−γ₀V−H+ζ tanh(ÃH)+u ; τ̇=α tanh(ÃH)−βτ ; Ṗ=κ₁‖H‖+κ₂‖V‖−κ₃P. Garde D={∃i : P_i≥Θ}, Θ=1,25. Au saut, i*=argmax(P≥Θ) (départage par indice) ; m=min(2,|nb(i*)|,|nn(i*)|) ; on retire les m voisins de plus faible cosinus cos(τ_{i*},τ_j) et on ajoute les m non-voisins de plus fort cosinus (départage par indice croissant) ; rescalage V_{i*}←r_V V_{i*} (0,5), P_{i*}←r_P P_{i*} (0,35) ; similarité 0 si une norme de trace est nulle (Tome I, « Recâblage conservatif » ; Annexe A). Le recâblage est conservatif (degré de i* inchangé).

**Fait structurel central (découplage).** À γ₁=λ=0, ni Ḣ, ni V̇, ni Ṗ ne dépendent de τ ; le saut ne modifie ni H ni τ (seuls V,P en i* sont rescalés, par des constantes). Donc (H,V,P) est **indépendant de τ à tout instant** : τ n'entre dans la dynamique qu'à travers le classement des cosinus au Kairos. Conséquences : (i) deux états de même chemin structurel ont le même y=(A,H,V,P) ; (ii) 𝔐^adm_x ne dépend que de x∈D ou non (donc de P), jamais de τ : l'admissibilité est constante sur F_y.

### 3.2 Identifiabilité universelle de la structure

**[PROP] Lemme d'identifiabilité (γ₁=λ=0, ζ>0).** Pour A≠A′ et tout x∈X_A∩(C∖D) : R_x ∉ Rep^max(A′). Preuve : si les lectures coïncidaient, ζ tanh(BH)=ζ tanh(B′H), donc K:=Ã−Ã′ vérifie KH≡0 (tanh injective), puis KV≡0, puis K V̇ ≡ 0, soit ζK tanh(BH(0)) + K u₀ = 0 pour tout u₀ d'une boule, donc K(u₀−u₁)=0, donc K=0, donc A=A′ (A↦Ã injective). Hypothèses : (i) D est ρ_int-lisible (ne dépend que de P), donc x′∉D et les flots durent le même temps ; (ii) 𝔐^adm_x contient les constantes d'une boule de ℝ^{N×d} (actuation complète, propriété du noyau — Tome I, ‖u_i‖≤u_max — et non hypothèse du socle général) ; (iii) le support hors diagonale de Ã est celui de A. Corollaire : Rep^max(A)≠Rep^max(A′) (X_A∩(C∖D)∋(0,0,τ,0) est non vide). Le lemme n'exige que u_max>0.

### 3.3 Atteignabilité par réflexion (écriture dans τ sans trace lue)

H est une sortie plate de (H,V) : tout chemin H(·) de classe C² est réalisé par u = Ḧ+γ₀Ḣ+H−ζ tanh(ÃH), borné pour une petite amplitude. Depuis (H,V)=0, P₀<Θ : branche 1 = boucle H¹ de 0 à 0 (vitesse nulle aux bouts), branche 2 : H²=−H¹ (u²=−u¹, par imparité de tanh). Alors H(T)=V(T)=0 dans les deux, P¹(T)=P²(T) exactement (Ṗ ne voit que des normes), A inchangé, et τ^{1,2}(T)=e^{−βT}τ₀ ± I : *P est aveugle au signe, τ ne l'est pas*. Trois pièges : (1) **invariance du cosinus** : si τ₀=0 alors τ²=−τ¹ et tous les classements coïncident ; il faut une partie commune non nulle c=e^{−βT}τ₀≠0 ; (2) **localisation** : (ÃH)_{i*}≈0 avec (ÃH)_j≠0, possible ssi i* et j ne sont pas jumeaux (N[i*]≠N[j]) ; (3) **coupure de sélection** : il faut plus de m candidats du côté concerné (par ex. deg(i*)≥3 avec m=2) et que l'*ensemble* sélectionné change. Fenêtre de pertinence : préparer P_{i*} juste sous Θ, continuation commune courte. Sous continuation commune, **τ₁(t)−τ₂(t)=e^{−βt}(τ₁(0)−τ₂(0))** : l'historicité structurelle a une durée de validité (oubli β).

### 3.4 Témoin numérique N=6 (script `temoin_C23_noyau.py`)

Graphe : arêtes (0,1),(0,2),(0,3),(1,4),(2,5),(3,4),(3,5),(4,5) ; i*=0, nb(0)={1,2,3}, nn(0)={4,5}, m=2 ; pas de jumeaux, Ã inversible ; paramètres Annexe F. Boucle H^±=±amp·sin²(πt/T)·v, T=3, (Ãv) supporté sur {1,2}. Pour amp=0,2, U=2,5 : max P=0,574<Θ, max|u|=1,33, écart (H,V,P) entre branches à T ~10⁻¹³, τ⁺−τ⁻=(0,−0,224) sur les nœuds 1,2 seuls ; Kairos à t*=1,446 dans les deux branches ; classement 1↔2 inversé (cos 0,9915/0,9462) ; branche + retire {3,2}, branche − retire {3,1}, les deux ajoutent {4,5} ; A₁⁺≠A₂⁺, marge 0,045. Balayage amp∈{0,05…0,3}×U∈{1,5…4}×ζ∈{0,4…1,2} : A₁⁺≠A₂⁺ partout ; marge ≈ linéaire en amp ; toute amp∈(0 ; 0,43) convient. Argument C23^act : un x′∈X_{A₂⁺}∩C de même lecture a même (H,V,P) ; sous u=0, V̇(0⁺) diffère de ζ[tanh(Ã₁⁺H)−tanh(Ã₂⁺H)]≠0 quel que soit τ(x′) ⇒ R_{x₁}∉Rep^max(A₂⁺).
Précision (somme) : (Ã₁⁺−Ã₂⁺)H sur la ligne i* porte sur des *sommes* Σ_{j∈N₁∖N₂}H_j ≠ Σ_{j∈N₂∖N₁}H_j (le degré de i* est conservé) ; les lignes des voisins échangés offrent d'autres chances de discrimination.

### 3.5 Borne sur u

Si 𝔐^adm = entrées mesurables bornées sans borne fixée, rien à ajouter. Avec borne fixée : écriture et identifiabilité passent pour tout u_max>0, mais **atteindre un Kairos demande u_max>u_crit** ; forçage résonant du seul nœud 0 depuis le repos : max P=1,14<Θ pour U=0,3 ; Θ atteint à t=6,5 pour U=0,5 ⇒ **u_crit ≲ 0,33** pour cette stratégie (borne supérieure, pas l'optimum). [CONJ] u_crit>0 (ζ<1, ‖Ã‖_∞=1 : non-linéarité contractante).

---

## 4. Programme F_y/∼_N : définitions, complétude, familles séparantes, minimalité

### 4.1 Définitions

- Fibre d'opacité F_y = ρ_X⁻¹(y)∩C. **Nerode** : x ∼_N x′ ⟺ 𝔐^adm_x = 𝔐^adm_{x′} et R_x^{ρ_int} = R_{x′}^{ρ_int} (même domaine, mêmes valeurs). Niveau intermédiaire : état → F_y/∼_N → Rep^max(s). |F_y/∼_N|≥2 est nécessaire (non suffisante) à un témoin de H en y.
- **Préordre de simulation** (réserve pour C5) : x ⪯ x′ ssi 𝔐^adm_x ⊆ 𝔐^adm_{x′} et R_{x′}|_{𝔐^adm_x}=R_x.
- Dans le noyau, la contrainte de domaine est automatique (§3.1) : ∼_N se réduit à l'égalité des réponses sur le domaine commun.
- **Équivalence en profondeur finie** : pour un protocole u et une profondeur k, x ≡_k^{(u)} x′ lorsque x et x′ produisent, sous u, le même chemin structurel (suite des mots de recâblage) sur leurs k premiers Kairos. Un chemin qui s'arrête après r<k Kairos n'est égal à un autre préfixe que s'il s'arrête au même endroit avec le même mot (symbole terminal † dans la définition). 𝒫_k^{(u)} = partition de F_y par ≡_k^{(u)} ; 𝒫_{k+1} raffine 𝒫_k.
- **Famille séparante** : 𝒰 est séparante si x≁_N x′ ⇒ ∃u∈𝒰, k<∞ : x ≢_k^{(u)} x′.

### 4.2 Théorèmes acquis (rédigés dans le .tex)

1. **Finitude à profondeur finie.** Si le prochain Kairos de chaque chambre est déterminé par un i* unique, 𝒫_k est finie pour tout k. L'induction exige y=(A,H,V,P) tout entier fixé sur la chambre (pas seulement A) — c'est vrai par indépendance de (H,V,P) vis-à-vis de τ. |𝒫_k|<∞ ∀k ⇏ sup_k|𝒫_k|<∞.
2. **Inclusion** : x∼_N x′ ⇒ x≡_k^{(u)}x′ pour tout u admissible et tout k fini.
3. **Complétude de la profondeur finie pour la famille maximale (γ₁=λ=0, admissibilité constante sur F_y).** x∼_N x′ ⟺ ∀𝓗∈𝔐^adm_x, ∀k<∞, x≡_k^{(𝓗)}x′. Sens ⇐ : non-Zénon (n(T)<∞ Kairos avant T), constance du readout sur une chambre (lemme V5.7), flot déterministe entre Kairos ⇒ ρ_int∘γ égal sur [0,T] pour tout T. **𝔐 est donc séparante.** Cassée dès que τ revient dans (H,V,P) (γ₁≠0 ou λ≠0) : alors des états de même chemin structurel peuvent avoir des ρ_int différents.
4. **Hypothèse correcte de domaine** : non pas « 𝔐^adm_x ne dépend que de π_s(x) » mais « ρ_X(x)=ρ_X(x′) ⇒ 𝔐^adm_x=𝔐^adm_{x′} » (la garde D dépend de P). Vérifiée pour le noyau; à confirmer sur la définition formelle de 𝔐_x du socle pour tout autre exemple (sinon axiome supplémentaire).

La question n'est donc plus l'existence d'une famille séparante mais sa **minimalité**.

### 4.3 Deux lemmes mécaniques généraux

- **Transport de la différence cachée.** Tant que x et x′ suivent le même chemin structurel (même (H,V,P)), Δτ=τ_x−τ_{x′} vérifie Δτ̇=−βΔτ, donc **Δτ(t)=e^{−β(t−t₀)}Δτ(t₀)**, quel que soit le protocole (erreur numérique ~10⁻¹⁵, `nerode_mechanism_check.py`). Le protocole n'agit pas sur l'écart caché mais sur le *fond commun* (A,H,V,P) relativement auquel K* le lit via les cosinus : une direction nouvelle déplace le fond transversalement aux murs, une amplitude seule ne change que l'instant où il est évalué.
- **Obstruction R_y (paire miroir).** Si u_y=0 sur le seul nœud forcé et H(0)=V(0)=0, H_y≡V_y≡0 exactement. Si x′ est le miroir exact de x (φ′=−φ), R_y (isométrie, donc cos(R_ya,R_yb)=cos(a,b)) conjugue les trajectoires de τ et les classements sont identiques à chaque Kairos : **𝒰₅ ne sépare jamais la paire miroir** (N=6, paire A). C'est la seule obstruction analytique prouvée. *Portée exacte* : elle établit qu'il faut **briser** la symétrie R_y pour séparer la paire miroir; une direction de forçage indépendante la brise (c'est ce que fait 𝒰₄), mais ce n'est pas démontré être le seul moyen.
- **Premier franchissement de marge** [PROP, .tex]. Pour deux états ne différant que par le nœud perturbé q≠i*_r, tant que le chemin est commun, τ_j est exactement identique pour tout j≠q ; le seul canal est la position de q dans le classement. Marge signée m_q^{(r)}(x)=sim(τ_{i*},τ_q)−seuil(x) (seuil = m-ième plus grande similarité parmi les autres candidats, commune à x,x′) ; k_min = min{r : m_q^{(r)}(x)·m_q^{(r)}(x′)<0}. Validation (N=9, nœud perturbé φ₇, 800 protocoles, K=7) : accord exact 783/783 ; 17 cas censurés par m_r=0 (Kairos sans concurrence), tous réellement non séparés jusqu'à K=7 ; 0 tie, i*=q jamais rencontré. Cas q=i*_r exclu de l'énoncé (ouvert).

### 4.4 Chaîne de minimalité 𝔐 ⊃ 𝒰₅ ⊃ 𝒰₄ ⊃ 𝒰₃ (noyau, N=6 et N=9)

Familles (forçage constant) : **𝒰₅** mono-axe, un nœud (0), direction fixée (u_y=0), amplitude variable ; **𝒰₄** forçage 2D constant, un nœud (0), amplitude × direction (grille de référence 3 amplitudes × 11 angles = 33 protocoles) ; **𝒰₃** forçage 2D constant, nœud variable (18 protocoles N=6, 12 N=9). 𝒰₂ (variable dans le temps, un nœud) et 𝒰₁ (tous nœuds, variable) non implémentées. Emboîtement des *échantillons* par construction (𝒰̂₅=tranche angle 0 de 𝒰̂₄, 𝒰̂₃=union des 𝒰̂₄(nœud)), contrôlé automatiquement (`check_nesting_and_monotonicity`).

Trois paires de référence : **A** (N=6, miroir exact φ_A′=−φ_A), **B** (N=6, coin (0°,0°), même chambre jusqu'à k=4, séparée à k=6), **C** (N=9, chambre {2,4,6}, scission (2 6) à k=2). Matrice (profondeur minimale séparatrice, moteur corrigé) :

| Paire | 𝒰₅ | 𝒰₄ | 𝒰₃ |
|---|---|---|---|
| A — miroir N=6 | ✗ **prouvé** (R_y) | ✓ k_min=3 (18/33) | ✓ k_min=1 (155/198) |
| B — coin (0,0) N=6 | ✗ observé (k≤12, 40 amplitudes) | ✓ k_min=1 (2/33) | ✓ k_min=1 (2/198) |
| C — {2,4,6} N=9 | ✗ observé (k≤12, 40 amplitudes) | ✓ k_min=2 (2/33) | ✓ k_min=2 (2/132) |

- Monotonie k_min(𝒰₃)≤k_min(𝒰₄)≤k_min(𝒰₅) vérifiée (B et C : égalité, fait sur ces témoins, pas propriété générale). Pour B et C, 𝒰₅ échoue parce que le profil relatif de τ_y entre nœuds est indépendant de l'amplitude; pas de preuve (un autre nœud forcé sous u_y=0 pourrait rompre le découplage; non testé systématiquement).
- **Le saut mono-axe → 2D (même nœud) suffit à séparer tôt dans les trois cas : la richesse décisive est la direction du forçage**, pas l'amplitude ni le nombre de nœuds forcés.
- **Recherche de contre-exemple à 𝒰₄** (4 candidats construits de façon informée, N=6 et N=9, murs de retrait et d'ajout) : tous séparés par 𝒰₄ après stress-test dense (360 protocoles, k=20), via des protocoles absents de la grille de référence. *Faible sensibilité locale (Jacobien) ⇏ défaut global de pouvoir séparant* : le Jacobien est un outil d'interprétation a posteriori, pas un filtre de recherche. **Statut : section non rejouée avec le moteur corrigé** (bug de regroupement, corrigé; effet sur la matrice nul) — si ce résultat doit entrer dans le manuscrit, rejouer `nerode_u4_counterexample_search.py` et `nerode_n9_u4_vs_u3.py`.
- **Ensemble atteignable.** Sur N=9 (A₀ déconnecté en 3 composantes {0,1,2,3},{4,5},{6,7,8} : (H,V) restent exactement nuls hors de la composante forcée, τ y décroît à direction fixe), R₀ = {τ₀(t_K;u)/‖τ₀‖ : u∈𝒰₄}⊂S¹ est **numériquement S¹** au premier Kairos (« 𝒰₄ angulairement complète », artefact de grille levé en densifiant à 1°). En revanche le conjoint R₀^{(1,2)}⊂S¹×S¹ (angles de τ₀ aux Kairos 1 et 2 sous un même protocole) **laisse ≈ 86–88 % du tore inatteint**, trou qui résiste à la densification (2160 puis 4800 protocoles); F₂:(r,φ)↦(θ₁,θ₂) quasi de rang 1 presque partout (médiane |det_rel|=0,027, 79 % <0,05, jamais nulle partout). Obstruction séquentielle réelle mais **pas encore de témoin de Nerode qui l'exploite**.
- **Pas de recette « différence d'angle cachée derrière un trou ».** Une différence d'angle sur un nœud auxiliaire libre fuit dès k=1 (i*=0 au premier Kairos et nb∪nn = tous les autres nœuds : tout nœud est déjà candidat) pour peu que l'amplitude soit suffisante. Les différences durables sont **structurelles** (graphe, à distance du nœud forcé, type paires B/C), ou protégées par une symétrie exacte (type R_y).
- **Dynamique des marges sur la chambre {1,4,5}/{2,4,5}/{2,4,6} de N=9** : la variable causale est la marge de classement g₂, non (θ₁,A₁,θ₂) ni l'amplitude seule (corr(amp,θ₁)=0,59 pour {1,4,5}, s'effondre pour {2,4,5}). Chaîne : u → chemin hybride commun → (m^{(1)},m^{(2)},…) → premier changement de signe → k_min. Sur 800 protocoles : 174/800 séparent avant correction, 170/800 après; la chambre {2,4,6} sépare 2/327 (le « zéro propre » 0/327 d'avant correction ne tenait pas).

**Prochaines étapes (non commencées)** : implémenter 𝒰₂/𝒰₁; élargir l'échantillon de paires; tester systématiquement un autre nœud forcé sous 𝒰₅ pour B/C; protocoles visant la zone angulaire de {1,4,5}/{2,4,5} tout en retombant dans {2,4,6}; chercher la fonction (amplitude, angle) ↦ séparation par régression plutôt que par projection; extraire proprement le lemme de transport et le cas R_y vers le .tex comme pièces du programme des familles séparantes.

---

## 5. Géométrie des partitions 𝒫_k à profondeur finie

### 5.1 Stratification par la symétrie : trois origines d'un mur

Programme : espace des τ → strates 𝒯_H={τ : Stab_Γ(τ)=H}, Γ=Aut(A) *au graphe courant* (suite de types de symétrie le long du mot, non un groupe fixé) → murs transverses → ∼_k → ∼_N. 𝒫_k = 𝒫_k^sym ∨ 𝒫_k^trans. Le groupe sert à *stratifier et expliquer*, jamais à identifier (deux états reliés par automorphisme ne sont pas nécessairement ∼_N-équivalents, à cause du départage).

**Lemme combinatoire (sélection équivariante à cardinal fixé).** X fini, G groupe fini agissant, v:X→ℝ G-invariante, c le m-ième plus petit niveau de v, T={v=c}, a=|{v<c}|. Il existe un S⊆X, G-invariant, réalisant exactement « les m plus petites valeurs de v » **ssi (m−a) est une somme de tailles d'orbites de T**. (Orbite unique de taille t>1 : possible seulement si m−a∈{0,t}.) [PROP, .tex : « Obstruction orbitale à une sélection équivariante »]. Conséquences :
- **Le lemme établit une incompatibilité, non l'unicité du remède** : déterminisme (H1–H4), Γ-équivariance et cardinal exact (fixé ou borné) ne peuvent être exigés ensemble sur le lieu de tie; **au moins une des trois exigences doit être abandonnée**. Le départage par indice (qui abandonne l'équivariance) est une solution, pas la seule logiquement possible (écarté dans la classe : m_max variable, qui déplace l'obstruction du contenu vers le cardinal; relâcher le déterminisme sortirait de H1–H4). Même obstacle pour le départage « plus petit indice » entre Kairos simultanés (cas m=1, a=0). K* n'a pas de préférence pour l'asymétrie : l'ensemble des règles déterministes, équivariantes et à cardinal exact est *vide* sur le lieu de tie; le départage comble ce vide par convention (posture C4).
- **Invariance des lieux fixes sous le flot** [PROP, .tex] : le flot du noyau est Γ-équivariant tant que le graphe l'est (vérifié sur l'état complet (H,V,τ,P), pas seulement sur K*).
- Suivi (Aut(A_k), G_k=Stab_{Aut(A_k)}(τ_k)) : **Aut(A_k) n'est pas monotone** (N=6 : oscille 2,1,2,1,… avec A_k de période 2), la bonne variable est G_k. Statut supplémentaire : symétrie **réapparue mais inerte** (Aut(A_k) non trivial, G_k trivial). Sous forçage fixe la rupture de symétrie à la première obstruction (k=0) est définitive; une seconde obstruction n'est obtenue que par réinjection délibérée d'une composante symétrique (`reinjection.py`), qui reproduit exactement la première (A₂=A₀).
- Témoin N=9 (`orbit_diversity.py`) : nb(0)={1,2,3} jumeaux, nn(0)={4,5}∪{6,7,8}, |Aut(A₀)|=72. Côté retrait : égalité exacte sim=0,557832, t=3, a=0, m=2 ⇒ aucune sélection équivariante (retire {1,2}, garde 3). Côté ajout : {4,5} à égalité au sommet (0,997785) devant 6,7,8 (0,447214), m−a=t=2 ⇒ sélection équivariante, {4,5} ajouté en bloc. Après le saut |Aut|=240 : {1,2} isolés fusionnent avec l'orbite {6,7,8} (S₃×Z₂×S₃ → Z₂×S₅).

**Taxonomie des murs** (tableau de diagnostic, N=6) :

| mur | origine | sous forçage générique 2D |
|---|---|---|
| φ₁=φ₂ (étape 1, τ libre) | coïncidence de score (Fix(σ) ⊊ {c_i=c_j}) | sans objet |
| φ₄=φ₅ dans « gardé=3 » | **structurel** Fix(σ), σ=(1 2)(4 5)∈Aut(A₁) | survit à l'identique ; |c₄−c₅|≤10⁻¹⁹ sur la diagonale |
| φ₄=−φ₅ dans « gardé=3 » | **induit par le protocole** (parité R_y d'un forçage mono-axe) | disparaît |
| bandes {4,5} dans « gardé=1 » (Aut(A₁)=1) | **transverse générique** | survit, déformée |

Règle de méthode : avant de qualifier un mur de « transverse », vérifier que le protocole de sonde n'introduit pas lui-même une symétrie (forçage ≥2 directions non colinéaires). Aucune égalité de scores ne révèle seule la nature d'un mur : il faut remonter à τ. Généalogie à deux axes : (mur déjà pertinent avant K* / mur activé par un nouvel ensemble de candidats) × (porté par une symétrie / transverse).

### 5.2 Croissance de 𝒫_k : N=6 et N=9

- **N=6, fenêtre (φ₄,φ₅), chambre « gardé=1 »** (Aut(A₁)=1, forçage 2D 37°) : grille 32×32 : 3→3→5→5 chambres (k=2…5). **Artefact de sous-résolution** : le zoom local sur le coin (0°,0°) révèle 9 chemins distincts à k=4 (motif en croix) ; tout compte de 𝒫_k doit préciser la résolution. Même courbe depuis « gardé=3 » (Aut(A₁)=4) avec une scission structurelle dès k=2 : ni la présence ni l'absence de symétrie ne pilote seule le rythme. Raffinement adaptatif sur le tore (16×16, 60/256 cellules raffinées) : la sous-structure est le long de toute la frontière, plus riche près des coins (5–9 étiquettes).
- **Réinjection combinatoire N=6** : à toutes les profondeurs de scission (k=2,4,6) la compétition est exactement entre {1,4},{1,5},{4,5} (partage à trois issues {1,2,3}/{2,3,4}/{2,3,5}), toutes transverses; le graphe revient à nb(0)={1,4,5} aux étapes impaires. Chemins : 3 (k=2), 9=3² (k=4), 26≈27=3³ (k=6, un manquant par effet de bord de fenêtre). **Arbre ternaire conditionnel à la dominance de τ₁ parmi {1,4,5}** (vérifiée numériquement branche par branche, non démontrée uniformément) : |𝒫_{2n}^{loc}|=3^n pour k=2n. Croissance non bornée mais **entièrement structurée** (pas d'explosion globale) ; formulation retenue : *la complexité observée n'est pas bornée, elle est structurée*.
- **N=9 (nb(0)={1,2,3}, |Aut(A₀)|=72)** : structurel et transverse coexistent dès la profondeur 1 (chambres {1,4,5} 79,4 %, {2,4,5} 12,2 %, {1,4,6} 7,2 %, {2,4,6} 1,1 %; scissions {1,2}-échange = structurelles). Diagnostics Aut(A₁) : {1,4,5} et {2,4,5} isomorphes (|Aut|=240), {1,4,6} et {2,4,6} aussi (48). À résolution égale (3600 points conditionnés par chambre) : |𝒫_k^loc| k=1…5 : {1,4,5} : 1,1,1,1,1 ; {2,4,5} et {1,4,6} : 1,2,2,3,3 ; {2,4,6} : 1,3,3,6,6 (puis 10, 11 à k=6,7). **La chambre la plus massive est localement la plus pauvre**, la plus marginale la plus riche ; |Aut(A₁)| n'est pas un prédicteur scalaire. La différence {1,4,5}/{2,4,5} du premier essai était un artefact de contexte τ (contrôle d'équivariance par σ=(1 2)). **Réinjection structurelle spontanée** : la scission {1,3,6}↔{1,2,3} est portée par la transposition (2 6) (4 témoins équivalents) à k=2,4,6, et se réactive à chaque retour au voisinage {2,4,6}, d'où qu'on vienne ; confirmé à un second centre (334°,18°). Contraste N=6 (réinjection combinatoire locale d'un même problème de classement) / N=9 (réinjection structurelle d'une même symétrie).
- Pas d'occurrence d'une scission structurelle portée par une autre symétrie que (2 6) jusqu'à k=7; profondeurs 8–10 non faites.

### 5.3 Du comptage de chambres aux surfaces de marge

- **Lemme d'analyticité par morceaux** [PROP, .tex, hypothèses de régularité] : à chambre fixée (i*_r et candidats constants), l'application état-initial → état-pré-Kairos-de-rang-r est réel-analytique sous (i) transversalité du contact de Kairos (Ṗ_{i*}(t*)≠0) et (ii) non-nullité des vecteurs intervenant dans les cosinus. Scores c_j^{(r)}=cos(τ_{i*},τ_j) analytiques, marges analytiques par morceaux; ∂𝒫_r ⊆ ∂𝒫_{r−1} ∪ ⋃_{i≠j}{c_i^{(r)}=c_j^{(r)}} ∪ 𝒟_r, avec 𝒟_r = contacts tangents ∪ Kairos simultanés ∪ vecteurs nuls. Seules les égalités à cheval sur le seuil de sélection (rang m vs m+1) sont des murs actifs. « Structurel » = forcé par le stabilisateur de l'état *et* du protocole.
- **Test de contour actif** (`contour_active_walls.py`, N=6, chambre {1,4,5}, fenêtre site2_bas 140×140) : prédiction « survivant = argmax(c₁,c₄,c₅) » accord pixel-à-pixel **19600/19600**. **Doigt à 219°** : c₁^{(4)}=0,995746 constant, c₄ a un maximum lisse =1 en φ₄=219,000°, c₁−c₄ change deux fois de signe (218,56° et 219,46°) sans aucune dégénérescence : *un couple de scores ⇏ un seul mur*. Cas structurel (`contour_active_walls_fixsigma.py`, chambre « gardé=3 », τ₁=τ₂) : accord 25440/25600; les 160 désaccords sont exactement la diagonale (tie, convention de tri stable); g₄₅^{(2)}≡0 sur Fix(σ) (max|c₄−c₅|=1,08×10⁻¹⁹).
- **Trois sources de croissance de 𝒫_k** : diversification (nouvelles paires actives), fragmentation (une paire, plusieurs composantes), entrelacement (intersections : point triple (φ₄,φ₅)≈(219°,357,5°), régulier, ni mur transverse simple ni 𝒟_r). Compteurs N_pair(r), N_comp(r), N_int(r). 𝒟_r reste sans témoin numérique (codimension supérieure; à garder comme frontière de validité).
- **Taxonomie des paires** (`growth_counting_v2.py`) : N_cand ⊃ (dépend réellement de q) ⊃ (atteint effectivement 0) ⊃ N_wall ⊃ N_comp. Sur la fenêtre N=6 : r=4,5,6,7 : N_wall = 4,0,4,0 (alternance); N_cand = 5,5,10,9 ; paires gelées 0,2,0,6.

### 5.4 Invariants exacts du noyau (lemmes)

1. **Conservation du support de dépendance cachée** [PROP, .tex]. Soit Dep(Σ) l'ensemble des nœuds dont la trace initiale dépend du paramètre ϑ. Dans une classe de mot, (A,H,V,P) est fermé et indépendant de ϑ, donc Δ_ϑτ_i(t)=e^{−βt}Δ_ϑτ_i(0) et i∉Dep(Σ) ⇒ τ_i(t;ϑ) constante sur toute réalisation du mot, à tout instant et tout Kairos (K* ne modifie jamais τ). Le support ne peut pas s'étendre : sur N=6 le bloc ϑ-dépendant {4,5} est le même pour toute la lignée; τ₀,τ₁,τ₂,τ₃ sont constants bit à bit sur la fenêtre. (Seul le sens ⇒ est affirmé; la réciproque exige une réalisation d'intérieur relatif non vide et Ω connexe.)
2. **Borne locale de mobilité** : pour i*_r∉Dep et J_r de cardinal n_r avec ν_r=|J_r∩Dep|, le nombre de paires potentiellement mobiles est ≤ ν_r n_r − ν_r(ν_r+1)/2 = O(n_r) (au plus linéaire, non O(n_r²)) ; si i*_r∈Dep la borne ne découle plus directement.
3. **Forme affine** [PROP, .tex] : dans la classe de mot w, τ_i^{(r)}(ϑ)=b_{i,w}^{(r)}+λ_{r,w}τ_i^0(ϑ), λ_{r,w}=e^{−βt_{r,w}}, b_{i,w}^{(r)} et les temps de Kairos ne dépendant que de w (et de y), pas de la composante. Vérifiée à la précision machine (résidus 1,94×10⁻¹⁶ et 1,55×10⁻¹⁵).
4. **Alternance 4,0,4,0** (N=6) : aux rangs pairs la réinjection ramène nb(0)={1,4,5}, les deux nœuds Dep ensemble dans la contestation (n=3>m=2) ⇒ murs ; aux rangs impairs, soit Dep absent de nb, soit un seul isolé qui domine *prouvablement* : inf(c_isolé) sur l'intervalle réel de la chambre dépasse le sup des concurrents (marges +0,004269 pour nb={2,3,4}, +0,018122 pour nb={2,3,5} ; valeurs extrêmes aux bornes 0,9855068273/0,9873623246 et 0,9992524311/0,9999322934 via c′(φ)∝−a(y+a sin φ)(a+x cos φ+y sin φ) : au plus 4 points critiques, aucun dans l'intervalle). La complexité vient de la combinatoire des chambres, du changement des constantes (b_x,b_y,λ) et de la réactivation périodique des statistiques d'ordre — pas d'une complexification analytique locale en r.

### 5.5 Borne de croissance du nombre de chambres, ties inclus

- **Lemme du vecteur de signes** [PROP, .tex `lem:signes-determinent-kstar`]. Avec τ_⋆:=τ_{i*}^{(r)}, a_i=⟨τ_⋆,τ_i⟩, s_i=‖τ_i‖², χ_ij=a_i²s_j−a_j²s_i (degré en z∈S¹ : ≤4 si i*_r∉Dep, ≤6 si i*_r∈Dep ; uniformément ≤6, indépendant de r) : pour a_i,a_j>0, signe(c_i−c_j)=signe(χ_ij) ; pour a_i,a_j<0, opposé ; signes différents ou nuls ⇒ immédiat; s_⋆=0 ou s_i=0 ⇒ score 0 (convention Tome I). Avec le départage par indice, le mot réalisé est une fonction du vecteur de signes de la famille 𝒫_w={a_i^{(r)},s_i^{(r)},χ_ij^{(r)},‖τ_⋆^{(r)}‖²}_{r≤k} (O(N²k) polynômes de degré ≤6).
- **Partition exacte** : Ω=⊔_wΩ_w, Ω_w=⋃_{σ∈S_w}Réali(σ,𝒫_w)∩Ω (réunion de cellules de signes; ties, traces nulles, cascades codées dans le mot, mots tronqués †). Aucun lieu exclu.
- **Borne** [PROP, `prop:complexite-mot-fixe`, `cor:borne-croissance-ties`] : b₀(Ω_w) ≤ B_sa k^p (**Barone–Basu, Thm 1.1**, Discrete Comput. Geom. 47 (2012) 577–597, DOI 10.1007/s00454-011-9391-3 — référence et énoncé vérifiés par Benoit sur le PDF ; application : ambiant Zer(Q,ℝ^{2p}) avec Q={x_ℓ²+y_ℓ²−1}, d₀=2, k=2p, k′=p, polynômes de 𝒫_w de degré ≤d=6 (donc 2d₀≤d), d'où (sd)^{k′}d₀^{k−k′}O(1)^k=(sd)^p O(1) avec s≤B_N k+O(1) : O(k^p) ; remplace le BPR–Milnor–Thom brut parce que le théorème distingue d₀ (variété) de d (famille) ; BPR chap. 7 pour les outils généraux) et **|𝒫_k^conn| ≤ B_conn k^p L^k** (L = nombre d'issues de K* par Kairos). Conséquence non écrite : |𝒫_k| ≤ |𝒫_k^reg| ≤ la même borne. Complexité locale polynomiale × prolifération combinatoire des mots. Ne donne pas l'uniformité de la borne en k au sens d'un contrôle de la tameness.

### 5.6 Variation du présent observable y : trois mécanismes de bifurcation

Décomposition (la fibration est triviale : C≃Y_adm×T pour le noyau, la famille de partitions de T indexée par y varie) :

| mécanisme | niveau | effet |
|---|---|---|
| **événementiel** : contact tangent, Kairos simultanés, P franchissant Θ | mot / lecture, ϑ-indépendant (strates de l'espace des y) | modifie le chemin |
| **classement régulier** : c_i=c_j, tangence de deux murs (discriminant de 𝒫_w), mur sortant de Ω | ϑ | naissance/fusion de chambres (pli : largeurs en √) |
| **trace nulle** : τ_j=0 | ϑ | discontinuité du score (±c₀ → 0 → ∓c₀); effondrement **linéaire** |

La règle s(i,j)=0 fixe la valeur en τ_j=0 mais les limites directionnelles du cosinus peuvent être opposées : système déterministe, fonction de décision discontinue; le comptage semi-algébrique n'est pas affecté, le théorème de déformation analytique des murs ne traverse pas ce lieu.

**Forme normale conique** [PROP, .tex `prop:annulation-conique`]. Sur le mot w, τ_j^{(r)}(φ,μ)=b(μ)+R(μ)e(φ) (arc de cercle de centre b, rayon R). Trace nulle ⟺ Δ(μ*)=‖b‖²−R²=0 avec φ*=arg(−b(μ*)). Si Δ′(μ*)=2det[∂_φΨ,∂_μΨ]≠0 (annulation transverse; φ* intérieur à Ω_w; Ψ difféo local), alors {c_j>seuil} est, près du point critique, un **secteur** de sommet (φ*,μ*) (angle ±arccos c_seuil autour de τ̂_⋆) et la largeur d'une coupe μ=const vaut L(μ)=υ_cone|μ−μ*|+o(|μ−μ*|), υ_cone=|m(θ₊*)/ℓ₊−m(θ₋*)/ℓ₋|. Preuve en coordonnées polaires du plan image (pas d'IFT à l'origine : l'angle est homogène de degré 0, non C¹ en T=0); hypothèse : ℓ(θ_±)≠0 de même signe, τ_⋆ de classe C¹ (à ajouter dans l'énoncé).

**Expérience (N=6, k=4).** On déplace de η (écrit μ dans le .tex) la composante 0 de la position initiale du nœud 0 (H(0)), même coupe φ₅=349°, φ₄∈[200°,228°], même protocole. Le mot (0,{1,2,3}),(0,{1,4,5}) est retrouvé pour tout η∈[−0,3 ; 0,3] (pas de bifurcation de mot aux rangs 1–3). Le doigt à 219° (bords 218,564°/219,461° à η=0) s'effondre sur le mur de trace nulle : τ₁,τ₀,τ₅ ne dépendent pas de φ₄ (c₁≈0,996), τ₄(φ₄) passe très près de l'origine (‖τ₄‖_min=0,0177 à η=0), c₄ balaie un demi-tour d'angle sur un intervalle étroit.

Résultats **corrigés** (Kairos résolu par interpolation de l'instant exact P_{i*}=Θ, `iws_kairos_interp.py` ; sans interpolation le pas de temps entre en b et λ comme un escalier discontinu en y) : forme affine : résidu 4×10⁻¹⁶ sur 27 angles, M=aI à 10⁻¹³, λ=0,7438, a=0,2231 (ρ=0,3) ; **μ*=η*=−0,161819** (Brent; stable en dt : −0,161819 à dt=2×10⁻³ et 10⁻³, −0,161818 à 5×10⁻⁴) ; Δ(−0,160)=+9,6×10⁻⁵, Δ(−0,165)=−1,7×10⁻⁴ ; ‖b‖=R=0,223049 à la racine ; **Δ′(η*)=+5,275×10⁻²** (=2×0,0264); **φ*=221,7497°**, simulation directe en (φ*,η*) : mot de référence et ‖τ₄‖=5×10⁻¹⁴; intérieur : tout [219° ; 225,5°] réalise le mot (marges 2,75° et 3,75°), mot conservé en (φ₄*,φ₅) pour φ₅∈[347°;350°], perdu à 351° (les trois autres angles φ₁,φ₂,φ₃ fixés); transversalité : u=∂_ητ₄=(0,1552 ; 0,0037), v=∂_φτ₄=(0,1485 ; −0,1664), det[v,u]=2,64×10⁻² (sin∠=0,76); secteur : θ_c=arccos c₁=5,511°, **K=6,347° par unité de η (≈0,1108 rad)**; largeur/(η−η*) = 6,25 ; 6,30 ; 6,32 ; 6,33 ; 6,32 pour η−η*=2×10⁻⁴ ; 5×10⁻⁴ ; 10⁻³ ; 2×10⁻³ ; 5×10⁻³, puis plateau (6,33→5,80 jusqu'à η=−0,05), à 0,3 % de K près. Largeurs du doigt à instant exact : 0,648 ; 0,374 ; 0,257 ; 0,136 ; 0,074 ; 0,0115° pour η=−0,05 ; −0,10 ; −0,12 ; −0,14 ; −0,15 ; −0,16. Le doigt n'existe que du côté Δ>0 (origine hors du cercle); pour Δ<0 le balayage passe par −e₀ et le doigt est remplacé par une zone g₁₄≫0 (c₄ atteint −1 au lieu de +1). L'effondrement est **linéaire en d=min‖τ₄‖**, non une fusion de deux racines (qui serait en racine carrée). Contrôles : même diagnostic (passage de côté entre η=−0,15 et −0,3, non localisé finement) en variant la composante 1 de H(0) du nœud 0 et la composante 0 du nœud 3; compatibles avec la même loi; pour η>0 la fenêtre fine ne contient plus tout le doigt : non concluant de ce côté.

**Statut** : un témoin vérifié (une coupe, un sens de variation, un jeu d'angles fixes) ; forme normale locale et loi linéaire confirmées sur ce témoin; **aucune conclusion sur l'uniformité en k**.

### 5.7 Définissabilité locale (remarque `rem:definissabilite-locale`, v5.15)

L'énoncé « tout est définissable dans R_an » est **trop fort**. Hypothèses nécessaires : protocole analytique ou analytique par morceaux (L^∞ ne suffit pas); compact K de lectures sur lequel les k premiers Kairos sont atteints avant un temps uniformément borné; événements transverses; prolongements analytiques des temps d'impact. Énoncé retenu : *la famille des partitions est définissablement triviale sur un domaine compact régulier*, k fixé (o-minimalité produite, Hardt applicable), **sans uniformité en k ni fibration stratifiée globale**. Le produit C≃Y_adm×T (Y_adm:=ρ_X(C)) est propre au noyau, non au socle. L'application y↦(b_{i,w}^{(r)},λ_{r,w}) est analytique non algébrique (intégrales du flot); les bifurcations en ϑ sont l'image réciproque d'un discriminant semi-algébrique.

### 5.8 Programme de soustraction : de γ₁=λ=0 à une condition intrinsèque (programme de travail, octobre 2026)

*Statut : **programme de travail**. Les résultats acquis sont ceux des §3–5.7; ce qui suit sépare explicitement (i) ce qui est acquis, (ii) l'énoncé **candidat** [CONJ] et (iii) les **témoins** numériques recueillis pour le tester. Rien ici n'est une proposition démontrée.*

**Deux minimalités.** *Descriptive* : plus petite famille de protocoles séparante dans le noyau (chaîne 𝔐⊃𝒰₅⊃𝒰₄⊃𝒰₃, §4.4). *Logique* : plus faibles hypothèses sur le noyau sous lesquelles les résultats subsistent. La seconde est la **soustraction** : remplacer l'hypothèse γ₁=λ=0 par une condition **intrinsèque** plus faible, sans la poser comme hypothèse tautologique. Cible de formulation : *« à mot fixé, les scores appartiennent à une famille définissable de complexité uniformément contrôlée »* — à n'adopter qu'**en conclusion** d'un mécanisme, jamais comme hypothèse (une uniformité postulée est tautologique).

**Autonomie conditionnelle du visible** (correction de Benoit; remplace « le mot et les temps sont fonctions de y seul », faux). Au mot structurel w *fixé*, l'application (y,u,w) ↦ (H_w,V_w,P_w,t*_{1,w},…,t*_{k,w}) est **indépendante de ϑ**. En revanche (y,ϑ,u) ↦ w **peut dépendre de ϑ** : c'est le mécanisme même d'historicité (le caché choisit le mot). Le découplage γ₁=λ=0 fournit ainsi deux choses distinctes : (1) l'autonomie conditionnelle du visible, (2) l'affinité du caché (τ linéaire en τ avec forçage indépendant de ϑ à chemin fixé ⇒ τ=b_w+Λ_w τ⁰(ϑ)).

**Tableau des dépendances par niveau** (ce qui est utilisé, à quel niveau).

| Niveau | Résultats | Hypothèses réellement utilisées |
|---|---|---|
| Socle hybride | admissibilité, flèches, déterminisme et non-Zénon | structure hybride (§2) |
| Classe IWS | C0–C4, historicité effective, ∼_N | présentation 𝐒, readout, répertoire |
| Classe à N fixé | mots finis à profondeur finie, finitude de 𝒫_k | N fixé, sémantique d'événements déterministe, issues finies |
| Noyau témoin | historicité effective, identifiabilité (actuation, amplitude) | équations du noyau |
| Noyau découplé | complétude de ∼_N; forme affine | autonomie conditionnelle du visible + dynamique cachée linéaire (γ₁=λ=0) |
| Noyau découplé paramétré | borne B k^p L^k | affinité, paramétrisation algébrique, scores cosinus, N fixé |
| Famille analytique régulière | définissabilité locale (§5.7) | régularité analytique, prolongements sur compacts, contrôle des événements |

**Trois propriétés à ne pas confondre** (hiérarchie raffinée).
- **A — modération à profondeur finie** : analyticité sur compacts à l'intérieur des domaines de continuation + contrôle des événements (R_an); *pas* sur des domaines arbitraires atteignant des singularités.
- **B — complexité uniforme à mot fixé** : exige une classe de fonctions **stable par l'évolution hybride** (l'affine est la réponse du régime découplé); chercher des mécanismes qui préservent une classe (p. ex. dépendance rationnelle), ne **pas** supposer l'uniformité.
- **C — borne combinatoire L^k** : N fixé, sémantique d'événements déterministe, issues finies; **n'exige ni affinité ni analyticité**.

**Énoncé candidat — stabilité perturbative à mot fixé, du noyau découplé vers le noyau faiblement couplé.** *(Mise à jour : preuve rédigée dans `stabilite_perturbative_mot_fixe.tex`, voir « Théorèmes » ci-dessous; reste [PROP à relire], non acquis tant qu'il n'a pas été relu.)* Soit ε=|γ₁|+|λ|. Fixons un mot w, une profondeur k, un compact K de paramètres cachés, un horizon borné, un chemin stable, des marges de classement strictes uniformes, des contacts de garde transverses et une dépendance lisse en ε. Alors
 sup_{ϑ∈K} ‖τ_{ε,w}^{(k)}(ϑ) − [b_{k,w}^{(0)} + Λ_{k,w}^{(0)} τ⁰(ϑ)]‖ ≤ C_{K,k} ε.
Esquisse d'argument visée : dépendance continue + Grönwall sur chaque épisode, théorème des fonctions implicites sur les temps d'impact. **Réserves** : (i) C_{K,k} dépend de k (rien ne dit en quel sens); (ii) l'énoncé tombe si un changement de classement modifie le mot ou près d'une dégénérescence d'événement; (iii) O(ε) ne borne pas les nombres de murs (la topologie peut changer près d'une tangence); (iv) γ₁‖τ‖ n'est pas différentiable en τ=0 (interaction avec les murs de trace nulle). Trois issues à distinguer : **(1)** la forme affine est perdue mais la perturbation est contrôlée à profondeur fixée; **(2)** la perturbation s'amplifie avec la profondeur sans détruire la définissabilité à profondeur finie; **(3)** une hypothèse d'événement casse et le mot change.

**Théorèmes — `stabilite_perturbative_mot_fixe.tex`, version 2c (9 p.), après trois relectures de Benoit.** Statut : **Th. 1 : trois ajustements finaux intégrés (A_r défini pour r≤k−1; phrase sur la référence en [T,t_r⁰[; min∅=+∞); Benoit : « ne plus toucher au théorème 1 » — travail désormais sur P2** ; Th. 2 **conditionnel** à l'hypothèse P2 reformulée.
- *Cadre.* (γ₁,λ)=ε(γ̄,λ̄); compact K de ϑ=τ(0); **mot de profondeur k = k−1 recâblages + k-ième impact pré-saut**; hypothèses : chambre (mot w réalisé à ε=0), transversalité ν=min dP̃⁰_r/dt(t_r⁰)>0 (dérivée du prolongement pré-impact), séparation σ>0, écart g>0 (ces trois indépendantes de ϑ par l'autonomie conditionnelle du visible), traces non nulles aux Kairos ν_τ>0, marges de **frontière** de sélection μ>0 (seul le m-ième/(m+1)-ième classement compte). Protocole u∈L^∞ seulement.
- *Th. 1 (ordre un).* Il existe ε₀, C_r tels que, pour ε<ε₀ et ϑ∈K : même mot, |T_r^ε−t_r⁰|≤D_rε (D_r=4F_r/ν), ‖τ_ε^{(r)}(ϑ)−[b_{r,w}+e^{−βt_r⁰}ϑ]‖≤C_rε. **Preuve v2** : on ne compare plus les trajectoires hybrides à travers le saut (faute de la v1 : Ṗ⁰≥ν/2 sur une fenêtre centrée en t_r⁰, alors que P_{i_r} est réinitialisé). On compare les **prolongements virtuels pré-impact** z̃_r^ε, z̃_r^0 (vraies solutions d'EDO sur le même graphe A_{r−1}, sans appliquer le r-ième saut) : Lemme G sur toute la fenêtre, F_r=e^{Lℓ_r}(E_{r−1}+Bℓ_r), franchissement monotone de φ=P̃^ε−Θ avec φ̇≥ν/4 sur toute la fenêtre, unicité du premier franchissement (zone calme + séparation), stabilité du classement (cosinus 1-lipschitzien sur vecteurs unitaires, κ=8C_r/ν_τ, besoin 2κε<μ), puis transport après saut (J 1-lipschitzien, décalage Φ̄|T−t⁰|) et Lemme G sur [S,a_r]. **Rang k à part** (étape 3) : récurrence complète avec synchronisation post-saut seulement pour 1≤r≤k−1 ; au rang k, uniquement franchissement + comparaison pré-impact, ni E_k, ni marge de classement au rang k. **r_P∈]0,1[ strictement** (r_P=1 : le déclencheur reste à P=Θ et redéclenche aussitôt), ρ≤δ_post/(4Ṗ_max) avec δ_post=min((1−r_P)Θ,σ), plus deux seuils sur ε ((F_r+Ṗ_maxD_r)ε<δ_post/2, E_rε<¾δ_post) pour l'absence de nouveau Kairos avant a_r. Constantes de Lipschitz notées K_P et χ_r (κ réservé aux paramètres de pression du Vol. I). Récurrence E_r≤A_rE_{r−1}+B′_r (1≤r≤k−1) avec A_r=e^{2Lρ+Lℓ_r}(1+8Φ̄/ν) : **ne dépend de r que par la longueur ℓ_r de l'épisode** (plus de e^{LT}); constantes exponentielles en r, borne grossière. **Distinction à retenir : C_r (amplification de l'erreur à mot conservé) ≠ ε₀(k) (rayon de conservation du mot)** — σ_r (1,21→0,12) illustre le second. Une borne polynomiale demande la sensibilité de l'évolution **hybride** complète (produits S_rDφ_r…S_1Dφ_1, décalages d'impact et sauts inclus), pas seulement la dissipation continue. Les bornes a priori (R, L) dépendent de l'horizon : l'uniformité en T n'est pas acquise.
- *Th. 2 (défaut d'affinité), conditionnel.* Sous u∈C¹, traces non nulles sur tout l'horizon et **P2 reformulée** : régularité C² en (t,ϑ), dérivées C¹ en ε, du **prolongement pré-impact P̃_r** (pas de la composante hybride P, discontinue à sa réinitialisation) ⇒ IFT légitime sur P̃_r, puis ‖D²_ϑτ_ε^{(r)}‖≤M_rε, ‖D_ϑτ_ε^{(r)}−e^{−βt_r⁰}I‖≤M′_rε, reste de Taylor ≤½M_rεδ² sur B(ϑ₀,δ) (D²τ₀=0). **C² n'est pas automatique après intégration d'une norme** : J(h)=∫√(t²+h²)dt ~ h²log(1/|h|) ; si ‖V_{i_r}‖ ou ‖H_{i_r}‖ s'annulait à un instant intérieur pour un ϑ de la boule, on aurait εδ²log(1/δ). Proposition de conditions suffisantes **seulement esquissée** : nœud i_r forcé avec u_{i_r}(0)≠0, H(0)=V(0)=0, factorisation V=s·v, H=s²h en s=0, (N2) non-annulation de ‖H‖/s², ‖V‖/s sur la trajectoire visible de référence (unique, ϑ-indépendante à ε=0), traitement par morceaux des réinitialisations.
- *Nécessité de la marge* (argument local sous régularité, non un théorème de non-existence): le mur de sélection se déplace de ≃ε|h|/‖∇g₀‖ ⇒ pas d'ε₀ uniforme sur un compact touchant le mur.

**P2 : transmission à travers un Kairos isolé et cas du nœud forcé — `regularite_P2_transmission.tex` (v6, 11 p.) et `lemme_singularite_log.tex` (5 p.), statut : preuve rédigée et corrigée après relecture de Benoit ; le lemme V (estimation O(ε) des variations) n'est PAS encore tenu pour démontré — à relire.** *v4 (deux justifications locales demandées par Benoit)* : (A) lemme `lem:coef` : max_{0≤q≤2}‖D_τ^q(M_{ελ̄}−I)‖≤Cε sur tout compact de traces, et même propriété pour la friction εγ̄‖τ_j‖ avec constante en 1/dist(τ,0) (hyp. h:tn); conséquence calculable des formules du noyau, pas une hypothèse nouvelle; (B) domaine des prolongements virtuels : la non-annulation sur la trajectoire *exécutée* n'assure rien sur un prolongement arbitrairement long; à chaque Kairos j≤r les normes sont non nulles juste avant l'impact, d'où par continuité du flot pré-impact un ρ_j>0; ρ=min(ρ_{Th.1}, min_{j≤r}ρ_j)>0 choisi **conjointement** avec les fenêtres du Th. 1 (même ρ); les flots étendus restent dans 𝒟. *Réserve de minimalité (Benoit)* : les conditions de non-annulation sont suffisantes, pas démontrées nécessaires. *Corrections v2→v3 :* (1) saltation d'ordre un : double comptage de ĝ⁻D_xT supprimé — formule correcte X_{j+1}=D_ξΦ[R_jX^{fix}_j+(R_jĝ⁻−ĝ⁺)D_xT_j]=D_ξΦ[R_jX^{tot}_j−ĝ⁺D_xT_j] (ne pas mélanger dérivée à temps fixé et dérivée totale); (2) premier épisode construit **sans flot étendu depuis t=0** (sous-système (H,V,τ) régulier + Duhamel pour les pressions; flot étendu seulement après T₁>0), ce qui supprime aussi la circularité lemme de démarrage ↔ lemme V; (3) second ordre explicité en cinq termes (E₁–E₅), le terme Φ_ξξ[Dy,Dy] (Dy_τ=O(1)) justifié par la structure des blocs du flot (lemme W : blocs à deux directions τ nuls à ε=0, O(ε) par équations aux variations); (4) formule de Leibniz : f=ψ_i (production); le saut de P_i (−κ₃(1−r_P)P_i⁻, P⁺=r_PP⁻) est traité par le flot étendu. Deux difficultés séparées. *(A) Transmission* : si les prolongements d'épisode sont C² (flot d'un champ C¹ en t, C^∞ en (ζ,ε) hors traces nulles et hors normes nulles) et l'impact transverse, alors P̃_j, T_j, ζ_j^± sont C² en ϑ par récurrence (la réinitialisation V←r_V V, P←r_P P est **linéaire** : ‖V⁺‖=r_V‖V⁻‖, aucune singularité de norme); les termes de bord de la formule de Leibniz (Benoit) sont la traduction en intégrales des matrices de saltation (R_jĝ⁻−ĝ⁺)·T_x. *(B) Zéros des normes* : traité pour le seul nœud **forcé au repos** (u_i(0)≠0, H=V=0 en 0) par la factorisation V=s·v, H=s²·h (v(0)=u_i(0), h(0)=u_i(0)/2, indépendants de (ϑ,ε)) ; u∈C¹ suffit (∂_s‖V‖ continue en 0). **Point nouveau** : (N_HV) (non-annulation de ‖H_i‖/s², ‖V_i‖/s) est une condition sur **une seule trajectoire** (le visible de référence est ϑ-indépendant à ε=0) : un zéro de V_i dans la boule ne peut apparaître que si min‖V_i⁰‖=O(ε) ; la question de la taille δ de boule ne se pose que pour les traces τ (Γ=γ₀+εγ̄‖τ‖), pas pour les normes de H,V. **Reformulation du Th. 2** : on abandonne « C¹ en ε des dérivées d'ordre 2 » (qui exigerait des dérivées troisièmes en temps, donc u∈C²) au profit de C² en ϑ à ε fixé **plus** l'estimation directe O(ε) des variations d'ordre 1 et 2 par Grönwall (clé : le bloc ∂_τ G_w est O(ε), ∂²_wψ[X_w,X_w]=O(ε²/min‖V_i‖)). Conclusion inchangée : ‖D²_ϑτ_ε^{(r)}‖≤M_rε, reste de Taylor ½M_rεδ². **Nœuds non forcés : ouvert.** Acquis : à ε=0 les ordres d'annulation sont ϑ-indépendants (autonomie du visible). Manque : (a) u∈C^{m_j} pour factoriser s^{m_j}, (b) annulations accidentelles des coefficients dominants (graphes symétriques, jumeaux) pouvant rendre l'ordre ε-dépendant. *Témoin* (`verif_temps_impact_C2.py`) : T_r(ϑ) est constant à ε=0 (autonomie conditionnelle); Q_T/ε constant à 4 chiffres en δ∈[5·10⁻⁴;4·10⁻³], rangs 1 à 7, linéaire en ε à ≈3 % (λ seul : 0,96→0,81 du rang 1 au rang 7). Un écart de 30 % au rang 1 (γ₁, ε=0,1, δ=4·10⁻³) est un **artefact de pas de temps** (écart ÷2 quand dt ÷2 : 0,96, 0,50, 0,25·10⁻²), non une proximité de trace nulle (min‖τ_j‖=0,176 sur l'épisode 1).

**Test discriminant d'une annulation intérieure de V₀ (octobre 2026; `verif_zero_interieur_V0.py`, `verif_zero_pente_log.py`, `zero_V0_lib.py`, sorties `sortie_zero_*.txt`).** *Prédiction* : près d'un zéro de V₀, ‖V₀‖≃(v²(s−s₀)²+(d+a_hδ)²)^{1/2} ⇒ T''(δ)=+(2Ba_h²/v)·ln δ+lisse, B=κ₂e^{−κ₃(T−s₀)}/Ṗ₀(T), **sans paramètre libre** (a_h=O(ε), signal singulier O(ε²ln(1/δ)); C² si d≫a_hδ ou a_h=0). *Construction* : racine (pas minimum) de la distance signée g(ang) de la courbe t↦V₀(t) à l'origine, en l'angle du protocole (brentq), épisode 7, Uamp=2,45 (2,31 pour λ ε=0,05), g≈10⁻¹⁸, ‖V̇₀‖∈[0,03;0,06], mot conservé. Zéros obtenus : γ₁ seul ε=0,02/0,05/0,1 (ang=0, symétrie y→−y exacte à tout ε), λ seul ε=0,02 et 0,05, couple ε=0,02; **pas de zéro trouvé** (domaine Uamp∈[2,25;2,49], |ang|≤1,5°) pour λ ε=0,1 et le couple ε=0,05/0,1 (pas une preuve d'inexistence). *Artefact démasqué* : DOP853 ordinaire (rtol 1e-12) donne au zéro exact un **faux** signal Q_T/ε divergent quand δ→0 (0,15→3,2 pour γ₁, ε=0,02), même dans le cas symétrique où la théorie n'en prévoit aucun, et dépendant de rtol (erreur ≈d²/v≈10⁻¹⁰ : le coude de ‖V₀‖ est enjambé); corrigé en réintégrant depuis 0 avec coupures en t_c±W et pas max W/300; plancher d'arrondi restant : différences secondes de T≈10⁻¹³ à δ=10⁻⁵ ⇒ pentes ajustées sur δ∈[10⁻⁴;5·10⁻³]. *Résultats* : (1) rang 6 (avant le zéro) : Q/ε constant à 4 chiffres; (2) **zéro symétrique (γ₁)** : Q_{T₇}/ε constant en δ à 4 chiffres (0,07656; 0,07274; 0,07106 à ε=0,02/0,05/0,1), pentes en ln δ ~10⁻⁷ : **(N) n'est pas nécessaire** (traversée 1D, T₇ reste C²); (3) **zéro non symétrique (λ)** : Q/ε croît quand δ↓ (ε=0,05 : 8,7·10⁻³ à δ=10⁻² → 3,6·10⁻² à 10⁻⁴), pente en ln δ positive dans les 12 directions, **rapport mesure/prédiction 1,04–1,07 (7 directions |a_h|≥1,5·10⁻³, ε=0,02, médiane 1,06) et 1,06–1,12 (8 directions |a_h|≥3·10⁻³, ε=0,05)**, 1,13–1,6 pour les petits a_h; direction 0 : pente locale 6,45·10⁻⁵ pour δ≥10⁻³ = valeur prédite à 0,2 %; l'écart résiduel de quelques % n'est pas expliqué; (4) distance au zéro (λ ε=0,02) : pente 6,7·10⁻⁵ (d=10⁻¹⁰) → 2,3·10⁻⁵ (5·10⁻⁷) → −3,8·10⁻⁶ (5·10⁻⁶) → ≤10⁻⁷ dès d=5·10⁻⁵≫a_hδ_max≈10⁻⁵ : C² retrouvé. *Lecture* : à une traversée exacte transverse non symétrique T_r n'est pas C² (T''~ε²ln(1/δ)); reste de Taylor du Th. 2' heuristiquement O(εδ²(1+ε ln(1/(εδ)))), défaut encore o(δ); la non-annulation n'est ni superflue ni nécessaire en général; condition suffisante plus fine suggérée (non démontrée) : tout zéro intérieur a un déplacement transverse nul. Limites : épisode 7, nœud forcé, zéro isolé obtenu par l'angle du protocole, pas de zéro de H₀, pas de nœud non forcé.

**Lemme de singularité logarithmique (`lemme_singularite_log.tex`, octobre 2026, démontré sans référence à IWS).** F(δ)=∫_J g|W(s,δ)|ds, W∈C²(J×(−δ₀,δ₀);ℝ^m), m≥2, zéros de W(·,0) en nombre fini, intérieurs, simples, g(s_k)>0, déplacement transverse a_k=|P⊥_{w_k}∂_δW(s_k,0)|>0 à chaque zéro (H3) ⇒ F''(δ)=Σ(2g(s_k)a_k²/v_k)ln(1/|δ|)+O(1) et F(δ)+F(−δ)−2F(0)=Σ(2g(s_k)a_k²/v_k)δ²ln(1/|δ|)+O(δ²) : F n'est pas deux fois dérivable en 0, les zéros ne peuvent pas se compenser (coefficients ≥0). Preuve : minoration |W|≥c·max(|σ|,|δ|) (IFT/Taylor, cas |σ|≷K|δ|), formule F''=∫g|P⊥_W∂_δW|²/|W|+O(1), découpage C/A/B (la zone B donne a²/(v|σ|) intégré sur K|δ|<|σ|<η), puis F(δ)+F(−δ)−2F(0)=∫₀^δ(δ−r)(F''(r)+F''(−r))dr. Corollaire (temps implicite, IFT en (δ,σ)) et proposition d'application au noyau sous (a)–(d) : différence seconde signée de T_r = −Σ(2B_ka_k²/v_k)δ²ln(1/|δ|)+O(δ²), B_k=κ₂e^{−κ₃(T₀−s_k)}/Ṗ_i(T₀). Vérifié sur un jouet sans lien avec IWS (`verif_lemme_log_abstrait.py`, m=2,3 : résidu constant 2,2291 / 2,0094). **Précisions** : (i) signé ≠ Q_T (valeur absolue), pentes positives en ln δ = coefficient −2Ba²/v de ln(1/δ); (ii) « déplacement transverse nul au centre » ne suffit pas pour C² sur la boule (il faut contrôler a(ϑ)²ln(1/d(ϑ)) partout; cas γ₁ : a≡0 par symétrie); (iii) zéros testés hors du voisinage ε₁ : min‖V₀⁰‖ de la référence ε=0 vaut 2,1·10⁻⁵ (λ, ε=0,02; ε/min≈970), 7,1·10⁻³ (λ, ε=0,05; ε/min≈7), 0 (γ₁) ⇒ pas de contradiction avec le Th. 2. **Relecture de Benoit (validée)** : lemme démontré, C² de W et C¹ de g suffisent; corrections : (H1) doit imposer **p≥1** (sinon A=0 et la conclusion est fausse), tableau « H1–H3 avec p≥1 »; proposition d'application : ajouter V_i(0)≠0 et V_i(T₀)≠0 (zéros de bord = résultat distinct), et expliciter (a) : W construite par le sous-système régulier (H,V,τ) sans flot étendu (état post-saut précédent C², traces non nulles, u∈C¹) ⇒ pas de circularité; lieu {d=0} hypersurface seulement dans le cadre plan m=2 non dégénéré; une racine de distance signée à 10⁻¹⁸ ne certifie pas un zéro exact du système continu (statut numérique du témoin). **Versant symétrique (lemme 2, démontré)** : W=e·q(s,δ), q∈C², zéros simples, q≠0 aux bords ⇒ F=∫g|q| est C² avec F''=∫g sgn(q)q_δδ+Σ2g q_δ²/|q_s| (racines mobiles par IFT, termes de bord nuls); corollaire T∈C²; proposition : symétrie de réflexion ⇒ C² malgré le zéro (explique γ₁ seul). **Non couvert** : zéros avec a_k=0 hors symétrie, zéros de ‖H‖, zéros doubles, nœud non forcé, formulation de la condition géométrique fine.

**Vérification numérique des hypothèses sur le témoin** (`verif_hypotheses_theoreme.py`; **δ = écart-type du bruit gaussien sur les 12 coordonnées de ϑ, pas rayon d'une boule fermée** : un minimum d'échantillon ≈10⁻⁴ signale une proximité, ne démontre pas qu'une trace nulle existe dans la boule). δ=0,003, 548 tirages, mot périodique à 6 sauts : ν≃1,42, g≃0,51; **σ_r décroît** le long du mot (1,21→0,12 en sept Kairos); min‖τ_j‖ aux Kairos ≥0,018; min sur l'horizon 0,0099; marges de frontière min 5,6·10⁻⁵ (saut 1), médiane ~2·10⁻³. À δ=0,03 (323 tirages, 4 sauts) le min sur l'horizon tombe à ≈10⁻⁴ : l'hypothèse de trace non nulle n'est plus plausible uniformément et K devrait être restreint.
*Prédiction « premier ε de perte du mot ≈ marge/|h| »* (h=d(marge signée)/dε par différences finies à ε=0,02) : grille grossière, δ=0,003 : 387 pertes avant ε=1,4, toutes prédites, Spearman 0,92, observé/prédit médian 1,92. **Grille fine** (`verif_seuil_grille_fine.py`, rapport 1,06, ε de 0,02 à 1,5, même échantillon) : 439 pertes, toutes prédites, **Spearman 0,996**; seuil vrai dans ]préc, obs] : observé/prédit médian **1,70** (quartiles 1,59–1,82), **précédent/prédit médian 1,61** (1,50–1,72) ⇒ **le facteur n'est pas un artefact de grille** (même la borne inférieure dépasse la prédiction). Le rapport croît avec ε_pred (médianes 1,47 ; 1,66 ; 1,77 ; 1,89 par quartile), compatible avec un terme d'ordre ε² dans la marge, **mais l'attribution à la courbure reste une hypothèse** (non isolée : il faudrait ∂²_ε de la marge). La marge seule ne prédit rien (Spearman 0,31); à δ=0,03 la prédiction linéaire est médiocre (13 prédits pour 16 observés, Spearman 0,58, rapport médian 0,15).
*Régularité C² ponctuelle* (`verif_regularite_C2.py`): différences secondes centrées Q(δ,h)=‖τ_ε(ϑ₀+δh)−2τ_ε(ϑ₀)+τ_ε(ϑ₀−δh)‖/δ², 8 directions, δ∈[2,5·10⁻⁴;4·10⁻³], rangs 2 à 6 : à ε=0 max Q≤7,5·10⁻⁸ (arrondi); à ε>0, **Q/ε constant à 4 chiffres en δ** (aucun facteur log(1/δ) au centre) et linéaire en ε à 1–8 % (ε=0,02→0,1). Compatible avec Th. 2 **au point de référence où aucune norme ne s'annule**; ne teste pas un point où V₀ ou H₀ passe par l'origine.
*Non-annulation des normes (N2)* (`verif_nonannulation_normes.py`): nœud déclencheur toujours le nœud forcé 0; ‖V₀‖/s→2,499, ‖H₀‖/s²→1,250 (attendu |u|=2,5 et |u|/2); minima sur s>2·10⁻³ : ‖H₀‖/min(s,1)²≥1,08, ‖V₀‖/min(s,1)≥0,061. **Mais le min de ‖V₀‖ par épisode décroît ×≈0,55 par Kairos** (1,113 ; 0,688 ; 0,388 ; 0,207 ; 0,107 ; 0,061 aux épisodes 2 à 7) ⇒ (N2) tient à chaque profondeur fixée, mais M_r (dérivées de ‖V₀‖, en 1/‖V₀‖) **se dégrade avec r** : aucune uniformité en k à attendre sans mécanisme.

**Témoins numériques** (`finger_perturbation.py`, `finger_perturbation_ball.py`, `finger_perturbation_depth.py`; noyau complet Γ=γ₀+γ₁‖τ_i‖, M(τ_i) par nœud; N=6, graphe A1_kept1, protocole constant de référence, y de référence, instant de Kairos interpolé exactement, dt=2·10⁻³; rang r = r-ième instant de Kairos, r=1 : état initial). ε=0 : le noyau couplé reproduit la forme affine à 10⁻¹⁵ (rangs 2 à 8). Mesures : dev_r = distance max à la forme affine **de ε=0** (même ϑ); oos_r = résidu max hors échantillon de la forme affine **ajustée à ε** (perte d'affinité). γ₁ et λ variés séparément, puis ensemble (γ₁=1,25ε, λ=2ε).
1. *Un paramètre caché* (φ₄∈[220°;225°], 41 points, mot w=((0,{1,2,3}),(0,{1,4,5})), ε∈[10⁻⁵;10⁻¹]) : dev_r ∝ ε, **pente log-log 1,000** aux rangs 2, 3, 4 et pour les trois balayages; C=dev/ε : γ₁ 7,5·10⁻³ / 1,6·10⁻² / 2,6·10⁻²; λ 8,4·10⁻⁴ / 4,3·10⁻³ / 1,3·10⁻² (rangs 2/3/4). **Mais** oos ≤ 2·10⁻¹⁰ jusqu'à ε=0,1 : **indicateur non discriminant** — sur une fenêtre de 5° toute fonction lisse est affine dans (1,cosφ,sinφ) à O(w³)~10⁻⁴ près. Ce résidu hors échantillon ne dit rien sur la perte d'affinité (leçon 9).
2. *Boule complète de τ⁰∈ℝ^{12}* (bruit gaussien d'écart δ autour de φ₄=222,5°; forme testée τ^{(r)}=b_r+L_r τ⁰; mot retenu : 370/400, 273/400, 215/400 tirages pour δ=0,003; 0,01; 0,03) : dev ∝ ε (pente 1,000), **oos ∝ ε** (pente 1,00) **et oos/ε ∝ δ^{1,8–2,0}**; dev/ε dépend très peu de δ (pente 0,09–0,17). Lecture : la distance à la forme affine découplée est O(ε), la **perte d'affinité** est O(εδ²) (second ordre dans l'amplitude cachée), ce que l'argument perturbatif prédit.
3. *Profondeur* (δ=0,003, 600 tirages, rangs 2 à 8; le mot le plus peuplé, 561/600, est **périodique** : ((0,{1,2,3}),(0,{1,4,5}))³) : dev ∝ ε (écart à la linéarité ≤1,5 % à ε=10⁻²). C_r=dev/ε aux rangs 2…8 : **γ₁** 7,7·10⁻³ ; 1,65·10⁻² ; 2,7·10⁻² ; 3,6·10⁻² ; 4,1·10⁻² ; 4,3·10⁻² ; 4,0·10⁻² (**sature**); **λ** 8,9·10⁻⁴ ; 4,5·10⁻³ ; 1,3·10⁻² ; 3,1·10⁻² ; 5,9·10⁻² ; 9,7·10⁻² ; 1,4·10⁻¹ (**croît**; rapports successifs 5,0 ; 3,0 ; 2,3 ; 1,9 ; 1,7 ; 1,5, décroissants; différences 3,6·10⁻³ → 4,5·10⁻²); **couplé** 8,8·10⁻³ ; 1,6·10⁻² ; 1,6·10⁻² ; 2,4·10⁻² ; 7,4·10⁻² ; 1,5·10⁻¹ ; 2,5·10⁻¹ (non additif : compensation partielle aux rangs 3–4). oos/ε reste ~10⁻⁶–10⁻⁵ (δ=0,003), croît d'un facteur ≈4 sur les 7 rangs.
4. *Perte du mot à couplage fort* (profondeur 8, δ=0,003) : mot conservé pour (γ₁,λ)=(0,0125;0,02) et (0,125;0,2) : 561/561; (0,3;0,5) : 560/561; (0,6;1) : 545/561; **(1,25;2) : 370/561** (4 chemins distincts) — l'issue (3) apparaît aux valeurs de l'Annexe F. Sur la fenêtre à un paramètre (φ₄∈[220°;225°], rangs ≤4), le mot est en revanche conservé à pleine force (41/41), dev=1,8·10⁻² au rang 4.

*Lecture prudente.* Ces témoins sont **compatibles** avec l'énoncé candidat à mot fixé, et distinguent les issues : à petit ε, l'issue (1)/(2) (perte d'affinité de second ordre en δ, écart O(ε)); à pleine force l'issue (3). La croissance en k de C_{K,k} est **différente** pour γ₁ (saturation apparente) et λ (croissance, polynomiale ou lentement exponentielle : 7 rangs sur un seul mot périodique ne les départagent pas). **Limites** : un seul témoin (N=6), un seul mot (périodique, donc pas la croissance 3^n des mots), un seul protocole, δ≤0,03; ‖τ_i‖ reste loin de 0 (la non-différentiabilité de γ₁‖τ‖ n'est pas sollicitée); la taille de la chambre quand ε→0 et l'uniformité sur K plus grand ne sont pas testées; la structure des parois (nombre de murs) n'est pas mesurée.

**Questions ouvertes du programme** : (a) mécanisme préservant une classe de fonctions sous l'évolution hybride (au-delà de l'affine); (b) comportement de C_{K,k} en k sur des mots non périodiques et autres chambres; (c) énoncé intrinsèque pour γ₁>0 seul vs λ>0 seul (l'expérience suggère des rôles différents); (d) autonomie conditionnelle du visible : quelle condition la remplace quand τ entre dans V̇ (le visible dépend alors de ϑ à mot fixé, à l'ordre ε); (e) contrôle des murs (nombres de chambres) sous perturbation près d'une tangence.

---

## 6. État du manuscrit (v5.16)

- **Compilation** : `pdflatex` passe (37 pages, figures externes exceptées); 90 environnements appariés, aucune référence sans cible. **v5.16 ne diffère de v5.15 que par le titre et trois retouches de `prop:annulation-conique`** : τ_⋆ de classe C¹ et non nulle près de μ_* ; IFT nommé dans les variables (ρ,ε) pour l'équation ε=ρℓ(θ_±(μ_*+ε))+O(ρ²), de dérivée −ℓ_± en ρ au point (0,0) ; énoncé inchangé par ailleurs.
- **Contenu à jour** : présentation 𝐒, C0–C4 avec C23^pot/C23^act, taxonomie à trois canaux, G₀/G₁, flèches structurelles/événementielles, §« Exploration à profondeur finie des fibres d'opacité » (finitude, constance du readout, complétude de ∼_N, lemme de transport, premier franchissement de marge, paire miroir R_y, forme affine, conservation du support, borne locale, fermeture exacte au rang impair, réduction semi-algébrique, bornes de croissance **ties inclus** `cor:borne-croissance-ties`), crash-test « Témoin N=6, doigt de la coupe site2_bas », `prop:annulation-conique`, sous-section « Variation du présent observable : base triviale, partitions variables », `rem:definissabilite-locale`.
- **Chantier de notation (v5.9 → v5.15), clos** : C→Ξ (chambre), F_y→𝒪_y, q→ϑ, Q→Dep, s_r^ε→ν_r^ε, d→p, E_r→Ω_k^sing (puis supprimé, ties intégrés), G_k→Aut_k, K_N→κ_N, a_i,s_i,χ_ij pour les scores, τ_⋆, μ_w, convention k/r (« au r-ième Kairos d'un mot de profondeur k, 1≤r≤k ; J_r^±=J_k^± si r=k »), chambre = composante connexe d'une classe de mot, **classe de mot** pour les sections expérimentales; plus de numéro de version dans le contenu des énoncés (titre seul); paramètre de variation μ (le seul η restant est le morphisme de monoïdes), R_j(μ), b_{j,w}^{(r)}(μ), Δ_{j,w}^{(r)}, Ψ_j, Y_adm:=ρ_X(C).
- **Vérifié** : preuve conique correcte (coordonnées polaires, IFT en (ρ,ε)), tous les chiffres du crash-test concordent avec les sorties de `finger_delta_check.py`, identité Δ′=2det[∂_φΨ,∂_μΨ].
- **Restes (facultatifs, rédactionnels)** : (a) la lettre R sert encore au rayon R_j(μ) et à l'application de réponse R_x^{ρ_int} (types et indices diffèrent, tolérable; sinon ϱ_j ou r_j — r est le rang); (b) la formule |𝒫_{2n}^{loc}|=3^n utilise n comme indice nu alors que n_r^ε=|J_r^ε| est défini ailleurs (sans ambiguïté de lecture); (c) la référence Barone–Basu est vérifiée (Thm 1.1 de DCG 47 (2012) 577–597) — plus rien à faire de ce côté.
---

## 7. Questions ouvertes

**Théorie de la classe**
1. **C5** (fermeture de la boucle historique) : piste par le préordre de simulation ⪯ ou par la quantification universelle sur l'autre fibre; quantificateurs non stabilisés. Le chantier F_y/∼_N doit d'abord dire ce que C5 devrait mesurer.
2. **G₂** (temps intrinsèque) : différé tant qu'aucun témoin ne l'exige.
3. **C23^act** : IWS exige-t-il l'efficacité actualisée, ou la capacité de l'organisation suffit-elle ?
4. **Structure du monoïde 𝔐** : libre sur les épisodes, ou quotienté par des relations temporelles (fusion des délais) ?
5. **Unification catégorique** : la charpente existe (𝔥_G, 𝔥_G^obs, flèches structurelles/événementielles), mais aucun énoncé ne dit qu'il s'agit d'une seule structure au sens fort. S_𝒜 et Ω_{𝒫,ρ} (Annexe H, écrire/lire) comme flèches composables : en réserve.
6. **Socle** : choix du Kairos au contact (à assumer dans le Tome I avec sa discontinuité aux contacts tangents); les hypothèses de la proposition d'invariance sont-elles générales ou le noyau est-il un cas favorable (C fermé, garde scalaire) ? Hypothèse « admissibilité constante sur F_y » à confirmer sur la définition formelle de 𝔐_x du socle.
7. **Quand la stratification, l'o-minimalité ou le temps propre deviennent-ils nécessaires** : terrain concret (§5) mais pas tranché.
8. **Régime γ₁, λ > 0** : le noyau n'est pas encore traité (τ entre dans V̇; la complétude de §4.2 est cassée; l'argument de répertoire plus difficile). Première exploration perturbative : §5.8 (énoncé candidat à mot fixé + témoins numériques).

**Programme F_y/∼_N et tameness**
9. **Uniformité en k** (laissée ouverte à dessein) : nombre de strates de la famille y↦𝒫_k(T;y), constantes B_sa, B_conn, exposant p en fonction de k, N. Pour le régime perturbatif : croissance de C_{K,k} (saturante pour γ₁, croissante pour λ sur un mot périodique, §5.8).
10. **Au-delà des bifurcations de niveau ϑ** : extension de la définissabilité à travers les bifurcations événementielles (contact tangent, Kairos simultanés, P franchissant Θ) — la « famille de partitions définissablement triviale » n'est établie que sur domaine compact régulier.
11. **Expérience de variation de y** : un seul témoin, une seule coupe, un seul sens (η<0). À faire : côté η>0 (fenêtre englobant tout le doigt), localisation fine de η* pour les deux autres composantes (H(0) comp. 1 du nœud 0; comp. 0 du nœud 3) avec interpolation de l'instant de Kairos, et d'autres coupes/rangs; test d'un pli régulier (largeur en √) pour confronter les deux mécanismes.
12. **Minimalité** : implémenter 𝒰₂/𝒰₁; tester un autre nœud forcé sous 𝒰₅ pour B et C (promouvoir ✗ observé en ✗ prouvé ou le réfuter); obstruction séquentielle sur R₀^{(1,2)} : construire un témoin de Nerode (x,x′) dont les murs k=1 et k=2 exigent une combinaison (θ₁*,θ₂*) hors de l'image de F₂; rejouer la recherche de contre-exemple à 𝒰₄ avec le moteur corrigé si elle doit entrer dans le manuscrit.
13. **Marges** : cas i*=q (nœud perturbé devenu i*), ties exacts, rangs avec m=0 — réserves formelles du mécanisme de premier franchissement de marge (non rencontrées numériquement); autres paires de référence que φ₇/δ=60°.
14. **Croissance** : dominance de τ₁ parmi {1,4,5} (arbre ternaire) démontrée uniformément sur la descendance ? Point triple et entrelacement N_int à r>4 ? N=9 : profondeurs 8–10 et scissions portées par une symétrie autre que (2 6)? Gel exact des paires entre nœuds ϑ-indépendants : prouvé (lemme de conservation), mais l'exclusion de ces paires de N_pair est une convention à fixer dans la définition des compteurs.
15. **Limites de la coupe du doigt à 219°** : les trois angles cachés φ₁,φ₂,φ₃ sont fixés; l'intérieur de Ω_w n'est établi que dans la coupe (φ₄,φ₅).
16. **Programme de soustraction** (§5.8) : (a) mécanisme préservant une classe de fonctions sous l'évolution hybride; (b) C_{K,k} sur mots non périodiques, autres chambres, N=9; (c) rôles distincts de γ₁ et de λ; (d) remplaçant de l'autonomie conditionnelle du visible quand τ entre dans V̇; (e) contrôle du nombre de murs près d'une tangence; (f) Th. 1 : pas de nouvelle modification (Benoit); Th. 2 / P2 : voir `regularite_P2_transmission.tex` — transmission C² et nœud forcé démontrés (à relire : termes de saltation d'ordre 2 du lemme V), **nœud non forcé ouvert** ; test de nécessité **fait** (témoin) : (N) non nécessaire sous symétrie (γ₁, traversée 1D), nécessaire sans symétrie (λ : T''~(2Ba²/v)ln δ vérifié à 4–12 % près) — reste à formuler/démontrer la condition fine « déplacement transverse nul aux zéros », à tester des zéros aux rangs ≤6 et par variation de l'état initial y, et ‖H₀‖; (g) borne **polynomiale** en r sur C_r (stabilité incrémentale du flot découplé) — cœur de l'uniformité en k; (h) expliquer le facteur ≈1,7 (grille fine : ni artefact de grille, ni encore attribué) entre ε* prédit et observé : isoler ∂²_ε de la marge.

---

## 8. Corrections et affirmations retirées

| Affirmation retirée / corrigée | Remplacement | Origine |
|---|---|---|
| I1/I2/I3 comme axiomes constitutifs | C0, C1, C23^pot, C4; I1_ρ/I2 = taxonomie diagnostique (F, D, K*) | V5.2 |
| « Le noyau satisfait I2 tel que rédigé dans le v4 » | faux (π_{¬s}𝒦 ne dépend pas de A) ; I2b retypé puis absorbé dans C23 | crash-test 1 |
| « 𝔐^adm_x ne dépend que de π_s(x) » | ρ_X(x)=ρ_X(x′) ⇒ 𝔐^adm_x=𝔐^adm_{x′} | Benoit |
| ω̂ dans l'objet constitutif | retiré (monotonie, ω̂=id); ψ_X=ψ_s×ψ_int | V5.1 |
| Union 𝔐^adm=⋃_x𝔐^adm_x | famille indexée par l'état | V5.2.1 |
| Compte « 5 chambres, stable à k=5 » (grille 32×32) | artefact de sous-résolution; ≥9 chemins à k=4 au zoom | §4.10 |
| « Le système reste fini » (N=6) | fini à chaque k, croissance 3^{k/2} non bornée mais structurée | relecture §4.13 |
| Antidiagonale φ₄=−φ₅ = mur transverse | symétrie R_y du protocole mono-axe | §4.6 |
| Échantillons 𝒰̂₃, 𝒰̂₄ disjoints (k_min(𝒰₃)=5>k_min(𝒰₄)=1) | emboîtement par construction | Benoit |
| Bug de regroupement dans `run_pair_family` (non déterminisme par hachage) | regroupement figé (`groups_map`); k_min de la matrice inchangés; {2,4,5} : 30 % → 17,4 %; {2,4,6} : 0/327 → 2/327 | erratum §4.17 |
| Mauvais graphe retapé à la main (Aut=2 au lieu de 1) | rechargé depuis `nerode_pairs.pkl` | §4.17 |
| Candidats contre-exemple à 𝒰₄ (N=6, N=9) | tous séparés après stress-test dense; ✗ de grille ≠ preuve | §4.17 |
| Mur d'ajout attendu entre 6 et 7/8 | mur actif entre 4 et 5 (7,8 trop loin : cos ≈ −0,86 à −0,99) | §4.17 |
| Différence 1,4,5 vs 2,4,5 « effet de l'échange 1↔2 » | artefact de contexte τ (contrôle d'équivariance) | §4.15 |
| Recette « p,q identiques + r,s qui diffèrent en angle » (cacher une différence derrière Q) | fuite dès k=1 (115/144 protocoles séparent) | §4.17 |
| Borne de croissance hors des ties (Ω_k^sing) | ties et traces nulles = strates de signe ordinaires; exposant p conservé; Ω=⊔Ω_w exact | v5.14 |
| « Sur y compact et k fixé, tout est définissable dans R_an » | hypothèses explicites (analytique, compact, transverse); pas d'uniformité en k | Benoit (v5.14) |
| Corollaire de conservation « non constante ⟺ i∈Dep » | seule l'implication i∉Dep ⇒ constante est affirmée | v5.12 |
| Preuve conique par IFT à l'origine | coordonnées polaires; IFT en (ρ,ε) | v5.15 |
| **η* ≈ −0,167** (interpolation du balayage) | **η* = −0,161819** (instant de Kairos exact) | §4.32 |
| Largeurs de doigt 0,66 ; 0,41 ; 0,29 ; 0,17 ; 0,11 ; 0,051 ; 0,021 | 0,648 ; 0,374 ; 0,257 ; 0,136 ; 0,074 ; 0,0115° (η = −0,05 … −0,16) | §4.32 |
| Rapport largeur/d « dans [51 ; 54] » comme loi | loi linéaire en η−η* (K=6,347°/unité) plus propre; plateau 6,25–6,33 | §4.32 |
| Référence Barone–Basu « non vérifiée » (étiquette, pages, DOI) | vérifiée par Benoit sur le PDF : Thm 1.1, DCG 47 (2012) 577–597, DOI 10.1007/s00454-011-9391-3 | octobre 2026 |
| Mention « V5.x » dans les énoncés | retirée (titre seul) | v5.10–v5.13 |
| « Le mot et les temps de Kairos sont des fonctions de y seul » | autonomie **conditionnelle** : (y,u,w)↦(H_w,V_w,P_w,t*_{k,w}) est ϑ-indépendante à mot fixé, mais (y,ϑ,u)↦w peut dépendre de ϑ (§5.8) | Benoit, oct. 2026 |
| Lemme orbital / R_y présentés comme prouvant la « nécessité » du départage par indice / de la direction indépendante | ils prouvent une **incompatibilité** (au moins une exigence à abandonner) et la nécessité de **briser** l'obstruction R_y; indice et direction indépendante sont des solutions, non démontrées uniques (§4.3, §5.1) | Benoit, oct. 2026 |
| « Contrôle du temps d'impact par IFT (exige de la régularité du protocole) » | franchissement monotone (Ṗ lipschitzienne en t): u∈L^∞ suffit pour le Th. 1; la régularité de u (C¹) n'est requise que pour le Th. 2 | oct. 2026 |
| Résidu affine hors échantillon sur fenêtre de 5° comme test de perte d'affinité | indicateur aveugle (O(w³)); test sur la boule complète de τ⁰∈ℝ^{12}, où oos∝εδ² (§5.8) | oct. 2026 |
| Th. 1 v1 : Ṗ⁰_{i_r}≥ν/2 sur une fenêtre centrée en t_r⁰, comparaison des trajectoires hybrides au premier instant de saut | fautif (P_{i_r} réinitialisé à r_PΘ; la comparaison au premier saut n'est pas O(ε) a priori) ⇒ v2 sur prolongements virtuels pré-impact (z̃_r^ε, z̃_r^0, même graphe A_{r−1}) | Benoit, oct. 2026 |
| Hypothèse P2 « P de classe C² » | mauvais objet (P hybride discontinue à sa réinitialisation) ⇒ régularité requise du prolongement pré-impact P̃_r | Benoit, oct. 2026 |
| « C² après intégration de ‖H‖,‖V‖ va de soi » | faux en général (J(h)~h²log(1/|h|)); condition de non-annulation (N2) requise | Benoit, oct. 2026 |
| e^{LT} dans la constante A de la récurrence | A_r ne dépend que de la longueur ℓ_r de l'épisode (la borne a priori R, L dépend encore de l'horizon) | oct. 2026 |
| « δ » = rayon de boule | δ = écart-type d'un bruit gaussien; un min d'échantillon ≈10⁻⁴ ne prouve pas une trace nulle dans la boule | oct. 2026 |
| Facteur 1,92 attribué à la courbure en ε | grille grossière non seule en cause (grille fine : 1,61–1,70), mais attribution à la courbure **non démontrée** | oct. 2026 |
| Récurrence du Th. 1 menée jusqu'à r=k avec graphes synchronisés après le k-ième saut | sans marge au rang k : récurrence complète pour r≤k−1, rang k = comparaison pré-impact seule | Benoit, oct. 2026 |
| r_P∈]0,1] | r_P∈]0,1[ (sortie du garde après le saut) ; ρ lié à δ_post=min((1−r_P)Θ,σ) | Benoit, oct. 2026 |
| A_k = graphe après le k-ième saut « déterminé par w » | A_r défini pour 1≤r≤k−1 seulement (le k-ième recâblage n'est pas dans le mot); constante de récurrence renommée Υ_r (A réservé aux graphes) | Benoit, oct. 2026 |
| Minima ν_τ, μ sur ensembles possiblement vides | convention min∅=+∞ : hypothèses sans objet pour k=1 ou sans sélection compétitive; le théorème couvre ces cas | Benoit, oct. 2026 |
| A_k = graphe après le k-ième saut « déterminé par w » | A_r défini pour 1≤r≤k−1 seulement (le k-ième recâblage n'est pas dans le mot); constante de récurrence renommée Υ_r (A réservé aux graphes) | Benoit, oct. 2026 |
| Minima ν_τ, μ sur ensembles possiblement vides | convention min∅=+∞ : hypothèses sans objet pour k=1 ou sans sélection compétitive; le théorème couvre ces cas | Benoit, oct. 2026 |
| « La référence n'a pas de Kairos sur J_r » | elle en a un en t_r⁰ : elle n'a pas encore sauté sur [T,t_r⁰[ et aucun autre nœud n'atteint le seuil (étape b) | Benoit, oct. 2026 |
| Th. 2 : hypothèse « dérivées d'ordre 2 de P̃ de classe C¹ en ε » | exigerait des dérivées troisièmes en temps (T dépend de ε), donc u∈C²; remplacée par C² en ϑ à ε fixé + estimation O(ε) des variations par Grönwall | oct. 2026 |
| « Zéro de trace proche » comme explication d'un écart de 30 % sur Q_T/ε (rang 1, δ=4·10⁻³) | artefact de pas de temps (écart ∝ dt); min‖τ_j‖=0,176 sur l'épisode 1 | oct. 2026 |
| Lemme V : X_{j+1}=D_ξΦ[R_jX^{tot}_j+(R_jĝ⁻−ĝ⁺)D_xT_j] | double comptage de ĝ⁻D_xT_j : X_{j+1}=D_ξΦ[R_jX^{fix}_j+(R_jĝ⁻−ĝ⁺)D_xT_j]=D_ξΦ[R_jX^{tot}_j−ĝ⁺D_xT_j] | Benoit, oct. 2026 |
| Flot étendu (H,V,τ,P) utilisé dès t=0 | état initial H=V=0 hors du domaine où ‖H‖,‖V‖ sont lisses : sous-système (H,V,τ) + Duhamel pour P sur le premier épisode | Benoit, oct. 2026 |
| Lemme de démarrage invoquant les estimations O(ε) du lemme V (et réciproquement) | circularité levée : régularité seule au démarrage, estimations quantitatives dans le lemme V | Benoit, oct. 2026 |
| Remarque de Leibniz avec f quelconque | f=ψ_i (production de pression); le saut de P_i s'ajoute à part | Benoit, oct. 2026 |
| Lettre κ pour des constantes de Lipschitz | κ réservé à la pression (Vol. I) : K_P, χ_r | Benoit, oct. 2026 |
| Mot de profondeur k = k impacts avec leurs recâblages | mot = k−1 recâblages + k-ième impact pré-saut | Benoit, oct. 2026 |
| Signal log(1/δ) de Q_T/ε au zéro exact de V₀ (DOP853 ordinaire) | artefact d'intégration (coude de ‖V₀‖ enjambé; dépend de rtol); signal réel obtenu après réintégration coupée au minimum | auto-contrôle (variation de rtol), oct. 2026 |
| « (N) est nécessaire » ou « (N) est superflue » | ni l'un ni l'autre : non nécessaire sous symétrie (traversée 1D), nécessaire sans symétrie (zéro transverse) | test de zéro, oct. 2026 |
| Zéro de V₀ cherché par minimisation de ‖V₀‖ | racine de la distance signée (en dimension 2 un minimum faible ne garantit pas une traversée) | Benoit, oct. 2026 |

---

## 9. Notations réservées, scripts et données

**Notations (collisions déjà résolues, à ne pas recycler)** : ρ_X (lecture constitutive d'état), ρ_int, π_s, r_s ; Ξ (chambre), Dep, ν_r^ε, n_r^ε=|J_r^ε|, p (dimension de Ω⊂(S¹)^p), Ω_w, Σ, Φ, ϑ, μ (variation de y), Ψ_j (application locale), R_j(μ), b_{j,w}^{(r)}(μ), λ_{r,w}, a_i, s_i, χ_ij, g_ij^{(r)}, τ_⋆, κ_N, κ_sa, 𝒪_y, Aut_k, 𝔊_N (graphe dans l'espace d'états; 𝒢 pris par la regraine), ν (valeur propre de Ã, Annexe C — à confirmer), u (entrée), s (structure), Q (préconditionneur du noyau, §12), h (boucle symétrique), η (morphisme de monoïdes), E (énergie), μ_w.

**Scripts et sorties** (copies dans `IWS_numerics_y_variation/`, sur le Mac dans `scripts/`) :
- noyau : `iws_kairos_core.py` (md5 b6a66f357aa08de1177b6b403a52f45e), `iws_kairos_core_gen.py`, `iws_kairos_interp.py` (instant exact; `patch(dt)`) ;
- socle/obstruction : `temoin_C23_noyau.py`, `equivariance_check.py`, `orbit_diversity.py`, `orbit_track_depth.py`, `check_period.py`, `reinjection.py` ;
- partitions : `partition_Fy.py`, `partition_Fy_depth2*.py`, `partition_Fy_depth2b_2Dforce.py`, `depth_growth*.py`, `adaptive_refine*.py`, `zoom_deep_genealogy.py`, `n9_etape1.py`, `n9_depth_growth_4branches*.py`, `n9_equivariance_control.py`, `n9_resample_conditioned.py`, `n9_246_*.py` ;
- minimalité : `nerode_separating_families.py`, `nerode_matrix_full.py`, `nerode_u5_diagnose.py`, `nerode_mechanism_check.py`, `nerode_u4_counterexample_search.py`, `nerode_sensitivity_jacobian.py`, `nerode_n9_u4_vs_u3.py`, `nerode_R0_mapping.py`, `nerode_R0_sequential.py`, `nerode_R0_jacobian.py`, `nerode_Q_witness_attempt.py`, `nerode_phi7_*.py` (chamber_maps, chamber_amplitude, margin7_signed, margin7_sequence, margin7_plot) ;
- surfaces et croissance : `contour_active_walls.py`, `contour_active_walls_fixsigma.py`, `growth_counting.py`, `growth_counting_v2.py`, `gram_test.py`, `jr_q_analysis.py`, `affine_form_check.py`, `affine_form_check_exact.py` ;
- variation de y : `finger_y_variation.py` (balayage en η; env PHI_LO/PHI_HI/NEAR/TAG/NPHI), `finger_profile.py`, `finger_critical.py` (d_min, côté, largeur), `finger_width_scan.py`, `finger_other_component.py`, `finger_delta_check.py` (ajustement affine, racine de Δ, φ*, transversalité, K conique, largeurs modèle; env INTERP, argv dt), `finger_delta_convergence.py` (convergence en dt, voisinage en φ₅); sorties `sortie_width_scan.txt`, `sortie_autres_composantes.txt`, `sortie_delta_check.txt`, `sortie_delta_convergence.txt` ;
- zéro intérieur de V₀ : `zero_V0_lib.py` (DOP853 + événement exact, `refine_episode`, distance signée, `construct_zero_ang`), `verif_zero_interieur_V0.py` (+ `sortie_zero_interieur_V0.txt`), `verif_zero_pente_log.py` (+ `sortie_zero_pente_log.txt`, `sortie_zero_distance.txt` avec `--dist`) ;
- perturbation γ₁/λ (noyau complet) : `finger_perturbation.py` (un paramètre caché, pentes en ε), `finger_perturbation_ball.py` (boule de τ⁰∈ℝ^{12}, dépendance en δ), `finger_perturbation_depth.py` (profondeur jusqu'au rang 8, mot le plus peuplé), `verif_hypotheses_theoreme.py`, `verif_seuil_grille_fine.py`, `verif_regularite_C2.py`, `verif_nonannulation_normes.py`, `verif_temps_impact_C2.py` (+ `sortie_temps_impact_C2.txt`, `sortie_temps_impact_C2_dt.txt`); sorties `sortie_perturbation.txt`, `sortie_perturbation_ball.txt`, `sortie_perturbation_depth.txt` (+ `.json`); `verif_hypotheses_theoreme.py` (hypothèses du Th. 1 et test marge/|h|), sorties `sortie_verif_hypotheses.txt` (δ=0,03), `sortie_verif_hypotheses_delta003.txt`; texte `stabilite_perturbative_mot_fixe.tex/.pdf`.

**Figures** : `partition_Fy_N6_*.png`, `partition_Fy_N9_*.png`, `contour_active_*.png`, `R0_*.png`, `margin7_signe_x_xp.png`, `opacity_*.png`, planches du manuscrit (`planche_I_sillon.pdf`, `planche_II_reste.pdf`, `planche_III_question.pdf`, `figure_*`). Les figures `partition_Fy_N9_4branches_zoom_k5.png` pour {1,4,6},{2,4,6} reflètent une version antérieure à la correction du rééchantillonnage (tableaux de §5.2 font foi).

**Leçons méthodologiques à retenir** (non spécifiques à un résultat) : (1) ✓ témoin / ✗ preuve seulement si obstruction analytique; (2) distinguer 𝒰_j et 𝒰̂_j; (3) préciser la résolution de tout compte de 𝒫_k; (4) vérifier que le protocole de sonde n'introduit pas une symétrie; (5) résoudre l'instant de Kairos par interpolation; (6) faible sensibilité locale ⇏ défaut de pouvoir séparant; (7) rejouer avec un moteur corrigé avant d'intégrer un chiffre dans le manuscrit; (8) une projection insuffisante force à remettre la variable projetée; (9) un indicateur de perte d'affinité doit être testé là où l'on sait qu'il peut être non nul (boule complète des paramètres cachés), sinon il est aveugle; (10) noter explicitement si un mot testé en profondeur est périodique (la croissance en k n'est alors pas celle de mots génériques); (11) ne jamais écrire une hypothèse de régularité sur l'objet hybride quand seul son prolongement pré-impact est régulier (P2); (12) un écart-type de bruit n'est pas un rayon de boule : les minima d'échantillon ne certifient pas des hypothèses uniformes; (13) avant d'attribuer un facteur à un effet (courbure), contrôler d'abord la résolution de la grille de seuil (borne inférieure prev/pred); (14) un écart sur des différences secondes de temps d'événements peut être une erreur d'interpolation O(dt) : rejouer à dt/2 avant toute explication structurelle; (15) distinguer ce qui dépend de la taille de boule (traces τ) de ce qui n'en dépend pas (normes de H,V, ϑ-indépendantes à ε=0); (16) à un événement, distinguer la dérivée à temps fixé (X^{fix}) de la dérivée totale (X^{tot}=X^{fix}+ĝ⁻D_xT) avant d'écrire une formule de saltation; (17) ne pas appliquer un lemme de flot lisse à un état initial situé sur le lieu singulier du champ (H=V=0 pour les normes): construire le premier épisode séparément; (18) un point anguleux (norme près de zéro) enjambé par un intégrateur adaptatif fabrique un bruit qui **imite exactement le signal recherché** (divergence quand δ→0) : toujours rejouer à plusieurs tolérances et, mieux, couper l'intégration au point singulier; (19) construire un zéro par recherche de racine d'une distance signée, pas par minimisation; (21) un lemme d'analyse locale s'écrit et se vérifie *sans* le système (jouet C^∞, quadrature adaptative) avant d'être appliqué au système; (20) un test de nécessité doit comporter un cas symétrique (où la théorie prévoit l'absence d'effet) *et* un cas non symétrique, avec une prédiction sans paramètre libre comparée à la mesure.

---

## 10. Esquisse Lean (état V5.3.2 ; noyau de la formalisation inchangé)

Les deux propositions de §5.1 (obstruction orbitale; invariance d'un lieu fixe), le lemme d'identifiabilité (§3.2), la complétude de ∼_N (§4.2) et la forme affine (§5.4) ne sont **pas encore portés** ici; `NerodeEquiv` est la prochaine cible naturelle, suivie du lemme combinatoire de sélection équivariante (énoncé élémentaire de combinatoire finie).

```
structure HybridCore where
  X : Type*
  C D : Set X                -- C flot, D saut ; C ∩ D = frontière, saut prioritaire
  F : ...                    -- générateur continu, défini au voisinage de C
  K : D → X                  -- saut ponctuel (granularité G₀)
  exec : ...                 -- priorité au premier contact, départage déterministe
  h1_exist_unique : ...
  h2_det_simultane : ...     -- inclut le départage par indice
  h3_priorite_saut : ...
  h4_nonZeno : ...
  h_adm_invariant :          -- invariance d'admissibilité (encadré du socle)
    ∀ x₀ ∈ C, ∀ H ∈ Madm x₀, ∀ t j, γ x₀ H t j ∈ C

-- La lecture ρ_X n'est plus un champ de HybridCore : donnée d'une Présentation, distincte de S.
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
  -- C0 : porté par HybridCore ; C1 : porté par h_pis_const_flot
  h_C23pot :                                     -- témoin de H_ρ^{s,ord,max}
    ∃ x₀ H₁ H₂ H', divergence_ordinale (mot P x₀ H₁) (mot P x₀ H₂) ∧
      RepMax P (mot_k 1) ≠ RepMax P (mot_k 2)     -- à la première position de divergence
  -- C4 : fait définitionnel — aucun champ objectif/récompense/cible

def NerodeEquiv (P : Presentation S) (x x' : S.X) : Prop :=
  P.ρ_X x = P.ρ_X x' ∧
  ∃ (h : Madm x = Madm x'), responseInterne P x = responseInterne P x' ∘ (cast h)
```

Les morphismes structurels (f, ψ_s, ψ_int bijectifs) restent à écrire (ils suivent la définition du .tex); ils n'ont pas encore été portés faute d'un besoin de preuve qui les exige — cohérent avec la méthode « ne rien ajouter tant qu'un défaut précis ne l'exige pas ».


### Relecture du lemme V (P2, v7) — bilan
Relecture complète (lemmes coef, W1–W3, étapes 0–3, E1–E5, thm aff) : aucune erreur logique trouvée ; le lemme reste « à relire » jusqu'à validation de Benoit. Points de dépendance explicités : (1) W1 suppose ‖H_i‖,‖V_i‖ ≥ c_* sur tout l'épisode (hyp. N aux rangs ≥ 2) ; (2) constantes a,b,c dépendantes de r (produit sur les épisodes), uniformité en r non acquise ; (3) a_h = O(ε) du lemme logarithmique repose sur ce lemme V. Ajout d'un tableau « trois régimes locaux » au bilan de la note P2.

### Statut après validation de Benoit (P2 v8, lemme v4)
Lemme V, transmission C² et théorème d'affinité passent de « à relire » à « démontré sous les hypothèses énoncées, à profondeur finie » (mot régulier, déclencheurs forcés, u∈C¹, non-annulation de la référence et des traces ; résultat suffisant, pas une caractérisation). Ajout à l'étape 0 : Y_V = O(εs), Y_H = O(εs²) (forçage O(εs) car ∂_τG_V, ∂²_ττG_V ∝ ‖V‖,‖H‖ ; borne non optimale). a_h = O(ε) au zéro de rang 7 : lemme V jusqu'au rang 6, puis équations régulières de (H,V,τ) au rang 7 ; le lemme V n'est pas appliqué à travers le zéro. Décision : ne plus rouvrir P2 sauf objection nouvelle. Deux soustractions possibles ensuite : non-annulation (condition géométrique fine) ou profondeur (produits de matrices de saltation).

### Cas a_k = 0 hors colinéarité : classement par l'ordre (ordre_deplacement_transverse.tex, 3 p.)
Exemple de Benoit W=(s,δ²) : F(δ)=Φ(δ²), Φ(a)=√(1+a²)+a²·arsinh(1/|a|)=1+a²ln(2/|a|)+a²/2+O(a⁴) ; vérifié à 40 chiffres (formule = quadrature ; reste = δ⁸/8). F∈C³∖C⁴ (F⁗~48 ln(1/δ), mesuré 149,7 ; 260,2 ; 370,7). Proposition de composition F=Φ∘a : (ii) a s'annule avec Da≠0 ⇒ pas C² ; (iii) Da=0 sur Z et |Da|²ln(1/|a|)→0 aux zéros (L) ⇒ C² ; (iv) a de signe constant ⇒ (L) (inégalité |Da|²≤2L|a|). Un paramètre : a=cδ^m, m=1 log (lemme), m≥2 F∈C^{2m−1}∖C^{2m}. Plusieurs paramètres : a=ϑ₁²−ϑ₂² est C² en 0 (D²F(0)=0) mais pas sur la boule (F'' croît de ≈1,66 par décade, prédit 1,658). Précision de Benoit retenue : 𝒬 borné ⇒ hessienne bornée, mais C² exige le prolongement continu (𝒬→0 sur {d_k=0}). Ouvert : réduction (R) du noyau plan au modèle (forme normale ‖W‖²=A(s−σ)²+a², reste C² uniforme).
**Profondeur (nuances de Benoit, non traité).** (1) La sensibilité pertinente est ‖P⊥_V D_ϑV‖²/‖V‖ (hessienne de la norme), pas 1/‖V‖ seul : une vitesse qui décroît géométriquement peut avoir une sensibilité transverse qui décroît plus vite ; cas extrême = symétrie. (2) Matrice de saltation S_j=R_j+(f⁺−R_j f⁻)nᵀ/(nᵀf⁻), n=e_{P_{i_j}} : un produit de S_j borné n'implique pas M_r borné (forçages quadratiques et saltations du second ordre) ; réciproquement un majorant qui explose ne prouve pas que M_r explose. Programme : mesurer les gains effectivement transmis dans les directions cachées, les comparer au quotient transverse ; un résultat négatif exigerait une famille de mots réguliers de profondeur croissante avec sensibilité réelle non bornée. Formulation retenue : uniformité suspecte, non tranchée (amplification / compensation par dissipation / perte de robustesse du mot).

### Note « ordre du déplacement transverse » v2 — caractérisation exacte (suite de la relecture de Benoit)
Dans le modèle réduit F=Φ∘a, a∈C²(U) : **F∈C²(U) ⇔ Da=0 sur Z={a=0}**. Clef (observation de Benoit) : lemme de Glaeser local — si |Da(x)|²>2L|a(x)| (L≥‖D²a‖ sur B̄(x,|Da|/L)), la marche x−sgn(a)Da/L·t coupe Z en un point z avec Da(z)≠0 (ψ'(t_z) ≤ −√(|Da|²−2L|a|) <0, transversalité stricte) ; donc Da=0 sur Z ⇒ |Da|²≤2L|a| localement ⇒ (L) automatique. Contrôle numérique de l'inégalité (x³ : rapport 0,75 ≤ 1 ; ϑ₁²−ϑ₂² : rapport non borné). Corrections intégrées : (a) signe constant n'est pas le seul cas (a=δ³ change de signe, Φ(δ³)∈C⁵∖C⁶) ; la lecture retenue est « lieu des zéros entièrement critique pour a » ; (b) m=1 : non-C² avec a∈C¹, a'(0)≠0 (argument F' lipschitz), l'équivalent F''~2a'(0)²ln(1/|δ|) exige a∈C² (contre-exemple δ+δ³sin(1/δ)) ; (c) m≥2 : C² obtenu par la caractérisation, non par une borne |a'|=O(δ^{m−1}) ; (d) reste du développement de F(δ)=Φ(δ²) : δ⁸/8−δ¹²/32+O(δ¹⁶) (vérifié) ; (e) 𝒬 localement borné ⇒ pas de zéro régulier ⇒ C² dans ce modèle. Prochaine étape : (R), lemme de Morse à paramètres avec poids et jacobien (σ(ϑ) par TFI, ∂²_s‖W‖²=2‖∂_sW‖²>0), conditions de régularité de W et de g.

### Réduction (R) à régularité renforcée — théorème R (ordre_deplacement_transverse.tex v3, 5 p.)
Piste de Benoit formalisée. Plan (d=2), W∈C⁵(J×U;ℝ²), g∈C², zéros simples, g(s_k)>0 : f=‖W‖², σ∈C⁴ (TFI), a=det(∂_sW,W)/‖∂_sW‖ au minimum (∈C⁴, a²=f(σ)), f=a²+(s−σ)²A, ξ=(s−σ)√A∈C³ ⇒ ‖W‖²=ξ²+a² exactement ; S=ξ⁻¹∈C³, poids h=g(S)∂_ξS∈C² (décompte de régularité : 5 = 2+3). Lemme poids : R=∫(h−h(0,ϑ))√(ξ²+a²)dξ∈C² SANS condition sur Da, car |r|≤C|ξ| compense ∂_a²√(ξ²+a²)=ξ²/φ³≤1/|ξ|. Théorème R : F=G+Σ b_kΦ_η(a_k), G∈C², b_k=g(σ)/√(½∂²_sf(σ))>0 ∈C² ; F∈C² ⇔ Da_k=0 sur {a_k=0} pour tout k (suffisance par thm carac + Φ_η=η²Φ(a/η) ; nécessité par Φ''≥0 : parties singulières semi-définies positives, pas de compensation entre zéros ; ensemble dense O où chaque terme est C²). Témoins (verif_reduction_poids.py, 30 chiffres, g=1+s/2) : A a~ϑ : pente de F'' par décade 4,61–4,63–4,73 vs 4,605 prédit ; B a~0,913ϑ² : F''→0,5366 (C²) ; C a=ϑ²−0,01, zéro régulier en 0,1 : pentes 0,170–0,182 vs 0,184 prédit. Application noyau : W=V₀ (d=2), C⁵ si (N) aux rangs<r et u constant (référence) ou u∈C⁴ ; temps terminal t traité comme paramètre indépendant (poids κ₂e^{−κ₃(t−s)}), a=a(ϑ) indépendant de t, donc pas de circularité ; ∂_tP̃≥ν/4 ⇒ T_r∈C². Ouvert : u∈C¹ seul (consomme C⁵), zéros multiples, d≥3, plusieurs Kairos (transmission), zéros de ‖H‖, nœuds non forcés. Retouche Glaeser : si a(x)=0, z=x.

### Raccords de l'application IWS (ordre_deplacement_transverse.tex v4, 6 p.)
Raccord 1 : théorème R reformulé avec poids paramétrique g∈C²(J×U) et bornes mobiles α,β∈C²(U) (fenêtres fixes autour des zéros intérieurs, morceaux restants réguliers car ‖W‖>0 ; positivité g(s_k,ϑ₀)>0 ; pas de zéro aux bords). Raccord 2 : proposition C⁵ autonome — (a) le sous-système (H,V,τ) n'a pas de norme de H,V ; u entre additivement : ω=z−BU(t), U=∫u, champ C⁵ conjoint ⇒ flot C⁵ en (t,s,ξ) ; pressions par Duhamel, C⁵ là où (N) tient ; (b) T_j∈C⁵ par TFI ; (c) ζ⁺_j=R_jζ⁻_j∈C⁵ ; (d) premier épisode au repos : V_i=s·v_i, H_i=s²·h_i avec v_i=∫₀¹V̇_i(θs)dθ∈C⁵, ce qui coûte UNE dérivée de plus sur u : u constant ou u∈C⁵ (et non C⁴). Pour r=1, W=v₀ et poids s·κ₂e^{−κ₃(t−s)}. Trois niveaux : modèle Φ∘a (démontré), intégrale plane pondérée W∈C⁵ (démontré), noyau u∈C¹ (ouvert). Résultat conceptuel retenu pour le Volume II : en dimension deux, zéros temporels simples et poids positifs, la régularité C² intégrée est caractérisée par la géométrie du lieu des zéros dans l'espace des paramètres (lieu critique pour a), pas par la présence de zéros. Prochain travail : baisse de régularité (W∈C⁵ → régularité réelle de u∈C¹).

### Piste B : projection tangentielle fixe (ordre_deplacement_transverse.tex v5, 8 p.)
Idée de Benoit : e=∂_sW(s₀,ϑ₀)/‖·‖ fixe, q=⟨e,W⟩, p=⟨n,W⟩ ; σ(ϑ) (q(σ,ϑ)=0) et a(ϑ)=p(σ,ϑ) sont C² dès que W∈C² (TFI, composition) ; minoration c√(τ²+a²) ≤ ‖W‖ ≤ C√(τ²+a²) démontrée (Taylor, q=τm, m≥m₀ ; p=a+τν, |ν|≤ε<m₀). Apport nouveau : décomposition ρ=|q|+p²/(ρ+|q|) ⇒ F=F_∥+H, F_∥=∫g|q| est C² par le lemme symétrique multi-paramètres (aucun coût), donc F∈C² ⇔ H∈C² : toute la singularité est dans H. Nécessité (⇒ Da=0 sur Z) acquise à W∈C², g∈C¹ via le lemme logarithmique (composante ⊥ au tangent = cosφ·Da·h). Reste la suffisance à basse régularité (conjecture, plan en 4 étapes : D²H hors de Z ; découpe |τ|≤ε + Glaeser ; dérivabilité de DH en Z quand Z est épais ; inclinaison φ(ϑ)≠0). Explication du coût de la voie de Morse : b=g(σ)/√(½∂²_sf(σ)) compose ∂_sW avec σ(ϑ) ⇒ ∂³_sW pour deux dérivations ; avec u∈C¹, W n'est que C² en s tandis que D^b_ϑW (b≥1) est C³ en s (u additif, disparaît des équations variationnelles). Exemple colinéaire q=w(s)−ϑ, w∈C¹ : F''=2g(σ)/w'(σ) continue. Test numérique (verif_projection_fixe.py, 30 chiffres) : F_∥''→0,18000=2g(∂_ϑq)²/q_s dans 4 cas ; H'' porte seule le log en A, A' (pente ≈4,6/décade) et converge en B (0,3566), B' (0,3617) ; variantes A', B' avec ½|s|^{5/2} (C² exactement en s au zéro mobile) se comportent comme les lisses. Aucun résultat établi sur la suffisance à basse régularité à ce stade.

## V6 de la note « ordre du déplacement transverse » — projection fixe, coordonnées τ=s−σ(ϑ), suffisance à W∈C²

Statut : démonstration PROPOSÉE (théorème S), à relire par Benoit ; non encore validée.

- Poids paramétrique : il faut g∈C² conjointement pour la suffisance ; contre-exemple de Benoit g=1/Φ(ϑ), W=(s,ϑ) : F≡1 (C²) alors que Da(0)≠0 ; Φ''~2 ln(1/|ϑ|). Pour la nécessité, g∈C¹ en s, C² en ϑ suffit (différence seconde : g₀[N(δ)+N(−δ)−2N(0)] + δg₁[N(δ)−N(−δ)] + O(δ²)).
- Hessienne de F_∥ corrigée : D²F_∥=∫sgn(q)[gD²q+2Dg⊗_sDq+qD²g]ds+Σ2g DqDq/|q_s|.
- Borne grossière ‖D²H‖≤C(1+‖D_ϑp‖²/ρ) abandonnée (exemple W=(s−ϑ)(cosϑ,sinϑ) : F=1+ϑ², F_∥=cosϑ(1+ϑ²), H=(1−cosϑ)(1+ϑ²), tous analytiques).
- Coordonnées τ=s−σ(ϑ) : W̃(τ,ϑ)=W(σ+τ,ϑ)∈C² (pas de ∂_s³W). W̃=(τm̃, a+τν̃), m̃,ν̃∈C¹. ‖P⊥DW̃‖²/ρ=τ²N²/ρ³, N=m̃Da−aDm̃+τ(m̃Dν̃−ν̃Dm̃). Terme T₁=g τ²m̃²(Da·h)²/ρ³ : ∫T₁≤C|Da|²(1+ln⁺(1/|a|)) →0 près de Z par Glaeser (|Da|²≤2L|a|) et ≡0 sur Z ; tous les autres termes bornés et continus ponctuellement ⇒ DF_in dérivable, D²F_in continue.
- Corollaire : sous (P₂), g∈C² : F∈C² ⇔ Da_k=0 sur Z_k ; aucune forme de Morse.
- Noyau u∈C¹ : fenêtres s_k>0 avec W=V_0 ; s=0 via factorisation P2 ; transmission = Prop T de P2 ; t paramètre indépendant. Anisotropie limitée à b=1,2.
- Numérique : verif_coordonnees_tau.py / sortie_coordonnees_tau.txt (formule en τ = différences finies : écart ≤2,4e-11 en B, ≤1,7e-5 en A à ϑ=1e-4 [bruit]).
- Ouvert : zéros multiples/dégénérés, d≥3, plusieurs Kairos, zéros de ‖H‖, nœuds non forcés, uniformité en profondeur.

### V6.1 — relecture de Benoit : théorème S validé
- Preuve de suffisance jugée correcte (aucune faille logique). Deux précisions rédactionnelles intégrées : (P₂) complétée par α,β∈C²(U), [α,β]⊂J, ‖W‖>0 aux bornes uniformément ; convergence uniforme locale de ∫T₁ près de Z explicitée.
- Statut : Théorème S et corollaire (caractérisation nécessaire et suffisante dans le plan, W∈C², g∈C², zéros simples) = démontré, relu. Prochaine relecture : raccord avec le noyau (autres contributions C², terme ‖H_i‖, données transmises, t paramètre, borne quantitative M_rε en présence de zéros = ouvert).

### V6.2 — retouches de Benoit
- Lemme de décomposition : termes de bord de Leibniz ajoutés (bornes mobiles α,β∈C², C⁰, sans effet sur la singularité intérieure).
- Statuts harmonisés : plan pondéré W∈C² = démontré (thm S) ; noyau IWS u∈C¹ = raccord à relire. Deux questions IWS distinctes : (1) transport aux temps de Kairos avec u∈C¹ ; (2) estimation quantitative O(ε) du défaut d'affinité (C² à ε fixé ⇏ hessienne uniformément O(ε)). Note abstraite considérée comme terminée.

## Complément « transmission C² épisode par épisode » (octobre 2026) — proposé, à relire
- Piste de Benoit : enchaîner théorème S et transmission P2 sans repasser par Morse. Les (H,V,τ) n'ont ni norme ni P ; P = fonctionnelle intégrale du flot ; pas besoin du flot étendu de P2 (lemme W) sur un épisode à zéros.
- Condition (Z2) = critique : D_ϑW h ∥ ∂_sW aux zéros (forme intrinsèque de D_ϑ a=0). Vraie hypothèse, non conséquence (à ε=0 a₀≡0 trivial ; à ε>0 elle ne suit pas de Da=O(ε)). Elle doit couvrir tous les nœuds de I_j (pressions transmises), ‖H_i‖ et ‖V_i‖.
- Théorème T (étapes A/B) : T_1..T_r∈C² avec u∈C¹. Remarque : a_k seulement C² suffit grâce à S (Morse aurait exigé T_j∈C⁴).
- Étape C : lemme de Glaeser avec marge δ₀ fixe : |Da|² ≤ 2L|a| + (2/δ₀)|Da||a| (dichotomie ρ≤δ₀ / ρ>δ₀). ⇒ |Da|²(1+ln⁺1/|a|) ≤ C ε. Sans marge : zéro non critique à distance d=exp(−1/ε²) hors de U' ⇒ quotient ~1/ε. Témoin : verif_glaeser_marge.py (60 fonctions, ratio ≤0,99 ; 1re version avec min de grille donnait des ratios >1 = artefact : fonction à zéros non critiques).
- Non fermé : (E) à chaque rang (propagation D z⁺, D² z⁺ = O(ε) avec saltation), simplicité uniforme, profondeur, défaut d'affinité O(εδ²) non annoncé.

### Complément transmission C² — V2 après relecture de Benoit
- Prop Q corrigée : seuls ‖D²_{ϑϑ}F‖, ‖D²_{tϑ}F‖ sont O(ε) ; |∂_ttF|≤C (contre-exemple W≡(1,0), F=κ(1−e^{−κ₃t})/κ₃). ∂_tt n'intervient que × DT⊗DT=O(ε²).
- Théorème T : (Z0) nœuds de I_1 forcés ; (Z1) au 1er épisode sur [s_*,T_1] (factorisation sur [0,s_*]) ; conclusion limitée aux pressions de I_j ; prolongement virtuel pré-impact explicité ; I_j={i_j..i_r} si resets de pression diagonaux.
- ERREUR de ma part corrigée : j'avais écrit D z_j^+ = O(ε) pour l'état complet ; faux pour τ (D_ϑτ_0=e^{−βt}I). Récurrence par blocs : 𝒜_j (H,V : D, D² = O(ε)), 𝒜^τ_j (Dτ=O(1), D²τ=O(ε)), ℬ_j (pressions utiles O(ε)), 𝒞_j (T_j : D, D² = O(ε)). Flèches (a)→(d) acycliques ; hypothèses (D),(U),(R) posées non redémontrées ; (R) = resets ne transmettent pas O(1) de τ vers (H,V), à contrôler contre P2.
- Lemme de Glaeser avec marge : statut démontré (relu).

### Complément transmission C² — V3 (relecture de Benoit, 3 points)
- A : ligne explicite D_ϑm̃=∫(D_ϑ∂_sq+∂_s²q D_ϑσ)dλ=O(ε) ⇒ |E'|≤Cερ. B : conclusions en t seulement sur le voisinage terminal de l'impact (‖W(t)‖≥c₀). C : persistance du mot par continuité des pressions hors I_j (marges strictes), pas besoin de C².
- (R) vérifiée sur P2 (R_j diagonal : V_{i_j}→r_V V_{i_j}, P_{i_j}→r_P P_{i_j}, identité ailleurs, dont τ et H).
- Corollaire : défaut d'affinité ≤ ½C_jε‖h‖² (Taylor reste intégral, boule convexe), conditionnel à la prop. R.
- Travail restant dans (U) : (U1) flot/compacité ; (U2) simplicité/séparation uniformes (branches de zéros, à partir de zéros simples de W₀) ; (U3) criticité à marge fixe = vraie hypothèse géométrique.

### Complément transmission C² — V4 : (U2) déchargée, raffinement logarithmique
- Lemme de persistance uniforme des fenêtres (U2) : sous convergence C¹ uniforme vers W₀ à zéros simples, fenêtres I_k, e_k fixe, ∂_s q≥m₀, unique branche σ_{ε,k}, encadrement c√(τ²+a²)≤‖W‖≤C√(τ²+a²), ‖W‖≥μ₀ hors fenêtres ; ne présuppose aucun zéro vectoriel (ce sont les branches σ qui persistent ; zéros vectoriels ssi a_{ε,k}=0). Avec taux Cε : |σ−s_k|+|a|≤C'ε.
- (U1) : compacité ET persistance du mot (marges strictes, traces non nulles, bornes de temps) ; (U3) : hypothèse structurelle, non déduite du noyau.
- Raffinement (conditionnel à U3) : b=a/ε ⇒ ‖Db‖²≤C|b| (Glaeser avec marge) ⇒ ‖Da‖²(1+ln⁺1/|a|)=O(ε²(1+|ln ε|)) ; T₁ négligeable devant O(ε), conclusion de Q inchangée. Aucun test numérique spécifique (calcul analytique).

### Complément transmission C² — V5 (corrections de Benoit)
- (R) : D_τR_j^{(H,V)}=0 vaut même pour r_V=0 ; mais ‖V⁺‖=r_V‖V⁻‖>0 FAUX si r_V=0 (le noyau autorise r_V∈[0,1)) : (Z1) peut exclure la configuration, démarrage post-Kairos à analyser séparément. (Ma phrase précédente "‖V⁺‖=r_V‖V⁻‖>0" reprise de P2 était trop forte.)
- Lemme U2 : la constante C de l'encadrement dépend aussi de sup‖∂_sW₀‖.
- T₁=O(ε²|ln ε|)=o(ε) ; formulation prudente : ne détermine pas l'ordre O(ε) de la majoration générale. Netteté : a_ε=ε(1+ϑ) ⇒ F''(0)=2ε²ln(1/ε)+O(ε²) (limite (F''−2ε²ln(1/ε))/ε²→2ln2−2=−0,6137). Script verif_exemple_log_eps.py.
- (U3) = véritable objet de recherche.

## Criticité transverse : classes structurelles (note `criticite_transverse_classes`, 4 p.)
Question de Benoit : (U3) est-elle structurelle dans certaines classes du noyau ?
- Critère au 1er ordre : a_ε = εA(ϑ)+O(ε²). A≠0 ⇒ (U3) vide ; A=0, DA≠0 ⇒ zéro régulier, (U3) échoue ; contact 1er ordre insuffisant (a=εϑ²−ε² : zéros ±√ε).
- **Classe isotrope** (λ=0, γ₁ quelconque, forçage et (H,V)(0) sur un axe de coordonnée, traces ϑ quelconques non nulles) : le sous-espace E={H,V∈Re} est invariant (M_λ=I, friction scalaire, Ã sur l'indice de nœud, tanh(0)=0, Kairos/graphe ne voient que normes et traces) ⇒ a≡0, (U3) triviale. Démontré ; témoin : composante n = 0.0 sur 8 tirages.
- **Classe anisotrope** (λ>0) : réflexion R (n→−n) équivariance ⇒ a_ε impaire, nulle sur Fix(R). Réponse transverse linéaire (eq. T) ; DA(p)≠0 numériquement (nœud 0 : 0,3707 noyau, 0,3699 formule linéaire indépendante, 0,2 %). Donc (U3) échoue au voisinage de Fix(R), sous (N) : DA≠0. Contact a≥0 impossible près de p (impaire).
- T_2∉C² : seulement esquissé (inversion de P(T,ϑ)=θ). Témoin : D²T_2 borné (0,2511) pour λ=0 ; divergence log pour λ>0 ; pente mesurée −1,47…−1,83e-2/décade (bruit à δ petit : −2,57e-2) vs prédite −1,742e-2 ; coïncidence à 5 chiffres sur une seule tranche, à ne pas sur-lire.
- Réserves : point axial = mur du mot (ties de cosinus, étiquette fixée par l'arrondi ; nœuds 1 et 5 changent le mot, comparaison invalide) ; τ(0)=0 pollue D²T (‖τ‖ non lisse) ⇒ base 0,6·e ; persistance du mot près de Fix(R) non vérifiée ; contact : aucun mécanisme structurel trouvé (R rend a impaire, positivité = coïncidence codim 1).
- Dichotomie suggérée par Benoit : théorème positif en classe isotrope / négatif dès que λ>0 (anisotropie historique) — établi sous (N) et esquissé pour T_j, pas encore théorème général.
- Scripts : crit_lib.py, verif_criticite_classes.py, verif_reponse_transverse_formule.py (+ sorties).

### Criticité transverse V2 (retour de Benoit : normalisation, branche régulière, contre-exemple sans mot)
- Corrections : eq. (T) réécrite pour X_H=∂_εH^n, X_V=∂_εV^n (sans facteur ε) ; énoncé « sur une branche régulière fixée » (graphe et mot constants sur un ouvert de traces) ; « codimension un » remplacé par « condition de dégénérescence supplémentaire, non imposée par la symétrie ».
- **Contre-exemple sans mot (§ premier épisode)** : zéro de V_0^x avant le premier Kairos ⇒ graphe fixe, flot analytique, aucune similarité cosinus. Protocole : constantes du manuscrit sauf **Θ=2,2** (avec Θ=1,25 : T_1=2,38, pas de zéro avant l'impact ; il faut Θ≳2,0). s*=3,7013, T_1=4,4552, marge 0,754, i*=0, un seul zéro, ‖H_0‖≥0,118.
- Réponse transverse (tous nœuds valides) : nœud 0 : 0,4945 (noyau, λ̄ seul) vs 0,49547 (formule linéaire), 0,21 % ; autres nœuds à 1,6–2,8 % ; ‖DA(p)‖=0,489 ; γ̄ seul : 0 ; perturbation axiale aléatoire : a=0 ; additivité sur direction aléatoire : 2,60620e-4 vs 2,60605e-4.
- D²P_0(t=4) : pentes +6,8544e-3, +6,8698e-3 par décade vs +6,8714e-3 prédit ; D²T_1 (T_1 par racine de P_0=Θ) : −2,3824e-2, −2,3867e-2 vs −2,3872e-2 prédit ; λ=0 : bornés (−0,144538 ; 1,423247).
- **La dérive observée en épisode 2 était un artefact de localisation d'événement solve_ivp** (même dérive en épisode 1 par événement, absente par racine). Épisode 2 non refait par racine.
- Statut : P_0(t;·)∉C² sous (N) seul (Prop nec2) ; T_1∉C² esquissé ; (N) évaluée par deux calculs indépendants, non certifiée ; ne dit rien sur Θ=1,25 (pas de zéro en épisode 1) ; Θ comme choix de protocole à cadrer.
- Script : verif_premier_episode.py (+ sortie_premier_episode.txt), calcul ~3 min (lancer en arrière-plan).

### Criticité transverse V3 : (N) certifiée, coefficient à ε fixé, T_1 démontré (retour de Benoit)
- Précisions de Benoit intégrées : (1) c_ε(t)=2κ2 e^{-κ3(t−s*^ε)}/|∂_sV^x_{0,ε}(s*^ε,p)|·(Da_ε·h)² avec s*^ε=σ_ε(p) (perturbé), pas s*^0 ; (2) domaine [t1,t2] compact dans ]s*^0,T_1^0[ (+ prolongation virtuelle du flot au-delà de l'impact) ; factorisations V_0=s·ṽ_0, H_0=s²·h̃_0 pour traiter s=0 (ṽ_0≥0,993, h̃_0≥0,497) ; (3) inversion vers T_1 écrite : Δ=−c_ε/(2∂_tP_0)δ² ln(1/δ)+O(δ²), reste d'inversion δ⁴ln²(1/δ) (pas O(δ⁴)) → T_1(δ)+T_1(−δ)−2T_1(0)=−c_ε/∂_tP_0·δ²ln(1/δ)+O(δ²).
- **Certification (N)** `certif_N_premier_episode.py` (python-flint 0.9.0 / Arb, Taylor validé ordre 22, pas 1/20, 200 bits, <1 s) : X_{V,0}(s*^0)=0,495473971795 ± 2,1e-13 (λ̄=1) ; s*^0=3,70133761238468 ± 3e-15 unique, simple, v_s=−0,5578391252 ± 4e-11 ; τ_i^x≥0,46 ; ṽ_0≥0,993 ; h̃_0≥0,497 ; h_0≥0,117 sur [0,5;4,6] ; P_i≤2,131<Θ sur [0,4] ; P_i≤0,74 (i≥1) ; g−κ3Θ≥0,214 sur [4;4,6] ; P_0(4,45)<Θ<P_0(4,50) ⇒ T_1^0∈]4,45;4,50[, déclencheur nœud 0 seul.
- Recoupements : solve_ivp à 1e-9 (h_0,v_0,τ_0,P_0,P_1 à t=1..4) ; Richardson noyau ε→0 : 0,49547385 (ordre 2) vs 0,49547397 certifié (2e-7 relatif).
- Statut : théorème du premier épisode (perte de C² de P_0(t;·) et de T_1) = **démontré, assisté par ordinateur**, pour le protocole Π (Θ=11/5, traces 3/5·e, constantes du manuscrit). Correct si code + Arb le sont (non vérifié formellement). Ne dit rien sur Θ=1,25 ni sur les épisodes ≥2 (mot) ; profondeur laissée de côté.
- Piège corrigé : dans le calcul de P par série de Taylor, ne pas mettre P(0) dans la série (dépendance → rayon ×e^{κ3 h}/pas) ; utiliser P=e^{-κ3τ}(P0+Φ(τ)).

### Criticité transverse V4 : retouches de Benoit (pression initiale, analyticité, H_0, certificat)
- **Pression initiale explicite dans Π** : P_0(0)=r_PΘ=77/100, P_i(0)=0 (i≥1). Elle ne change pas s* ni les données transverses, mais fixe T_1 : 4,455195 (P_0(0)=77/100) vs 4,812400 (P_0(0)=0), vérifié. Formule de Duhamel : P_0(t;ϑ)=P_0(0)e^{-κ3 t}+ intégrales ; terme indépendant de ϑ, sans effet sur le coefficient log.
- **Analyticité** réservée au sous-système (H,V,τ) ; la pression prolongée est continue (dérivable en ϑ) mais pas C² au zéro transverse.
- **H_0 entre 1/20 et 1/2** : appui sur la borne certifiée h_0≥0,000626 sur [1/20 ; 4,6] (et ≥0,117 sur [1/2 ; 4,6]), la factorisation ne sert que sur [0,1/20].
- **Θ** : paramètre de la famille (Tome I, « Ensemble de flot et ensemble de saut », Θ>0) ; Θ=11/5 appartient à la famille, ≠ protocole numérique de référence 5/4.
- **Certificat reproductible** : toutes les conclusions sont des assertions sur les boules Arb (CHECK lève AssertionError), bornes décimales arrondies vers l'extérieur (0,495473971794 ≤ X_V,0 ≤ 0,495473971795), test négatif (seuil τ≥0,47) fait échouer le script ; conditions initiales affichées en tête de sortie.

### Criticité transverse — note V4 / script V3 (retour de Benoit sur la V3)
- Normalisation de λ̄ : X^{(λ̄)}=λ̄·X^{(1)} (source contenant déjà λ̄) ; DA(p)·e_{0n}=λ̄·X^{(1)}_{V,0}(s*⁰) ; le certificat porte sur X^{(1)} = 0,495473971795 ± 2,1e-13.
- Script V3 : `sign_of` par comparaisons Arb (plus de float) ; mêmes résultats (17 pas grossiers sur 552) ; convention : décisions = comparaisons de boules, float = affichage.
- TeX : « hérité du flottant » reformulé (données = rationnels exacts encadrés par Arb ; décisions par comparaisons Arb ; float = affichage) ; conclusion : « lorsque l'anisotropie intervient ET que (N) est satisfaite » (l'imparité donne le zéro, (N) la régularité).
- Reproductibilité : fichiers versionnés `criticite_transverse_classes_V4.{tex,pdf}`, `certif_N_premier_episode_V3.py`, `sortie_certification_N_V3.txt`, `MANIFEST_certification_V3.txt` (Python 3.11.15, python-flint 0.9.0, SHA-256 dans la note et le manifeste).

### Nettoyage du certificat — script V4 / note V5
- a_priori : test redondant supprimé (newB=x0+[0,h]f(B) ⊆ B est lui-même une enclosure valide par isotonie ; x(t)=x0+∫f ∈ x0+[0,t]f(B) ⊆ newB) ; `if False else` supprimé dans le pas du zéro. Sortie identique octet pour octet (diff vide).
- Fichiers : certif_N_premier_episode_V4.py, sortie_certification_N_V4.txt, MANIFEST_certification_V4.txt, criticite_transverse_classes_V5.{tex,pdf}.

### Profondeur — premières mesures (V1, oct. 2026) — `profondeur_premieres_mesures.pdf`, `verif_profondeur.py`
- Sens retenu de « profondeur » : uniformité en le rang r des impacts (nuance (1) de Benoit : sensibilité pertinente = ‖P⊥_V D_ϑV‖²/‖V‖). Témoins numériques seulement (un point de base, protocole du manuscrit Θ=5/4, d=2, nœud 0 forcé).
- ε=0 : déclencheur = nœud forcé 0 pour les 7 premiers impacts ; le 8e est déclenché par le nœud 1, marge de pression 0,0115 (rang 7 : 0,122). Bascule de ce déclencheur pour γ₁≈3,1·10⁻³ (γ̄=1), ε≈7,1·10⁻³ (γ̄=λ̄=1), pas avant 10⁻² pour λ̄ seul. ‖V₀‖ à l'impact : ÷1,6–1,9 par rang jusqu'au rang 7, puis ∝ e^{-0,115 T} (β=0,12) ; ~10⁻² (rangs 10–30), ~10⁻³ (40–60), minimum intérieur ~10⁻⁴ au rang 48 (pas de zéro exact). Mot stable (12/12 jusqu'au rang 59) pour perturbations gaussiennes de ϑ ≤10⁻³.
- ε>0 (λ̄=1, ε=10⁻³, rangs 1–40) : G_r=max‖D_ϑV‖/ε : 0,68 (r=2), 0,95 (r=4), 0,28 (r=14), 0,025 (r=40) ; Q_r=max|∇(V·n)|²/(ε²‖V‖) : max 4,98 au rang 14 (m_14=0,007), 1,59 au rang 23, 0,04 au rang 40 ; ajustements rangs 15–40 : G~e^{-0,20T}, Q~e^{-0,24T}. γ̄ seul : Q≤0,24 (r≤14). Indépendance en ε : ≤5 % jusqu'au rang 7, 16–44 % aux rangs 8–13 entre ε=10⁻² et 10⁻³ (non expliqué).
- **Correction de ma propre lecture** : sur les rangs ≤14 seuls, Q_r semblait croître comme 1/‖V‖ (0,34 → 5,6) ; poussé au rang 40, c'est un pic lié à une quasi-annulation, puis décroissance. Les obstacles réels sont locaux : murs de déclenchement (marge 0,0115 au rang 8) et quasi-annulations de V₀ (rangs 14, 23, 48).
- Non établi : borne ‖D_ϑV₀‖ ≤ Cε e^{-κT} (propagation par les S_j), deuxième point de base, nœud 1 déclencheur non forcé, ε₀(r) uniforme.

### Profondeur — V2 (relecture de Benoit) — `profondeur_mesures_V2.pdf` (4 p.), `verif_profondeur_V2.py`, `verif_profondeur_propagation.py`, `verif_profondeur_derive_visible.py`, `verif_profondeur_bascule_rang8.py`
- Corrections de la V1 : Q_r ≤ G_r²/m_r (rapport mesuré 0,2–0,6 : le minimum de ‖V₀‖ est à s=0 après le reset, le maximum de Q en fin d'épisode) ; m_r par minimisation bornée, rang 1 non défini (V₀(0)=0) ; décroissance de m_r sur 60 rangs = indication, pas m_r→0 ; persistance du mot jusqu'au rang 59 réellement mesurée (sortie_profondeur_V2_C) ; NS=1200 = NS=300.
- Écart entre ε=10⁻² et 10⁻³ : γ̄=1 → mots différents dès la 8e lettre ((0,{1,4,5}) vs (1,{2,5})), d'où m₉ ×2 (reset r_V) ; λ̄=1 → mêmes 13 lettres, écart dû à la dérive linéaire en ε de la vitesse visible (pente +0,46…+0,76 aux rangs 5–13, identique à 2 % entre les deux ε), pas à une correction non linéaire ni à s_maxQ (sauf rang 14).
- Propagation variationnelle : Φ_r (FD du flot à temps fixe), S_loc=DR(I−f⁻nᵀ/nᵀf⁻) (horloge locale, celle des G_r) et S_glob (Benoit, temps global fixe) ; la chaîne redonne G_r à 10⁻⁴ sur 14 rangs. ∏‖S_locΦ‖ : 3,6 → 6,4·10³ ; K_r=‖Π_V z_r,ϑ‖/ε ≤ 1,05 (pic aux rangs 8–9 : nœud 1, nᵀf⁻=0,227, ‖S_loc‖=8,1).
- Murs : ν'(0)=−∂_εP_j+(Ṗ_j/Ṗ_i)∂_εP_i lu sur la chaîne. Rang 8 (ν=0,0115) : ε_c prédit 3,06·10⁻³ (γ̄) et 7,08·10⁻³ (1,1) contre 3,07·10⁻³ et 7,11·10⁻³ par bissection hybride ; λ̄ : ν'>0, pas de bascule. En profondeur (rangs 1–40, 1er ordre) : seul le rang 8 a ε_c<1 pour γ̄ ; λ̄ min ε_c=0,11 (rang 13) ; recâblage ε_c ≥0,08 ; rayon de chambre en ϑ 4,3·10⁻³ (rang 1), ≥10⁻² ensuite, croît avec la profondeur (0,1–0,2), min 5,6·10⁻² au rang 30.
- Non fait : décomposition tangentielle/transverse de S_loc au rang 8 ; réponse de V₁ aux traces ; second point de base ; bissection hybride aux rangs 12–14 (λ̄) ; borne ‖D_ϑV₀‖ ≤ Cε e^{−κT}.

### Profondeur — V2.1 (relecture de Benoit de la V2) — `profondeur_mesures_V2_1.pdf` (5 p.), `verif_profondeur_saut_rang8.py`
- Corrections : plage de Q_r/(G_r²/m_r) en entier (λ̄, ε=10⁻³, rangs 2–40 : 0,159 au rang 15 → 0,777 au rang 9) ; m₁, G₁²/m₁ et leur rapport « n/a » (V₀(0)=0) ; sorties à ε=0 : K_r et G_chaîne « n/a » (division par ε) ; sorties régénérées (V2_B, V2_B40, V2_NS1200, mur40_gam/lam, mur_both) ; colonne ε écrite explicitement Z⁻_r=Φ_r Z⁺_{r−1}+(∂_εφ_r)e_εᵀ, Z⁺_r=S_loc Z⁻_r ; S_loc = jacobien de la carte d'impact à horloge locale.
- **Rayon de chambre** : les ρ_j^lin sont des distances linéarisées à un mur de rang j ; pour le mot complet ρ_{≤r}=min_{j≤r}ρ_j=4,3·10⁻³ pour tout r≤40 (premier saut), et ce n'est pas un rayon garanti (termes d'ordre supérieur non contrôlés). « Le rayon croît avec la profondeur » retiré.
- Deux questions distinctes : stabilité du mot (murs, ρ) vs stabilité des dérivées (Q_r, K_r, saltations).
- Saut du rang 8 : ‖∂_ϑT‖/ε passe de 0,21 à 1,87 (rang 9 : 1,94, impact quasi simultané, ‖∇P₀‖/ε=2,77) ; part « temps fixe » A et part « décalage » B=DR f⁻dT de la dérivée post-saut de V_k ; nœud 1 : A=0,21, B=0,33, A+B=0,34 (normale 0,19) ; nœud 0 : composante normale 0,107 → 0,161 (×1,5). L'amplification du temps passe peu dans V car V̇₀ est petit (0,04–0,06) ; V̇₁=0,35.
- Nœud 1 : ‖V₁‖≃0,111 t³, ‖H₁‖≃0,0278 t⁴ au départ (ordres t³,t⁴, pas s,s²) ; min ‖V₁‖ ≥0,043 et min ‖H₁‖ ≥0,074 sur les épisodes 2–8 ; franchissement simple (Ṗ₁=0,2265). Hypothèses de régularité de la transmission NON vérifiées.
- Hypothèse candidate (Benoit, non démontrée) : ‖P⊥_{V₀}D_ϑV₀‖ ≤ Cε‖V₀‖^{1/2} sur les portions régulières ; témoin : sup_{r≤40}Q_r=4,98 (λ̄), C≈2,2.
