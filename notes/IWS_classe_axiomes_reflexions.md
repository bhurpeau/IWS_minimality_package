# Classe IWS — axiomes, objets, transformations

*Document compagnon du Volume II. **État courant du .tex : V5.5** — les sections 1 à 3 ci-dessous sont un instantané figé de la relecture faite à l'époque du v4 et n'ont pas été remises à jour depuis (elles portent encore, à dessein, leurs marqueurs [TEX]/[DISC]/[NOUV] d'origine, datés v4) ; plusieurs de leurs points sont depuis résolus ou incorporés dans le .tex (par exemple 3.13, signalé « incorporé en V5.5 » en §4.3) sans que la section elle-même ait été mise à jour en conséquence. Une repasse de consolidation de 1 à 3 contre la V5.5 reste à faire — voir la question ouverte correspondante en §5. Les sections 4 et suivantes sont tenues à jour au fil de l'eau.*

*Marqueurs (tels qu'utilisés dans les sections 1 à 3, datés de l'époque v4 — voir note ci-dessus) :*
- **[TEX]** : décidé et rédigé dans le .tex v4 ;
- **[DISC]** : acquis en discussion, pas encore reporté dans le .tex ;
- **[NOUV]** : point relevé à la relecture du v4.

*Statuts épistémiques : [DEF], [CHOIX], [PROP], [PROP, candidate], [OUVERT].*

---

## 1. Décisions consolidées (état du .tex au moment de la relecture v4 — non remis à jour, voir note en tête de document)

### 1.1 Instance et classe [TEX]

Le noyau du Tome I est une **instance**. La classe 𝔍𝔚𝔖 = {S | S satisfait les propriétés constitutives d'un IWS} doit contenir exactement ce que l'appareil des Tomes I–III exige, pas tout ce que le noyau vérifie.

Principe de minimalité : aucune structure n'est introduite tant qu'une difficulté précise ne l'exige. Règle de travail : objet → obstacle → structure minimale nécessaire.

### 1.2 Socle hybride 𝔥 [TEX]

S = (𝒳, C, F, D, 𝒦), avec quatre hypothèses de régularité :
- **(H1)** structure bien définie ;
- **(H2)** existence et unicité locale du flot ;
- **(H3)** déterminisme de l'exécution, événements simultanés compris ;
- **(H4)** absence de Zénon.

Ces hypothèses ne caractérisent pas un IWS : 𝔍𝔚𝔖 ⊆ 𝔥.

- **Priorité au saut au premier contact avec D** [TEX]. C'est une règle de *sémantique* de Exec. Elle participe à O1/H3 et ne se déduit pas de (C, D, 𝒦) : dans le cadre hybride standard (Goebel–Sanfelice–Teel), flot et saut sont tous deux permis sur C ∩ D.
- **Statut de Exec** [TEX, OUVERT]. Deux présentations restent à tester :
  - S = (𝒳, C, F, D, 𝒦), avec Exec défini extérieurement ;
  - S = (𝒳, C, F, D, 𝒦 ; Exec).

### 1.3 Axiomes constitutifs [TEX]

**I1 — Historicité interne causalement effective (canal continu).** On écrit x = (y, h), où h est une composante historique non décorative, éventuellement composite, et F = (F_y, F_h). L'axiome demande :
$$
\exists\, y_0,\ h_1\neq h_2 :\quad F_y(y_0,h_1)\neq F_y(y_0,h_2).
$$
Aucune fonctionnelle explicite du passé n'est exigée : h peut suivre une loi locale sur l'état augmenté. *(Voir §3.1 : cette formulation dépend de la présentation.)*

**I2 — Restructuration événementielle endogène (canal discret).** Trois exigences :
- il existe une composante s avec ṡ = 0 pendant le flot, et s⁺ ≠ s⁻ possible à un événement ;
- le déclenchement dépend de l'état (x ∈ D), pas d'un calendrier extérieur ;
- la restructuration est causalement effective au-delà de s elle-même :
$$
\exists\, x_1,x_2\in D:\quad \pi_{\neg s}(x_1)=\pi_{\neg s}(x_2),\ \ \pi_s(x_1)\neq\pi_s(x_2),\ \ \pi_{\neg s}\mathcal K(x_1)\neq\pi_{\neg s}\mathcal K(x_2).
$$
Plusieurs composantes peuvent changer au saut. L'extérieur peut contribuer à conduire le système vers D, mais le critère de déclenchement reste porté par l'état. I2 fournit un ordre intrinsèque des transformations, sans durée propre supposée.

**I3 — Absence de telos primitif.** La spécification primitive d'un IWS ne requiert ni état-cible, ni récompense, ni fonction-objectif dont l'optimisation définirait la dynamique ou les restructurations. Deux notions sont distinguées :
- l'**absence de telos primitif**, qui est un axiome de classe ;
- la **non-téléologie comme propriété dynamique**, qui s'étudie sur des réalisations particulières.

Remarque : I3 n'exclut ni des telos locaux, ni un environnement téléologique agissant via u(t), ni une internalisation historique d'une orientation.

### 1.4 Définition minimale [TEX]

S ∈ 𝔍𝔚𝔖 (provisoirement) si S satisfait I1, I2 et I3 sur le socle H1–H4. La définition ne suppose ni graphe, ni métrique, ni dimension particulière, ni forme de mémoire, ni géométrie historique, ni temps propre, ni stratification.

### 1.5 Indépendance de I1 et I2 [TEX]

- **Témoin continu** : ẏ = −y + h, ḣ = y − h, D = ∅. On a F_y(y₀,h₁) − F_y(y₀,h₂) = h₁ − h₂ ≠ 0, donc I1 est vraie. Comme D = ∅, I2 est fausse.
- **Témoin discret** : y ∈ [0,1], s ∈ {0,1}, ẏ = 1, ṡ = 0, D = {y = 1}, 𝒦(1,s) = (f(s), 1−s), avec f(0) = 0 et f(1) = ½. Comme F_y ne dépend pas de s, I1 est fausse. Comme π_y𝒦(1,0) = 0 ≠ ½ = π_y𝒦(1,1), I2 est vraie.

Conclusion : I1 ⇏ I2 et I2 ⇏ I1. I1 porte la causalité historique dans le flot, I2 la causalité structurelle dans le saut. *(Voir §3.1 : l'indépendance tient pour une décomposition déclarée.)*

### 1.6 Transformations : trois constructions présentes [TEX]

- **Morphisme candidat** : une application qui envoie toute exécution admissible de S sur une exécution admissible de T. La structure à préserver en premier est le comportement dynamique, pas la représentation interne.
- **Inclusion dynamique** ι : S_Δ → S. C'est un candidat de morphisme interne, sous réserve que S_Δ satisfasse lui-même les axiomes.
- **Projection d'interface** π_A : S_A → Y, où Y est un espace d'observables. C'est le prototype d'une application d'observation, pas automatiquement un morphisme interne.
- **Contenu survivant (Annexe H)** : écrire puis lire, R(𝒜·𝒫) = Ω_{𝒫,ρ} ∘ S_𝒜. Ce n'est pas un quotient global : le résultat est conditionnel à l'extinction exacte et à la regraine canonique. C'est une réduction *suffisante* sous protocole : s_r = s_r' implique les mêmes réponses, mais la réciproque n'est pas démontrée. Ce n'est pas le quotient de Nerode.
- **Quatre opérations** : inclure, écrire, lire, quotienter. Oublier de l'information n'est pas un défaut. La question est ce qui doit survivre à la perte.

### 1.7 Objets, support, quotient [TEX]

**Objet** 𝖲 = (S, I_S, 𝔅_S), avec I_S ⊆ C_S les conditions initiales déclarées et 𝔅_S ⊆ 𝔐_S les histoires admissibles. I_S n'altère pas l'IWS : il équipe sa description expérimentale.

**Support** :
$$
\mathrm{Reach}^G_{\mathcal B_S}(I_S)=\{\gamma^G_{S,\mathcal H}(x_0)(t) : x_0\in I_S,\ \mathcal H\in\mathcal B_S\},\qquad \mathrm{Supp}^G(\mathsf S)=I_S\cup\mathrm{Reach}^G_{\mathcal B_S}(I_S).
$$

**Flèche** (f, η) avec f(I_S) ⊆ I_T. En G₁, la condition est :
$$
f\bigl(\bar\gamma_{S,\mathcal H}(x_0)(t)\bigr)=\bar\gamma_{T,\eta(\mathcal H)}(f(x_0))(t),\qquad x_0\in I_S,\ \mathcal H\in\mathcal B_S.
$$

**Quotient** : f ∼_G f' si et seulement si f et f' coïncident sur Supp^G(𝖲). Trois propriétés :
- être un morphisme ne dépend que de f|_Supp, donc Hom est saturé pour ∼_G ;
- f(Supp^G(𝖲)) ⊆ Supp^G(𝖳) ;
- ∼_G est une congruence pour la composition.

**Normalisation propre à G₁** (remarque) : remplacer I_S par K*(I_S) ne change pas la trajectoire post-cascade. Ce n'est pas retenu comme définition, pour que I ∪ Reach reste uniforme en G₀ et en G₁.

### 1.8 Admissibilité et règle de saut [TEX]

- Dans le noyau, X^adm = C = {P_i ≤ Θ ∀i}. L'admissibilité de l'Annexe A est exactement l'appartenance à C.
- Deux écritures du saut coexistent : P⁺_{i*} = r_P P⁻_{i*} et r_PΘ. Elles coïncident sur les sauts atteints depuis C, où P⁻ = Θ. **Décision** : conserver r_P P⁻ comme règle générale, qui se réduit à r_PΘ sur une exécution admissible.

### 1.9 Points de sortie et invariance [TEX]

**Définition trajectorielle.** La tangence ponctuelle ne suffit pas à exclure une sortie d'ordre supérieur. Pour un point x du bord :
$$
x\in\partial^{\mathcal B}_{\mathrm{exit}}C \iff \exists u\in\mathcal B\ \forall\varepsilon>0\ \exists t\in(0,\varepsilon):\ \phi(t;x,u)\notin C.
$$
Cela suppose le flot défini sur un voisinage de C, et la notion dépend des entrées admissibles.

**[PROP, candidate] Invariance de C.** Hypothèses :
- C et D fermés ;
- flot continu ;
- entrées stables par décalage ;
- ∂_exit C ⊆ D et 𝒦(C ∩ D) ⊆ C ;
- priorité au premier contact ;
- H4.

Conclusion : toute exécution issue de C reste dans C.

### 1.10 Kairos au contact [TEX]

Dans le noyau, D ⊋ ∂_exit C peut se produire. Un point où P_i = Θ et Ṗ_i < 0 est rentrant, mais le saut s'y déclenche quand même ; de même pour un contact tangent. C'est un choix de modélisation : le Kairos a une signification événementielle propre. Conséquence : la dépendance en la condition initiale est discontinue lorsqu'un événement apparaît ou disparaît par contact tangent. C'est une seconde source de discontinuité, distincte des changements d'ordre entre Kairos. Point gardé en réserve pour la transversalité et la stratification.

### 1.11 Niveaux de description [TEX]

| Donnée | Rôle |
|---|---|
| S = (𝒳, C, F, D, 𝒦) | système hybride et événements possibles |
| Exec | sémantique d'exécution (priorité au saut, départage, fermeture des cascades) |
| I ⊆ C | conditions initiales / préparations déclarées |
| 𝔅 ⊆ 𝔐 | histoires / sollicitations admissibles |
| G | résolution temporelle et événementielle |
| ω_ρ | lecture de l'exécution |

L'objet est (S, I_S, 𝔅_S). G indexe la notion de morphisme. ω_ρ reste dans la couche observationnelle. *(Amendement, §3.2 : la lecture d'état ρ_X entre dans la définition de la classe via I1_ρ. Seules les lectures d'exécution ω restent observationnelles.)* La clôture de C porte sur les états, la clôture de 𝔐 (décalage, concaténation) sur les histoires : ces deux niveaux interagissent dans la preuve d'invariance mais ne se confondent pas.

---

## 2. Acquis de discussion absents du .tex v4 [DISC] (non remis à jour — voir note en tête de document)

Ces points sont utilisés implicitement par la section « Point d'étape » du .tex (γ̄, K*, η, G₁), mais ne sont définis nulle part dans le document.

### 2.1 Granularité des exécutions

**Pourquoi il en faut une : le cas Δ.** Sur Δ, toutes les pressions sont égales, donc chaque Kairos du système homogène est une cascade de N sauts dans S. Les états intermédiaires de cette cascade sortent de Δ. Il en découle :
- la flèche naturelle est ι : S_Δ → S, et c'est la cible qui a le plus de sauts ;
- aucun carré commutatif saut par saut n'existe ;
- ι n'est un morphisme **que pour les entrées uniformes**, puisque Δ n'est invariante que sous entrée uniforme.

Le .tex (§4.1.1) écrit encore « toute exécution de S_Δ correspond à une exécution de S », sans ces deux réserves.

**Commutations et exécutions : la hiérarchie s'inverse.** La définition est « préserver les exécutions ». Les égalités f∘Φ_S = Φ_T∘f et f∘𝒦_S = 𝒦_T∘f ne sont que des conditions suffisantes. Elles ne le sont que si f préserve *et réfléchit* les gardes :
$$
f(D_S)\subseteq D_T \quad\text{et}\quad f(C_S\setminus D_S)\subseteq C_T\setminus D_T.
$$
Le .tex (§4) présente encore les commutations comme l'expression de l'idée.

**Les trois granularités.**
- **G₀ — même domaine hybride.** f ∘ γ ∈ Exec(T) sur un même dom γ ⊆ ℝ≥0 × ℕ.
- **G₁ — trajectoire post-cascade.** Par H3 et H4, la fermeture de cascade K*(x), état terminal unique de la cascade instantanée, est bien définie. On en tire la trajectoire canonique γ̄ : ℝ≥0 → 𝒳, et l'application q₁ : γ ↦ γ̄. Coût : G₁ oublie les états intermédiaires et l'ordre interne d'une cascade, mais pas son résultat.
- **G₂ — reparamétrisation du temps continu.** [OUVERT] Quelle classe de λ (continue, strictement croissante, homéomorphisme, plateaux) ? Que deviennent les instants de Kairos ?

**Ordre** G₀ ≼ G₁ ≼ G₂. [PROP] **IWS**₀ ⊆ **IWS**₁ (sous-catégorie large) : sur un même domaine E, le dernier indice j̄(t) = max{j : (t,j) ∈ E} est commun, donc f(γ̄_S(t)) = f(γ_S(t, j̄(t))) = γ_T(t, j̄(t)) = γ̄_T(t). □ L'inclusion **IWS**₁ ⊆ **IWS**₂ attend la définition de G₂.

**Pourquoi G₁ comme niveau canonique.** Il ne demande aucun choix de témoin κ, il est exact pour la réduction homogène, et il est maniable en Lean (une trajectoire ℝ≥0 → 𝒳).

### 2.2 Transport des histoires η

- η : 𝔐_S → 𝔐_T est un **morphisme de monoïdes sur les monoïdes ambiants** : η(ε) = ε et η(ℋ₁·ℋ₂) = η(ℋ₁)·η(ℋ₂). On demande de plus η(𝔅_S) ⊆ 𝔅_T.
- **Pourquoi sur 𝔐 et non sur 𝔅** : l'Annexe G admet des classes minimales sans fermeture (ε ∉ 𝔅 et ℋ₁·ℋ₂ ∉ 𝔅 sont possibles).
- **Pourquoi un morphisme de monoïdes** : la condition sur les exécutions ne l'impose pas, mais continuations, fermetures et congruences de l'Annexe G reposent sur la concaténation.
- **η est indépendant de x₀.** Sinon η transporterait des expériences complètes X^adm × 𝔅 → 𝔅 : c'est une autre notion, non interdite, mais qu'aucun obstacle ne demande.
- **La compatibilité temporelle relève de G, pas de η.** En G₀ et G₁, |η(ℋ)| = |ℋ| ; c'est même une conséquence si l'exécution sous ℋ est définie sur [0, |ℋ|]. En G₂, on attend une condition via λ.

### 2.3 Catégorie **IWS**_G

- **Identité** : (id, id).
- **Composition** : (g, θ)∘(f, η) = (g∘f, θ∘η), puisque
$$
(g\circ f)\circ\bar\gamma_{S,\mathcal H}(x_0)=\bar\gamma_{U,(\theta\circ\eta)(\mathcal H)}(g f x_0).
$$

C'est une catégorie pour chaque granularité G. La question 2 du §5 du .tex (fermeture par composition, identités) est donc **résolue**. On note **IWS**_G et non **IWS**_{G,𝔅}, parce que 𝔅 varie avec l'objet et que η fait partie de la flèche.

**Lecture d'ensemble** : on n'obtient pas « la catégorie des IWS », mais une famille de catégories de *descriptions*, indexées par la résolution à laquelle une transformation doit être fidèle.

### 2.4 Lectures

- **Type** : ω_ρ : Exec(S) → 𝒴_ρ, qui est le type de l'Annexe H. Une lecture d'état ρ_X : 𝒳 → Y en est un cas particulier.
- **Compatibilité avec G₁** : ω_ρ = ω̄_ρ ∘ q₁ pour un certain ω̄_ρ. Une lecture d'états post-cascade factorise ; un compteur de Kairos à l'instant t ne factorise pas.
- **Rôle des indices** : ρ ne fixe pas G, il **contraint** les G admissibles. Les indices (𝔅, ρ, G) répondent à trois questions distinctes : sous quelles sollicitations ? que regarde-t-on ? à quelle résolution ?
- **Transport ψ entre espaces de lecture** : différé, jusqu'à ce qu'un obstacle le réclame.

### 2.5 Admissibilité abstraite et Annexe A

- Dans la classe, « admissible » est une donnée déclarée (X^adm, 𝔐^adm), soumise à deux conditions :
  - **(a) bonne position** : H2–H4 depuis X^adm sous 𝔐^adm ;
  - **(b) clôture** : états atteints dans X^adm ; histoires stables par restriction, décalage et concaténation.
  L'invariance fait partie de la définition d'« admissible » ; il n'y a pas d'axiome H5.
- **À ajouter à l'Annexe A** : le lemme d'invariance de C, aujourd'hui utilisé implicitement lors de la relance après chaque saut. Il faut aussi y harmoniser la règle de saut selon la décision du §1.8 (l'Annexe A écrit r_PΘ).
- **Option écartée** : l'ensemble maximal de bonne position W. Il serait automatiquement invariant, mais il est plus grand que l'ensemble du Tome I (les états où P_i > Θ donnent encore des cascades finies) et il n'est en général ni connu ni calculable.

---

## 3. Points relevés à la relecture du v4 [NOUV] (non remis à jour — voir note en tête de document ; au moins 3.13 est déjà incorporé en V5.5, cf. §4.3)

### 3.1 — I1 dépend de la présentation — l'indépendance I2 ⇏ I1 en dépend aussi

I1 est énoncé pour une écriture « x = (y, h) ». Si cette écriture peut être choisie librement, le témoin discret satisfait I1. Prenons la décomposition
$$
\tilde y = y\,(1+s),\qquad h = s,
$$
qui est bijective sur [0,1] × {0,1}. Sur le flot, F_ỹ = (1 + s)·ẏ = 1 + h. En ỹ₀ = ½, par exemple avec (y, s) = (½, 0) et (¼, 1), on obtient F_ỹ = 1 d'un côté et 2 de l'autre. **I1 est satisfaite.**

**Portée.** Pour presque tout système dont le flot n'est pas nul et qui possède une seconde composante, un changement de coordonnées du type ỹ = y·g(h), avec g non constante, rend F_ỹ dépendant de h. Lu existentiellement sur les décompositions, I1 est presque vide, et le témoin discret ne prouve plus I2 ⇏ I1.

En revanche, I1 ⇏ I2 reste robuste : D = ∅ exclut I2 dans toute présentation. I2 dépend aussi d'une coupe déclarée (π_s), mais le choix de la présentation ne peut que la rendre plus facile à satisfaire.

**C'est la leçon de I3 qui revient** : une même dynamique admet plusieurs présentations, et ce qui semblait réglé par la syntaxe dépend de la coordonnée choisie.

**Correction proposée** : rendre I1 relatif à une coupe déclarée, de préférence induite par une lecture d'état ρ : 𝒳 → Y (où y = ρ(x)). La formulation devient intrinsèque, sans coordonnées :
$$
\exists\, x_1,x_2\in C :\quad \rho(x_1)=\rho(x_2)\quad\text{et}\quad (\mathcal L_F\rho)(x_1)\neq(\mathcal L_F\rho)(x_2),
$$
où ℒ_Fρ désigne la dérivée de ρ le long du champ (pour une entrée admissible donnée, en présence d'entrées). Pour ρ = π_y, le témoin discret échoue I1 ; pour ρ(y,s) = y(1+s), il la satisfait. L'indépendance doit donc s'énoncer **pour une lecture déclarée** (« pour ρ = π_y, … »).

**Conséquence** : la question 1 du §5 du .tex (historicité relative à ρ) n'est plus « en réserve ». Elle conditionne le caractère bien défini de I1. Deux remarques :
- le type ρ_X : 𝒳 → Y utilisé dans la remarque sur I1 (ligne ~234) est le bon type à cet endroit : c'est un cas particulier de ω_ρ, pas une incohérence ;
- cela rattache I1 au principe d'indexation (𝔅, ρ) du reste du manuscrit.

**Décision (à reporter en tête de la V5)** : *I1 n'est pas intrinsèque à F ; I1_ρ est relative à une lecture déclarée.* Interprétation : deux états instantanément indiscernables pour ρ n'ont pas le même futur infinitésimal. L'indépendance s'énonce pour ρ fixée :
$$
\mathrm{I1}_\rho\not\Rightarrow\mathrm{I2},\qquad \mathrm{I2}\not\Rightarrow\mathrm{I1}_\rho\qquad(\rho=\pi_y).
$$
On ne prétend plus démontrer une indépendance sous changement arbitraire de présentation.

### 3.2 — I1_ρ n'est pas encore l'historicité

**Distinction.** I1_ρ établit une **non-Markovianité apparente relativement à ρ** : une mémoire cachée relativement à ρ, pas encore son caractère historique. Un degré interne quelconque, non lu par ρ, produit le même phénomène. Deux cas concrets :
- **Le témoin continu est de l'inertie déguisée** : h = y + ẏ, et le système équivaut à ÿ = −2ẏ. La variable « cachée » est la vitesse de la lecture.
- **Le noyau avec ρ = π_H** satisfait I1_ρ par V seul (Ḣ = V), sans intervention de τ.

**Conséquence immédiate pour la V5** : déclarer la lecture du noyau. Pour que I1_ρ capte la trace, ρ doit lire au moins (H, V). La lecture qui correspond à `prop:t1-trace-modifie-futur` est ρ = (H, V, P, A), puisque la proposition fixe ces quatre composantes et ne fait varier que τ.

**Fausse piste : la reconstructibilité à partir du passé récent de ρ.** Pour des systèmes génériques, l'état se reconstruit à partir d'un jet fini de la sortie (observabilité générique : Aeyels, Gauthier–Kupka, dans l'esprit du plongement de Takens — *énoncés à vérifier avant citation*). Dans le noyau, M et Γ ne dépendent de τ que via ττᵀ et ‖τ‖. Le 2-jet de H (avec u connu) fixe donc probablement τ au signe près, et τ̇ lève le signe aux ordres suivants. Ce critère ne séparerait pas τ de V : l'historicité doit venir des **histoires**, pas de l'observabilité.

**Formulation par les histoires (proposition).**
$$
\mathrm H_{\rho,I,\mathcal B}:\quad \exists\,x_0\in I,\ \mathcal H_1,\mathcal H_2\in\mathcal B:\ \rho(x_1)=\rho(x_2)\ \text{ et }\ \exists\,\mathcal H':\ \mathcal R^\rho_{x_1}(\mathcal H')\neq\mathcal R^\rho_{x_2}(\mathcal H'),
$$
où x_k est l'état atteint depuis x₀ après ℋ_k. Deux histoires issues d'un même départ laissent la même lecture présente mais des futurs séparables. Le quotient des histoires par les réponses (type Nerode, Annexe G) est alors strictement plus fin que le quotient par la lecture présente. La différence est *produite* par l'histoire, pas donnée par une condition initiale cachée.

**Vérifications sur les témoins.**
- **Témoin continu (autonome, histoires = attentes) : H échoue.** Depuis x₀, y(t) = (u + v e^{−2t})/2 est strictement monotone si v ≠ 0, constante si v = 0. Aucune paire d'histoires ne donne la même lecture avec des futurs différents : la variable cachée existe, mais aucune histoire ne l'écrit différemment.
- **Témoin discret : H est satisfaite.** Depuis (0,0), on atteint (½, 0) à t = ½ et (½, 1) à t = 3/2 : même lecture y = ½. Au saut suivant, l'un repart de 0, l'autre de ½.

**Le piège.** H est indifférente au canal : elle recueille les effets d'histoire du flot *et* des sauts. Remplacer I1_ρ par H ferait retomber I2 ⇏ I1, comme avec l'ancienne formulation « la trajectoire finit par différer ».

**Architecture proposée.**
- **Mécanismes** : I1_ρ (canal du flot, niveau du générateur) et I2 (canal du saut). Ils restent indépendants pour ρ fixée.
- **Phénomène** : l'historicité effective H_{ρ,I,𝔅}, indifférente au canal, relative à (ρ, I, 𝔅). Résultat attendu, à établir et non à postuler : « I1_ρ ou I2, plus une condition d'atteignabilité, entraîne H ». [OUVERT] : H dans la définition de classe, ou propriété dérivée ?

**Statut dans les modèles.** Pour le noyau, H est [OUVERT] : la proposition du Tome I porte sur des conditions initiales différant en τ, pas sur des différences produites par une histoire. Le modèle de l'Annexe H en est une instance, sous réserve que Ω_{𝒫,ρ} ne soit pas constante sur les contenus atteints : regraine et extinction ramènent (y, p, χ, θ) à une même valeur, et seul s diffère.

**Conséquence de typage.** Dès que I1 est relative à ρ, une lecture d'état ρ_X entre dans la définition de la classe : 𝔍𝔚𝔖 porte sur des couples (S, ρ). Seules les lectures d'exécution ω restent dans la couche observationnelle. La question ψ revient au niveau des objets : une flèche (f, η) doit-elle relier ρ_S et ρ_T ? [OUVERT] — à poser explicitement dans la V5.

### 3.3 — Condition de contenu du quotient — *adopté*

Le .tex écrit : « Le quotient retrouve un contenu réel dès lors que I_S est strictement plus petit que C_S. » La bonne condition est
$$
\mathrm{Supp}^G_{\mathcal B_S}(S, I_S)\subsetneq C_S.
$$
Même avec une graine I_S = {x₀}, si ses histoires explorent tout C_S, l'équivalence par restriction au support n'est que l'égalité.

### 3.4 — Reach en G₀ et en G₁ — *adopté*

$$
\mathrm{Reach}^{G_0}_{\mathcal B}(I)=\{\gamma_{\mathcal H,x_0}(t,j): x_0\in I,\ \mathcal H\in\mathcal B,\ (t,j)\in\operatorname{dom}\gamma\},
\qquad
\mathrm{Reach}^{G_1}_{\mathcal B}(I)=\{\bar\gamma_{\mathcal H,x_0}(t): x_0\in I,\ \mathcal H\in\mathcal B\}.
$$
Ce n'est pas cosmétique : la différence entre les deux ensembles est exactement ce que G₁ oublie.

### 3.5 — Entrées et histoires dans ∂_exit

La définition écrit « ∃ u ∈ 𝔅 » puis φ(t; x, u), ce qui confond histoires et entrées. Il faut préciser comment une histoire induit une entrée. L'argument de décalage requiert aussi la stabilité par décalage, qui est bien énoncée dans la proposition.

### 3.6 — Notation 𝒢_N

Le .tex v4 (§ Admissibilité, ligne ~709) écrit « le graphe dans 𝒢_N », comme la phrase d'admissibilité du Tome I. L'espace des états utilise 𝔊_N, et 𝒢 est déjà pris par la regraine et par 𝒢_lin (Annexes H, I). Proposition : remplacer 𝒢_N par 𝔊_N dans le Tome I et dans le v4. Vérifié seulement sur le Tome I et les Annexes A, H, I ; un grep sur l'ensemble des sources confirmerait.

### 3.7 — Définition du morphisme au §4 du .tex

« Envoie toute exécution admissible sur une exécution admissible » doit renvoyer à une granularité G. Sans cela, ι ne satisfait pas la définition (voir §2.1).

---

### 3.8 — Terminologie figée, et trois crash-tests du noyau

**Terminologie retenue pour la V5.** Le mot « historique » est retiré de la définition d'I1 : on avait baptisé le mécanisme d'après le phénomène qu'on espérait qu'il produise.
- **I1_ρ** : mécanisme continu caché relativement à ρ. Il répond à la question : « existe-t-il de l'information invisible à la lecture qui agit sur son évolution par ce canal ? ». Il ne dit ni que cette information vient du passé, ni qu'une expérience accessible permet de l'écrire.
- **I2** : mécanisme discret structurel.
- **H_{ρ,I,𝔅}** : historicité effective produite par des histoires.

Schéma : I1_ρ et I2 → H. Les flèches ne sont **pas** des théorèmes, faute des hypothèses d'atteignabilité et d'écriture. Le témoin continu montre qu'elles sont indispensables : I1 y est vraie grâce à deux états de C qu'aucune paire d'histoires issues de I n'atteint avec la même lecture. Le témoin discret donne H ⇏ I1_ρ, ce qui est voulu : H ne dit pas comment l'histoire est stockée ni réinjectée.

**Lecture déclarée du noyau.** Avec ρ = π_H, ℒ_Fρ = V, et I1 serait « démontrée » sans toucher τ. On fixe
$$
\rho_{\ker}(x)=(H,V,P,A).
$$
**[PROP]** I1_{ρ_ker} ⟺ (γ₁ > 0 ou λ > 0). Le sens ⇐ est `prop:t1-trace-modifie-futur`. Pour ⇒ : si γ₁ = λ = 0, ni Ḣ, ni V̇, ni Ṗ ne dépendent de τ (à entrée u commune).

**Crash-test 1 — le noyau échoue I2 tel que rédigé dans le v4.** La seule composante constante pendant le flot est A, donc s = A. Or π_{¬s}𝒦 ne dépend pas de A :
- i* est choisi par les pressions ;
- V_{i*} ↦ r_V V_{i*} et P_{i*} ↦ r_P P_{i*} ;
- H et τ sont inchangés.

La clause « π_{¬s}𝒦(x₁) ≠ π_{¬s}𝒦(x₂) » échoue. Le graphe agit *après* le saut et *par le flot* (Ã(A) dans V̇ et τ̇). *(Correction d'une affirmation antérieure de ce document, selon laquelle le noyau satisfaisait la clause.)* Correction proposée — « discret » qualifie le moment où s change, pas l'endroit où il agit :
$$
\mathrm{I2}:\ \exists\,x_1,x_2,\ \pi_{\neg s}x_1=\pi_{\neg s}x_2,\ \pi_sx_1\neq\pi_sx_2,\ \bigl[F_{\neg s}(x_1)\neq F_{\neg s}(x_2)\ \text{ou}\ (x_{1,2}\in D,\ \pi_{\neg s}\mathcal K x_1\neq\pi_{\neg s}\mathcal K x_2)\bigr],
$$
plus ṡ = 0 en flot, s⁺ ≠ s⁻ possible et déclenchement endogène. L'indépendance tient toujours :
- le témoin continu échoue I2 (sans saut, s ne change jamais) ;
- le témoin discret satisfait I2 (par 𝒦) et échoue I1_{π_y} ;
- le noyau satisfait I2 par F, dès que ζ ≠ 0 ou α ≠ 0 et que H n'est pas homogène.

**Crash-test 2 — S_Δ n'est probablement pas un IWS.** Sur Δ, H est homogène et Ã est stochastique par lignes, donc ÃH = H quel que soit A. Le graphe n'agit ni sur le flot ni sur le saut : la restructuration est décorative, et S_Δ échoue I2. *(À vérifier contre l'Annexe C, notamment ses « équilibres structurels ».)* Ça ne casse pas l'édifice : les flèches et les catégories n'utilisent que H1–H4, jamais I1–I3. On définit donc les flèches sur 𝔥 muni de ses régimes, et 𝔍𝔚𝔖_G est la sous-catégorie pleine. ι : S_Δ → S devient une flèche de 𝔥_G, d'un système qui n'est pas un IWS vers un IWS. La réserve du .tex (« sous réserve que le système réduit satisfasse les axiomes ») est tranchée sans perdre l'exemple.

**Crash-test 3 — le mécanisme central du noyau n'est représenté par aucun axiome.**

| | par F | par 𝒦 |
|---|---|---|
| caché pour ρ | I1_ρ | **manquant** |
| structurel s | I2 (corrigé) | I2 (corrigé) |

La case manquante est la trace qui pilote le recâblage : τ est invisible à ρ_ker, mais les similarités décident des arêtes. Candidat :
$$
\mathrm{I1}^{\mathcal K}_\rho:\ \exists\,x_1,x_2\in D,\ \rho(x_1)=\rho(x_2),\ \rho(\mathcal Kx_1)\neq\rho(\mathcal Kx_2).
$$
Le noyau la satisfait avec ρ_ker : la différence en τ ressort dans A⁺. Au point γ₁ = λ = 0, la trace est invisible au flot mais pilote le recâblage — le cœur d'IWS (nœuds communiquant par leurs traces accumulées) —, et pourtant ce système sort de la classe si I1_ρ est exigé tel quel. [OUVERT] : exiger I1_ρ, ou « un mécanisme caché, par F ou par 𝒦 » ?

**Typage de H.** Deux précisions :
$$
\mathrm H_{\rho,I,\mathcal B}:\ \exists\,x_0\in I,\ \mathcal H_1,\mathcal H_2\in\mathcal B,\ \mathcal H'\in\mathcal H_1^{-1}\mathcal B\cap\mathcal H_2^{-1}\mathcal B:\ x_k=\mathrm{End}(x_0,\mathcal H_k),\ \rho_X(x_1)=\rho_X(x_2),\ \mathcal R^{\omega}_{x_1}(\mathcal H')\neq\mathcal R^{\omega}_{x_2}(\mathcal H').
$$
- la continuation doit être admissible après les deux préfixes, d'où ℋ' ∈ ℋ₁⁻¹𝔅 ∩ ℋ₂⁻¹𝔅, avec les classes de l'Annexe G ;
- ρ intervient deux fois : ρ_X pour l'indiscernabilité présente, ω pour la lecture des futurs. Si ω lit plus que ρ_X (par exemple τ en fin d'exécution), H est triviale. On exige donc que ω soit induite par ρ_X — par exemple ω = ρ_X ∘ γ̄ sur la continuation, ou au moins qu'elle factorise par la trajectoire lue par ρ_X.

Interprétation Nerode : l'égalité de lecture présente est plus grossière que l'équivalence comportementale sous continuation. Le présent lu par ρ ne résume pas ce que l'histoire a laissé.

**Statut de ρ.** On distingue l'**IWS présenté** (S, ρ_X), qui porte la lecture constitutive nécessaire à I1_ρ, du **régime expérimental** (I, 𝔅) dont il est équipé, sans donner le même statut aux quatre composantes. Cohérent avec le crash-test 2 : ρ sert à l'appartenance à la classe, pas à la définition des flèches. La compatibilité ρ_T∘f = ψ∘ρ_S reste **grande ouverte** : l'imposer maintenant transformerait une conséquence possible de certains exemples en axiome général.

**Observabilité ≠ historicité.** Une trace historique peut être reconstructible à partir d'un jet assez riche de la sortie ; elle n'en a pas moins été produite par une histoire. On ne définit donc pas l'historicité par la non-reconstructibilité.

### 3.9 — Grille des mécanismes, S_Δ, stabilité par isomorphisme

**S_Δ ne satisfait pas I2 (vérifié contre l'Annexe C) — donc S_Δ ∉ 𝔍𝔚𝔖 si I2 est constitutif.** Pour un état homogène et une entrée uniforme, (ÃH)_i = h pour tout i, quel que soit le graphe (Ã stochastique par lignes). Les équations réduites ne contiennent plus A, et le Tome II présente la réduction comme une dynamique sur (h, v, θ, p) seul. Le graphe est causalement muet sur Δ : la restructuration y est décorative. Donc S_Δ ∉ 𝔍𝔚𝔖 si I2 reste constitutif. Les modes transverses à Δ dépendent encore du graphe ; seul le mode homogène redonne la dynamique réduite. *Une réduction exacte d'un IWS peut cesser d'être un IWS précisément parce qu'elle a quotienté le mécanisme qui faisait de lui un IWS.*

**Espace ambiant.** 𝔥 = systèmes hybrides satisfaisant H1–H4, et 𝔍𝔚𝔖 ⊆ 𝔥. Les catégories se construisent d'abord sur 𝔥_G ; 𝔍𝔚𝔖_G en est la sous-catégorie pleine une fois les axiomes arrêtés. ι : S_Δ → S est une flèche légitime de 𝔥_{G₁}, mais pas une flèche interne de 𝔍𝔚𝔖_{G₁}. La théorie des transformations n'attend pas la définition complète d'un IWS.

**I2 découpé.**
- **I2a (restructuration)** : s est constante pendant le flot, et ∃ x ∈ D : π_s𝒦(x) ≠ π_s x ; le déclenchement est endogène.
- **I2b (efficacité)** : ∃ x₁, x₂ avec π_{¬s}x₁ = π_{¬s}x₂ et π_s x₁ ≠ π_s x₂ tels que
$$
F_{\neg s}(x_1)\neq F_{\neg s}(x_2)\ \lor\ \bigl[x_1,x_2\in D\ \land\ \pi_{\neg s}\mathcal K(x_1)\neq\pi_{\neg s}\mathcal K(x_2)\bigr].
$$

I2 dit ainsi : une composante modifiée discrètement possède une efficacité causale, qu'elle s'exerce ensuite continûment ou au saut suivant. Cela corrige la confusion antérieure entre *mode d'écriture* et *mode de lecture* de s.

**Grille des mécanismes.**

| information causalement efficace | agit par F | agit par 𝒦 |
|---|---|---|
| cachée relativement à ρ | I1^F_ρ | I1^K_ρ |
| structure s, écrite discrètement | I2^F | I2^K |

- **I1^F_ρ** (ancien I1_ρ) : ∃ x₁, x₂ ∈ C, ρ(x₁) = ρ(x₂), ℒ_Fρ(x₁) ≠ ℒ_Fρ(x₂).
- **I1^K_ρ** : ∃ x₁, x₂ ∈ D, ρ(x₁) = ρ(x₂), ρ(𝒦x₁) ≠ ρ(𝒦x₂).

Le noyau occupe potentiellement trois cases : τ → F, τ → 𝒦 (recâblage par similarité ; suppose une configuration avec m > 0 où les classements diffèrent), et A → F.

**Question constitutive (laissée ouverte dans la V5)** : un IWS exige-t-il I1^F_ρ, ou I1^F_ρ ∨ I1^K_ρ, ou autre chose ? Crash-test idéal : γ₁ = λ = 0, où la trace n'agit plus sur le flot visible mais gouverne encore le recâblage. Si la définition exclut ce système, il faut pouvoir dire pourquoi il aurait cessé d'être un IWS ; faute de bonne réponse, c'est l'axiome qui est trop étroit.

**[PROP à démontrer proprement]** I1^F_{ρ_ker} ⟺ (γ₁ > 0 ∨ λ > 0). Il faut vérifier toutes les composantes de ℒ_Fρ_ker et les dégénérescences éventuelles.

**Recouvrement des lignes et convention sur ρ.** Avec ρ = π_y, la paire (1,0), (1,1) du témoin discret témoigne à la fois de I2^K et de I1^K_ρ. Si la clause constitutive devient I1^F_ρ ∨ I1^K_ρ, ce témoin la satisfait et ne prouve plus l'indépendance. **Convention proposée : la lecture constitutive lit toujours la composante structurelle** (ρ lit π_s). Les lignes deviennent disjointes par définition : caché = invisible à ρ ; structurel = visible et écrit discrètement. Une composante structurelle non lue n'est qu'une variable cachée constante par morceaux. ρ_ker lit A, donc le noyau est conforme. Indépendance réénoncée :
- I1^F_ρ ⇏ I2 : témoin continu, ρ = π_y ;
- I2 ⇏ (I1^F_ρ ∨ I1^K_ρ) : témoin discret, ρ = id — rien n'est caché, et I2^K tient puisque y repart de f(s).

**Typage final de H.** On définit la trajectoire lue ρ_{X*}γ̄ : t ↦ ρ_X(γ̄(t)) et on n'autorise que les réponses qui factorisent par elle :
$$
\omega=\widehat\omega\circ\rho_{X*}.
$$
H_{ρ,I,𝔅} signifie alors : même présent selon ρ, mais futurs distinguables en ne regardant toujours le système qu'à travers ρ. Continuation : ℋ' ∈ ℋ₁⁻¹𝔅 ∩ ℋ₂⁻¹𝔅.

**Crash-test : 𝔍𝔚𝔖_G n'est pas stable par isomorphisme dans 𝔥_G.** L'appartenance dépend de ρ, alors que les flèches de 𝔥_G ne voient pas ρ. Exemple : (noyau, ρ_ker) satisfait I1^F (si γ₁ > 0 ∨ λ > 0) ; (noyau, id) n'a rien de caché et échoue tout mécanisme de type I1 ; pourtant l'identité est un isomorphisme de 𝔥_G entre les deux. Le dilemme est structurel :
- ρ existentiel rend I1 triviale (ỹ = y(1+s), §3.1) ;
- ρ fixé fait de l'appartenance une propriété de la présentation.

Deux issues :
- **(a) Classe non stable par isomorphisme, assumée** : être un IWS est une propriété de l'IWS *présenté* (S, ρ), cohérente avec l'anti-essentialisme (𝔅, ρ).
- **(b) Des flèches qui voient ρ** : ρ_T ∘ f = ψ ∘ ρ_S. Si les isomorphismes exigent ψ bijective et différentiable, I1^F_ρ se transporte le long d'un isomorphisme. En effet, f conjugue les flots, donc ℒ_{F_T}ρ_T(f x) = dψ(ℒ_{F_S}ρ_S(x)) et ρ_S(x₁) = ρ_S(x₂) ⟺ ρ_T(f x₁) = ρ_T(f x₂).

C'est le **premier obstacle réel qui appelle ψ**, conformément à la règle « ψ apparaîtra parce qu'il manque quelque chose ». Non tranché. Seules les lignes « caché » dépendent de ρ : une classe définie par I2 et I3 seuls échapperait au problème. Le dilemme est donc couplé à la question constitutive ci-dessus.

**Collision de notation ρ.** ρ désigne désormais :
- la lecture constitutive ;
- la résolution d'observation (Annexes G–H) — même famille conceptuelle, acceptable ;
- les modes de Ã dans l'Annexe C (ρ ≠ 1, ρ = 1) — collision à corriger dans la V5.

*(Vu via la citation de l'Annexe C, pas vérifié dans le texte source.)*

**Architecture résultante.**
$$
\begin{array}{c}
(S,\rho_X)\ \text{IWS présenté}\\
\downarrow\ \text{équipé de } (I,\mathcal B)\ \text{régime expérimental}\\
\mathrm{I1}^F_\rho,\ \mathrm{I1}^K_\rho,\ \mathrm{I2}^F,\ \mathrm{I2}^K\ \ \text{mécanismes}\\
\downarrow\ \text{atteignabilité à établir}\\
\mathrm H_{\rho,I,\mathcal B}\ \ \text{phénomène historique effectif}
\end{array}
$$
Les morphismes vivent dans 𝔥_G sans avoir à savoir quel mécanisme fait d'un objet un IWS.

### 3.10 — ψ justifié, convention sur s, transport des mécanismes

**Convention adoptée : la lecture constitutive voit la structure.**
$$
\pi_s=r_s\circ\rho_X\qquad(\text{donc }\rho_X(x_1)=\rho_X(x_2)\Rightarrow s(x_1)=s(x_2)).
$$
Les témoins de I1^F_ρ ou I1^𝒦_ρ ne peuvent plus différer uniquement par s. Les lignes de la grille correspondent à deux sources d'information distinctes : invisible à ρ_X, ou structure visible et écrite discrètement. « Caché » n'est plus une propriété ontologique d'une variable : c'est « non visible par la lecture constitutive ». Un s non lu n'a aucune raison de recevoir le statut de structure. Indépendance :
- I2 ⇏ (I1^F_ρ ∨ I1^𝒦_ρ) : témoin discret avec ρ_X = id (aucune paire distincte de même lecture ; I2^𝒦 tient) ;
- I1^F_ρ ⇏ I2 : témoin continu, inchangé.

**S_Δ — formulation rigoureuse.** S_Δ ne satisfait pas I2 (Annexe C : ÃH = H indépendamment du graphe). Par conséquent, S_Δ ∉ 𝔍𝔚𝔖 **si I2 est retenu comme axiome constitutif**.

**Typage des objets avant la stabilité par isomorphisme.** Si les objets de 𝔥_G sont les systèmes nus, alors que l'appartenance à 𝔍𝔚𝔖 dépend de (S, ρ_X), écrire « 𝔍𝔚𝔖_G sous-catégorie pleine de 𝔥_G » est trompeur : (S, ρ_ker) et (S, id) ont le même objet sous-jacent. Deux architectures restent ouvertes :
- **A.** IWS = propriété d'une présentation. On travaille dans une catégorie 𝔥_G^pres d'objets (S, ρ_X), dont les flèches peuvent oublier ρ_X. C'est cohérent, mais deux objets de même dynamique peuvent avoir des statuts différents.
- **B.** Les lectures font partie de la structure transportée. Les flèches sont des triplets (f, η, ψ) : (S, ρ_S) → (T, ρ_T), avec ρ_T ∘ f = ψ ∘ ρ_S.

Le choix entre A et B dépend lui-même de la question constitutive : si la classe minimale n'exige que I2 + I3, le problème disparaît. Il serait prématuré de construire une catégorie enrichie pour sauver un axiome dont on ignore s'il est constitutif.

**Transport des mécanismes par une flèche de type B.**
- **Canal continu, calcul le long des trajectoires.**
$$
\mathcal L_{F_T}\rho_T(fx)=\tfrac{d}{dt}\big|_0\,\psi\bigl(\rho_S(\phi^S_tx)\bigr)=d\psi_{\rho_S(x)}\bigl(\mathcal L_{F_S}\rho_S(x)\bigr).
$$
Les témoins partageant r = ρ_S(x₁) = ρ_S(x₂), il suffit que dψ_r soit injective et ψ différentiable. Ni l'injectivité de ψ ni la différentiabilité de f ne sont requises. Deux réserves : il faut conserver le temps (G₀, G₁ ; en G₂, des facteurs λ' propres à chaque trajectoire peuvent rendre égaux deux vecteurs proportionnels), et les témoins doivent être dans le support.
- **Le support est un problème de fond.** Les flèches ne sont contraintes que sur Supp = I ∪ Reach, alors que les mécanismes sont définis sans régime (témoins quelconques dans C). L'invariance ne s'énonce donc que pour des témoins dans Supp. Choix à faire : mécanismes relatifs au régime (I, 𝔅), ce qui les rapproche de H, ou invariance partielle.
- **Canal discret en G₁ : 𝒦 et D sont invisibles aux flèches.** ρ_T(𝒦_T fx) = ψ(ρ_S(𝒦_S x)) suppose une conjugaison saut par saut, disponible en G₀ seulement. Surtout, Reach¹ tel qu'il est défini ne contient que les valeurs post-cascade γ̄(t) ; les états pré-saut γ̄(t⁻) ∈ D n'y sont pas, donc f n'est contraint nulle part sur D. I1^𝒦 et I2^𝒦 sont invisibles aux flèches G₁, même avec ψ. **Correction proposée** :
  - G₁ retient les couples (γ̄(t⁻), γ̄(t)) = (x⁻, K*(x⁻)), et Reach¹ contient les limites à gauche ;
  - les mécanismes discrets s'énoncent en G₁ avec K* : I1^{K*}_ρ, I2^{K*}.

  G₁ oublie alors l'intérieur des cascades, pas leurs deux bords.
- **[CONJ]** Sous A ou B, avec régularité, conjugaison des exécutions et gardes précisées : I1^F_ρ et I1^{K*}_ρ sont invariants par isomorphisme présenté, pour des témoins dans le support.

**Notation.**
- **ρ_X** est réservé à la lecture constitutive d'état.
- **Valeur propre de Ã (Annexe C).** Elle doit être renommée, mais **μ est déjà pris** (Tome I : μ = L_M(λ)(α√d + β τ̄), condition (S)). Proposition : ν, avec J(ρ) → J(ν), ν = 1 homogène, ν ≠ 1 transverse. *(ν absent des textes lus — Tome I, Annexes A, H, I — à confirmer en cherchant dans toutes les sources.)*
- **Convention (𝔅, ρ) du manuscrit.** Elle est utilisée partout. Proposition pour la préserver : ρ désigne la déclaration observationnelle complète ρ = (ρ_X, ω̂), avec ω = ω̂ ∘ ρ_{X*}. ρ_X en est la composante d'état constitutive, et la résolution des Annexes G–H devient ω̂.

### 3.11 — Avis sur les trois nœuds ouverts de la V5 (propositions à valider)

Ordre de traitement suggéré : 1 → 2 → 3. Le nœud 1 conditionne le 2 ; le 3 peut attendre.

**Nœud 1 — H constitutif, mécanismes comme taxonomie.**
- **Ancrage textuel** (conclusion de main.tex) : « Un IWS n'est donc pas défini par la conservation de son passé. Il l'est […] par la manière dont ce passé demeure capable de modifier ses futurs. » C'est H_{ρ,I,𝔅} : le phénomène est définitionnel, les mécanismes décrivent comment il se réalise.
- **Dépendance au régime levée par monotonie.** H est croissante en (I, 𝔅) (ℋ⁻¹𝔅 = {ℋ' : ℋ·ℋ' ∈ 𝔅} grossit avec 𝔅). « Il existe un régime où H vaut » ⟺ « H vaut dans le régime maximal (C, 𝔐^adm) ». L'appartenance ne dépend plus que de ρ. Pas de trivialisation, contrairement à l'existentiel sur ρ, qui n'est pas croissant.
- **[PROP, candidate] H ⇒ un témoin, dans Supp, d'un mécanisme caché.** Si aucun mécanisme caché n'a de témoin sur Supp, on a sur Supp ℒ_Fρ = g∘ρ, 𝟙_D = d∘ρ et ρ∘K* = k∘ρ : ρ_X est une *application facteur* (semi-conjugaison vers une dynamique hybride fermée sur Y). Si cette dynamique lue a des exécutions uniques (g localement lipschitzienne, etc.), la trajectoire lue d'une continuation ne dépend que de ρ(x) et de ℋ', donc H est fausse. Interprétation : l'historicité effective est un défaut d'agrégation exacte de ρ que les histoires exploitent effectivement (analogue hybride de la lumpabilité de Kemeny–Snell). Ce sens n'exige aucune atteignabilité ; c'est la réciproque qui en demande.
- **Colonne manquante : la garde.** La preuve fait apparaître un troisième canal :
$$
\mathrm{I1}^D_\rho:\ \exists\,x_1,x_2,\ \rho(x_1)=\rho(x_2),\ x_1\in D,\ x_2\notin D.
$$
La grille passe à trois canaux : F (flot), D (déclenchement), K* (résultat du saut). Dans le noyau, D = {P_i ≥ Θ} est lu par ρ_ker, donc la colonne est vide ; c'est pourtant là que vit l'endogénéité du Kairos. Ajouter aussi à I2b une clause de garde (x₁ ∈ D, x₂ ∉ D).
- **Crash-tests.**
  - Témoin inertiel : exclu (H échoue).
  - Noyau avec γ₁ = λ = 0 : inclus dès que H vaut par le recâblage (plausible, à démontrer). Plus besoin de choisir entre I1^F et I1^F ∨ I1^K.
  - Témoin discret sous la convention π_s = r_s∘ρ_X : ρ lit tout l'état, donc H échoue. Un système entièrement lu n'a pas d'historicité relative à sa lecture.
- **Candidat** : 𝔍𝔚𝔖 = H_{ρ, C, 𝔐^adm} + I2 + I3. Réserves : H est plus difficile à vérifier qu'un mécanisme (il faut exhiber des histoires) ; garder I2 reste un choix, car sans lui H admettrait des mémoires purement continues sans Kairos.

**Nœud 2 — ψ transporte toute la déclaration.**
- Si H est constitutive, ψ = (ψ_X, ψ_ω), avec ρ_T∘f = ψ_X∘ρ_S et ω̂_T∘ψ_{X*} = ψ_ω∘ω̂_S.
- **[PROP, candidate] H se transporte vers l'avant le long de (f, η, ψ) si ψ_ω est injective.** Esquisse :
  - f(x_k) = End(f x₀, η(ℋ_k)), par la condition de flèche ;
  - η(ℋ') ∈ η(ℋ₁)⁻¹𝔅_T ∩ η(ℋ₂)⁻¹𝔅_T, puisque η est un morphisme de monoïdes et η(𝔅_S) ⊆ 𝔅_T ;
  - égalité des lectures présentes par ψ_X ;
  - trajectoire lue dans T = ψ_X ∘ (trajectoire lue dans S), puisque f∘γ̄_S = γ̄_T ;
  - réponses distinctes par l'injectivité de ψ_ω.

  Ni différentiabilité ni décalage de support (H vit sur les états atteints). Transport plus simple que celui des mécanismes : autre argument pour H.
- **Recommandation : B localisée.** 𝔥_G pour les flèches dynamiques ; une couche 𝔥_G^obs dont les flèches portent ψ, avec un foncteur d'oubli vers 𝔥_G. L'appartenance est invariante par isomorphisme dans 𝔥_G^obs, pas dans 𝔥_G — ce qui est juste, puisque l'historicité est relative à la lecture.

**Nœud 3 — G₂ : ne pas le définir dans la V5, noter deux contraintes.**
- **G₂ uniforme** (même λ pour toutes les exécutions). η morphisme de monoïdes et |η(ℋ)| = λ(|ℋ|) rendent λ additive sur les durées ; monotone, elle est linéaire, λ(t) = ct. C'est seulement un changement d'unité de temps.
- **G₂ orbital** (λ dépendant de la trajectoire, comme le temps propre en longueur d'arc). En présence d'entrées, il est incompatible avec un η indépendant de x₀ : il force le transport η̃ d'expériences complètes, jusqu'ici écarté faute d'obstacle. Le programme du temps intrinsèque sera cet obstacle. Deux ajustements suivraient :
  - I1^F en version orbitale (vitesses lues non positivement colinéaires) ;
  - ω̂ invariante par reparamétrisation.
- **Ce que G₂ conserverait** : les orbites et la suite ordonnée des Kairos, c'est-à-dire l'« ordre intrinsèque » de la remarque sur I2.

**Correction au document d'état V5 (§8).** Reach¹ contient les deux bords de cascade, mais la condition de flèche G₁ doit aussi les préserver. Sans continuité de f, il faut ajouter f(γ̄_S(t⁻)) = γ̄_T(t⁻). L'inclusion 𝔥_{G₀} ⊆ 𝔥_{G₁} reste vraie (l'état pré-cascade est γ(t, j_min(t))).

### 3.12 — H constitutif : acquis, et cinq crash-tests avant de figer

**Acquis de principe.** On définit l'IWS par la conséquence comportementale que le Tome I lui attribue, pas par ses mécanismes. Notations :
- H_ρ^max := H_{ρ, C, 𝔐^adm} pour l'axiome constitutif ;
- H_{ρ,I,𝔅} pour l'analyse expérimentale (l'historicité est-elle manifestable dans telle expérience ?).

La grille I1/I2 devient une taxonomie causale des membres de la classe (trois canaux F, D, K*). La question « I1^F ou I1^F ∨ I1^K ? » disparaît : c'était la mauvaise question. ψ et la couche observationnelle : U : 𝔥_G^obs → 𝔥_G est le foncteur d'oubli, et 𝔍𝔚𝔖_G vit dans 𝔥_G^obs. G₂ n'a pas encore gagné le droit d'être défini (horloge uniforme ⇒ λ(t) = ct ; horloge propre à chaque exécution ⇒ ressuscite η̃).

**Crash-test 1 — monotonie en ω̂.** Si ω̂' = φ∘ω̂ est plus grossière, ses témoins sont des témoins pour ω̂. Le test constitutif prend la réponse la plus fine : la trajectoire lue elle-même (ω̂ = id). Conséquences :
- l'appartenance ne dépend que de ρ_X (IWS présenté = (S, ρ_X)) ;
- l'invariance de l'appartenance ne demande que ψ_X injective sur les valeurs pertinentes ; ψ_ω ne sert qu'à l'analyse expérimentale.

**Crash-test 2 — le théorème central exige une hypothèse de régularité.** Contre-exemple : 𝒳 = ℝ², F = (1, 0), D = ∅, ρ(x) = max(0, x₁ − x₂)³.
- ℒ_Fρ = 3ρ^{2/3} ne dépend que de ρ : aucun témoin d'aucun mécanisme, nulle part.
- H vaut pourtant : depuis x₀ = (0,1), les attentes 0 et ½ donnent (0,1) et (½,1), de lecture nulle ; sous une attente d'une unité, les lectures sont max(0, t−1)³ et max(0, t−½)³.
- La factorisation est exacte mais la dynamique lue ṙ = 3r^{2/3} n'a pas l'unicité. Toutes les dérivées de Lie de ρ s'annulent aux deux points : aucun critère fini ne détecte la différence.

Énoncé corrigé, **[PROP, candidate]** :
$$
\mathrm H_\rho\Longrightarrow\bigl(\mathrm{I1}^F_\rho\lor\mathrm{I1}^D_\rho\lor\mathrm{I1}^{K^*}_\rho\ \text{sur le support}\bigr)\lor\bigl(\text{dynamique lue mal posée}\bigr).
$$
Le second cas est une **minuterie dormante** : la lecture reste plate pendant que l'état caché compte le temps. Deux options : l'exclure par hypothèse (g(r, u) localement lipschitzienne en r), ou l'admettre comme quatrième forme, une mémoire *latente*. Avec entrée, écrire g(ρ_X(x), u). La réciproque demande l'atteignabilité / l'écriture. Lecture : I1 = là où l'agrégation par ρ_X échoue ; H = une histoire exploite effectivement cet échec. Kemeny–Snell comme positionnement, pas comme identification.

**Crash-test 3 — H^max dépend de 𝔐^adm (correction de « inertie déguisée »).** L'identité h = y + ẏ ne vaut que pour le témoin autonome. Avec entrée (ẏ = −y + h + u, ḣ = y − h), le système est commandable (b = (1,0), Ab = (−1,1), rang 2). Des histoires d'entrée différentes atteignent (0,0) et (0,1), de même lecture et de futurs distincts : H vaut. h devient
$$
h(t)=e^{-t}h_0+\int_0^t e^{-(t-s)}y(s)\,ds,
$$
une trace exponentielle du passé de y, de même forme que τ. Autonome, h est de la cinématique ; forcé, c'est une vraie trace. Les deux verdicts sont justes, mais dépendent de la classe d'entrées.
- Noyau autonome (u ≡ 0) : H^max exigerait une récurrence exacte de (H, V, P, A) avec τ différent le long d'une même trajectoire, vraisemblablement non générique.
- Noyau avec les entrées bornées du Tome I : H^max plausible, [OUVERT].
- Régraine (Tome III) : c'est l'épisode qui fabrique l'égalité des lectures présentes.

Conséquence : **𝔐^adm est une donnée constitutive**, et l'objet présenté est (S, ρ_X, 𝔐^adm). Un même système peut n'être historique qu'ouvert — écho de la distinction Tome I (autonome) / Tome II (ouvert).

**Crash-test 4 — I2 : la juxtaposition.** Soit S₁ à mémoire continue (H sans I2 ; par exemple le témoin forcé) et S₂ un relais hybride entièrement lu (I2 sans H). Le produit S₁ × S₂, avec la lecture produit, satisfait H, I2 et I3, donc il est IWS selon le candidat. Pourtant rien n'y relie l'histoire à la restructuration.

Proposition : l'**historicité structurelle H^s**, c'est-à-dire H avec une réponse qui ne lit que la trajectoire de s (ω̂ = r_s-lecture) : les futurs se distinguent déjà dans la structure.
- H^s ⇒ H (ρ lit s) et H^s ⇒ I2a (s doit changer).
- Le produit échoue H^s : la structure de S₂ est indépendante de la mémoire de S₁, et S₂ seul n'a pas H.
- Le noyau avec γ₁ = λ = 0 en est le cas typique (la trace écrit le futur de A par le recâblage).
- H^s généralise au niveau des histoires l'« historicité structurelle » du Tome I (dépendance à l'ordre des Kairos).

**Candidat révisé :**
$$
(S,\rho_X,\mathfrak M^{adm})\in\mathfrak{IWS}\iff S\in\mathfrak H,\ \mathrm H^{s,\max}_\rho,\ \mathrm{I2b},\ \mathrm{I3}.
$$
I2b exclut une structure écrite par l'histoire mais inerte (simple registre). À soumettre aux mêmes crash-tests.

**Crash-test 5 — deux formulations non équivalentes de G₁.**
- Version ponctuelle : f(γ̄_S(t⁻)) = γ̄_T(t⁻) et f(γ̄_S(t)) = γ̄_T(t). Elle permet d'*effacer* un événement (T coule en t, f(x⁻) = f(x⁺)).
- Version macro-transition : x⁻ →K* x⁺ envoyé sur f(x⁻) →K*_T f(x⁺). Elle l'interdit, sauf macro-transitions identiques.

On voulait des flèches capables d'oublier des événements : garder la version ponctuelle comme définition, la version macro-transition comme sous-classe (flèches qui préservent les événements). Il faut distinguer « appartenir à Reach » et « être contraint par la flèche ». G₀ ⇒ G₁ reste immédiat (bords gauche et droit = premier et dernier état du bloc à l'instant t).

**Théorème central visé pour la V5** : H_ρ ⇒ échec, sur le support, de la factorisation hybride exacte *et bien posée* par ρ_X.

### 3.13 — Candidat structurel et nouveaux crash-tests

**Décisions de ce tour.**
- **ω̂ retiré de l'objet constitutif** (monotonie : le test d'appartenance prend ω̂ = id). Objet présenté : (S, ρ_X, 𝔐^adm). (𝔅, ρ) au sens expérimental subsiste avec des déclarations plus riches, mais ne définit pas la classe. Pour préserver l'appartenance, c'est ρ_{X,T}∘f = ψ_X∘ρ_{X,S} qui compte ; ψ_ω relève des expériences particulières.
- **Reformulation du théorème central** : H_ρ ⇒ ρ_X n'induit pas de dynamique hybride quotient déterministe et bien posée. Deux familles de défauts :
  - **défaut de factorisation** : I1^F, I1^D, I1^{K*} ;
  - **défaut de détermination** : factorisation possible, mais quotient non unique (la minuterie dormante : ṙ = 3r^{2/3}, solutions « en attente » r_a(t) = 0 pour t ≤ a, (t−a)³ pour t > a).

  Ce second cas n'est pas un quatrième canal causal mais un défaut de clôture déterministe après agrégation. **Il n'est pas exclu par une hypothèse lipschitzienne** : il a un sens, et l'égalité de tous les jets finis interdit de remplacer l'histoire par « davantage de dérivées locales ».
- **𝔐^adm constitutif.** L'historicité dépend aussi de l'espace des histoires auxquelles le système peut être exposé. On conserve la distinction (S, ρ_X, 𝔐^aut) / (S, ρ_X, 𝔐^open) : un même mécanisme peut ne pas manifester d'historicité dans le premier et en manifester dans le second.
- **H^s, typage de s.**
$$
\mathrm H^s_\rho:\ \exists\,x_0,\ \mathcal H_1,\mathcal H_2,\ \mathcal H'\in\mathcal H_1^{-1}\mathfrak M^{adm}\cap\mathcal H_2^{-1}\mathfrak M^{adm}:\ \rho_X(x_1)=\rho_X(x_2),\ \ \pi_{s*}\gamma_{x_1,\mathcal H'}\neq\pi_{s*}\gamma_{x_2,\mathcal H'}.
$$
  - H^s ⇒ H, puisque s est lu par ρ_X.
  - Astérisque : H^s ⇒ « différence structurelle par événement » seulement si ṡ = 0 pendant les flots est déjà imposé. L'ancien I2a devient une **condition de typage** : s est une composante structurelle discrète.
- **G₁ : l'effacement d'événements est autorisé.** La définition générale préserve les trajectoires avec leurs limites à gauche. Les **morphismes événementiels** (qui transportent les macro-transitions K*) forment une sous-classe plus forte.

**Candidat en cours (à casser).** (S, ρ_X, 𝔐^adm) ∈ 𝔍𝔚𝔖 si :
- **C0** — S ∈ 𝔥 ;
- **C1** — s est une composante structurelle discrète, et π_s = r_s∘ρ_X ;
- **C2** — H^{s,max}_ρ (version à préciser ci-dessous : ordre ou calendrier) ;
- **C3** — I2b, efficacité causale de s ;
- **C4** — I3, aucun telos primitif.

Noms C0–C4 proposés pour éviter la collision avec H1–H4 et H. Lecture : *le passé doit pouvoir modifier la restructuration future, et cette restructuration doit compter causalement.* Dans le noyau : histoire → τ → similarités → A⁺ → dynamique future, y compris quand γ₁ = λ = 0.

**Crash-test A — le compteur : ordre ou calendrier ?** Deux lectures de H^s :
- **H^s_t (calendrier)** : les trajectoires de s diffèrent comme fonctions du temps ;
- **H^s_ord (ordre)** : la suite ordonnée des valeurs structurelles visitées diffère.

Témoin : x = (y, h, s), ρ_X = (y, s), h intégrateur caché de l'entrée, Kairos quand h ≥ 1 (s ↦ s+1, h ↦ 0), et la parité de s agit sur ẏ (I2b). Deux histoires mènent au même (y, s) avec des h différents : H^s_t est vraie, mais la suite 0, 1, 2, … ne dépend pas de l'histoire, donc H^s_ord est fausse. L'histoire change *quand* la structure bouge, pas *ce qu'elle devient* : c'est une historicité chronologique.

Penchant : **H^s_ord constitutif**, H^s_t expérimental — cohérent avec le passage de Chronos au temps propre. Bonus technique : s étant constante par morceaux, sa trajectoire modulo reparamétrisation est le mot de ses valeurs successives ; H^s_ord n'exige **aucune définition de G₂**. Pour le noyau, H^s_ord est l'analogue, au niveau des histoires, de `prop:t1-historicite-structurelle` (l'ordre des Kairos change le graphe final) — à démontrer.

**Crash-test B — chaîne ou boucle ?** H^s + I2b donne une *chaîne* passé → structure → reste. Le noyau réalise une *boucle* : A entre dans τ̇ = α tanh(ÃH) − βτ, donc la structure modifie l'écriture des histoires suivantes (« modifiant les conditions de ses traversées futures »). Témoin à sens unique : la mémoire cachée de S₁ décide quand le relais S₂ bascule, et la structure de S₂ n'agit que sur la partie visible de S₂. Ce système satisfait H^s_ord (si les bascules changent la suite) et I2b, sans boucle.

Candidat pour fermer la boucle, **I2b^h** : la structure agit sur la dynamique cachée (F_h dépend de s). Le noyau le satisfait via Ã dans τ̇ (H non homogène). [OUVERT] : exiger la boucle ?

**Crash-test C — transport de H^s : flèches structurelles.** Une flèche observationnelle transporte H^s si ψ_X respecte la structure injectivement : il existe ψ_s avec
$$
r_{s,T}\circ\psi_X=\psi_s\circ r_{s,S},\qquad \psi_s\ \text{injective}.
$$
Ces flèches peuvent effacer les Kairos qui ne restructurent pas, mais pas ceux qui changent s. Hiérarchie des flèches : G₁ générales ⊃ structurelles ⊃ événementielles. Le transport vers l'avant de H^s_ord suit l'esquisse faite pour H.

### 3.14 — H^{s,ord}, typage de la structure, piste pour C5

**Retenu ce tour.**
- H^{s,ord} candidat constitutif. H^s_t conservée comme historicité chronologique structurelle (H^{s,ord} ⇒ H^s_t ; réciproque réfutée par le compteur). Opérateur Ord_s(γ) = red(s(γ)), où red supprime les répétitions consécutives.
- H^{s,ord} ne voit que l'ordre et l'effet des Kairos, ni la date ni la durée : c'est un premier temps intrinsèque, obtenu sans G₂. Relecture du Tome I : l'historicité structurelle, c'est que l'ordre antérieur des Kairos peut produire une autre structure.
- Hiérarchie des flèches G₁ : générales (peuvent effacer tout événement) ⊃ structurelles (ψ_s injective ; n'effacent que les événements tels que s⁻ = s⁺) ⊃ événementielles (préservent l'événement lui-même).
- Candidat C0–C4, et C5 laissée volontairement béante : *la restructuration change-t-elle la manière dont le futur deviendra à son tour passé ?* (« history-dependent structure » contre « history-dependent structure-dependent history formation »). La formulation par « composantes cachées » est rejetée, puisque le caché est relatif à ρ_X et que les fibres ρ_X⁻¹(y) n'ont pas forcément de coordonnées globales. Le système à sens unique est le crash-test canonique de C5.

**Crash-test — fuite par l'horizon.** Avec une continuation de durée finie, le compteur satisfait « Ord ≠ Ord » : trois incréments depuis x₁, deux depuis x₂, d'où (0,1,2,3) ≠ (0,1,2). Du calendrier transformé en longueur de mot par l'horizon. **Correction** : exiger des mots **incomparables pour l'ordre préfixe**,
$$
\mathrm{Ord}_s(\gamma_{x_1,\mathcal H'})\ \perp\ \mathrm{Ord}_s(\gamma_{x_2,\mathcal H'}).
$$
- Le compteur échoue : tous ses mots sont des préfixes de 0, 1, 2, ….
- Invariance par reparamétrisation *et* par horizon (prolonger la continuation ne défait pas une divergence).
- **[PROP] C2 ⇒ restructurations effectives.** Les positions 0 coïncident (s(x₁) = s(x₂) par π_s = r_s∘ρ_X). La divergence est donc à une position k ≥ 1 présente dans les deux mots, et avec ṡ = 0 en flot, chaque futur contient au moins un Kairos tel que s⁺ ≠ s⁻. C1 n'a plus besoin de la clause « peut être modifiée ».
- **Transport** : red∘ψ_s = ψ_s∘red exige l'injectivité de ψ_s (une ψ_s non injective peut fusionner deux lettres consécutives). Avec ψ_s injective, l'incomparabilité est préservée.

**Crash-test — pendule fatigué : que veut dire « structurel » ?** Coordonnées action-angle (E, θ), θ̇ = ω(E) anharmonique. Kairos à chaque tour (θ ≡ 0) : E⁺ = E⁻ + κ(h). Mémoire cachée h alimentée par l'entrée (ḣ = u) et mise à jour aux Kairos. ρ_X = (E, θ), s = E.
- Il satisfait C0–C4 : non-Zénon (période minorée) ; deux histoires d'entrée donnent le même (E, θ) avec des h différents, puis des suites d'énergies divergentes ; ω(E) donne I2b.
- Mais dans les coordonnées naturelles (y, v), aucune composante n'est constante pendant le flot : la « structure » est une intégrale première promue au rang de facteur par un choix de coordonnées. C'est la leçon ỹ = y(1+s) appliquée à C1.
- Problème de typage : I2b exige π_{¬s}, donc une décomposition produit 𝒳 = 𝒮 × X', pas seulement une fonction s.

Deux issues :
- **(a) Structure = mode discret.** s ∈ Q dénombrable, 𝒳 = Q × X' (modes des automates hybrides ; A en est un). Canonique ; exclut les intégrales premières. Mais exclut aussi des poids structurels continus modifiés seulement aux événements.
- **(b) Décomposition structurelle déclarée**, comme ρ_X : objet (S, ρ_X, s, 𝔐^adm). L'appartenance devient relative à la déclaration ; le pendule fatigué est un IWS s'il est présenté en action-angle avec s = E.

(b) est plus conforme à l'anti-essentialisme, (a) plus proche de « structure = organisation ». [OUVERT].

**Piste pour C5 (non axiomatisée).** Formulation par les histoires, sans coordonnées h. W(x) := ensemble des paires d'histoires (ℋ₁, ℋ₂) qui témoignent de H depuis x. C5 candidat : ∃ x, x' ne différant que par s tels que W(x) ≠ W(x') — la structure change quelles histoires laissent des traces distinguables. Réserve : sous cette forme naïve, le système à sens unique peut la satisfaire par sa seule partie visible, puisque le mode du relais change les ρ-présents atteints, donc les paires éligibles, sans toucher à la mémoire de S₁. Il faudrait comparer W(x) et W(x') modulo les différences visibles.

### 3.15 — Déclaration structurelle, tour de projections, C3 et C5 sans identification des fibres

**Retenu ce tour.**
- **Word plutôt que Ord.** Word_s(γ) = red(s∘γ) ∈ 𝒮* (ou 𝒮^ω pour les exécutions infinies). Le cœur de H^{s,ord} est la divergence Word_s(γ₁) ⊥ Word_s(γ₂) (incomparabilité préfixe) : *le passé peut faire bifurquer le mot structurel futur*, pas seulement l'accélérer ou le ralentir. L'injectivité de ψ_s est exactement ce qui empêche une abstraction de recoller deux branches structurelles distinctes.
- **Option (b) retenue.** La structure est déclarée, et non restreinte à un mode dénombrable ; (a) imposerait une restriction ontologique non justifiée (elle exclurait des poids W ∈ ℝ^{N×N} constants en flot et réécrits aux Kairos). Objet présenté : **𝐒 = (S, ρ_X, π_s, 𝔐^adm)**, avec π_s = r_s∘ρ_X. Être IWS n'est pas une propriété du champ nu. Le pendule fatigué devient un crash-test futur de ce que signifie « organisation ».
- **Obstacle.** Avec une simple projection π_s, « même état non structurel » (I2b, donc C3) est mal typé : il faut pouvoir comparer X_s et X_{s'}. C'est gratuit si X = 𝒮 × X_int, pas avec π_s seule. C5 rencontre le même obstacle : puisque π_s = r_s∘ρ_X, s ≠ s' ⇒ ρ_X(x) ≠ ρ_X(x'), donc « neutraliser le visible » demande de quotienter la composante structurelle de la lecture. **Question sous-jacente : qu'est-ce qu'une déclaration structurelle ?** C1 et C3 sont à reprendre ensemble.

**Deux projections, emboîtées (lien avec la note « Opacité, tameness, fibration »).** Le π : 𝒳̂ → 𝒳_obs de la note (fibres = états ou histoires compatibles avec un même présent observable) correspond à **ρ_X** (ou à End au niveau des histoires). La projection qu'appelle C3 est **π_s** (fibres = contenus compatibles avec une structure). Tour :
$$
I\times\mathfrak M^{adm}\xrightarrow{\mathrm{End}}\mathcal X\xrightarrow{\rho_X}Y\xrightarrow{r_s}\mathcal S.
$$
- fibres de ρ_X : l'opacité ;
- fibres de π_s : l'organisation ;
- H vit dans les fibres de ρ_X : la partition comportementale (Nerode) des points atteints d'une fibre n'est pas triviale.

La note contenait déjà la tour : ses strates naturelles (« graphe fixé », régimes, surfaces de Kairos) stratifient la base Y par r_s, et les fibres portent l'opacité. **Reformulation de la promesse** : *opacité sans sauvagerie = la partition comportementale des fibres de ρ_X est définissable* (types de mémoire en nombre fini par région — Hardt appliqué à ρ_X, pas à π_s).

**C3 sans identification des fibres.** Trois manières de comparer X_s et X_{s'} :
- **identification existentielle** : trivialise C3 (une bijection non conjuguante fabrique des témoins même si les dynamiques des fibres sont conjuguées — leçon ỹ = y(1+s), troisième occurrence) ;
- **identification déclarée** (π_int, trivialisation) : c'est déjà une connexion. Les trivialisations de Hardt ne sont pas canoniques, et C3 n'est pas invariant par changement de trivialisation en général ;
- **comparaison de répertoires** : on déclare le découpage de *ce qu'on lit*, pas de *ce qui est*, ρ_X = (π_s, ρ_int), et
$$
\mathrm{Rep}(s)=\{R^{\rho_{\mathrm{int}}}_x : x\in X_s\cap\mathrm{Supp}\},\qquad \mathbf{C3^{rep}}:\ \exists\,s\neq s'\ \text{atteignables},\ \mathrm{Rep}(s)\neq\mathrm{Rep}(s').
$$

C3^rep dit que changer de structure change ce que le système *peut* faire, lu hors de s. Les trois canaux (F, D, K*) sont inclus. Crash-tests :
- S_Δ échoue (A décoratif, répertoires égaux) ;
- le compteur passe (pente initiale a sur les fibres paires, b sur les impaires) ;
- le noyau passe vraisemblablement ;
- le pendule fatigué passe (ω(E) change la vitesse lue de θ), conformément au choix (b).

**Différence avec un C3 « produit »** : une structure qui ne fait que permuter les comportements entre contenus internes (relabeling caché préservant ρ_int) est efficace à contenu fixé, mais décorative pour C3^rep. Penchant : C3^rep, puisqu'aucune expérience ne distingue la structure autrement qu'en lisant s. Choix à faire en connaissance de cause. **Condition à crash-tester** : la lecture séparée ρ_X = (π_s, ρ_int). Le noyau la satisfait (A ; H, V, P) ; une lecture mêlant structure et contenu (par exemple ÃH) devrait être redéclarée.

**C5 sans identification (candidat).** Pour neutraliser la contamination, on quantifie universellement sur l'autre fibre :
$$
\mathbf{C5}:\ \exists\,x\in X_s,\ \mathcal H_1,\mathcal H_2:\ \rho_X(\mathrm{End}(x,\mathcal H_1))=\rho_X(\mathrm{End}(x,\mathcal H_2))\ \text{et les deux fins sont séparables},
$$
tandis que pour **tout** x' ∈ X_{s'} avec ρ_int(x') = ρ_int(x) où ℋ₁ et ℋ₂ fusionnent aussi visiblement, les deux fins sont Nerode-équivalentes. *La structure décide si une distinction cachée, produite par deux histoires visiblement équivalentes, survit.*
- le système à sens unique échoue (prendre x' avec la même mémoire de S₁ : le témoin persiste quel que soit le mode du relais) ;
- le noyau a une chance de passer (Ã entre dans τ̇) ;
- condition forte, peut-être trop ; mais intrinsèque (lectures et réponses seulement).

**Principe méthodologique.** Comparer des fibres par des ensembles de comportements, avec des quantificateurs ∃/∀, permet de *différer* le fibré. Une identification des fibres (une connexion) ne deviendra nécessaire que pour des énoncés ponctuels du type « même contenu interne » ; ni C3 ni C5 ne l'exigent pour l'instant. Quand le fibré entrera, la note dit déjà où : au-dessus de Y pour l'opacité, avec 𝒮 comme stratification de la base.

### 3.16 — Relecture de la V5 (.tex)

**État.** La V5 intègre : présentation 𝐒 = (S, ρ_X, 𝔐^adm) avec lecture séparée ρ_X = (π_s, ρ_int) ; tour End → ρ_X → r_s ; fibres d'opacité et d'organisation ; H^{s,ord} par divergence de mots ; C3^rep ; candidat C0–C4 ; taxonomie à trois canaux et défaut de détermination ; G₀/G₁ avec bords de cascade ; flèches G₁ ⊃ structurelles ⊃ événementielles ; C5 et G₂ ouverts ; réserve géométrique. Exec est désormais inclus dans les données de S lorsqu'il ne se déduit pas de (C, F, D, K).

**1. Trou entre texte et définition : C2 et C3 ne sont pas reliés.** La ligne 257 affirme que « la structure ainsi distinguée doit compter », mais C3 porte sur deux structures atteignables quelconques. Contre-exemple (**juxtaposition interne**) :
- modes a, b, c, d ;
- une mémoire cachée décide a → b ou a → c : les mots (a,b) et (a,c) divergent, C2 ✓ ;
- Rep(b) = Rep(c) ;
- Rep(a) ≠ Rep(d) : C3 ✓.

C0–C4 sont satisfaits alors que l'histoire ne choisit qu'entre des branches décoratives. **Correction proposée** :
$$
\mathbf{C23}:\ \text{témoin de }H^{s,\mathrm{ord},\max}\ \text{tel qu'à la première position de divergence }k,\ \mathrm{Rep}(s^{(1)}_k)\neq\mathrm{Rep}(s^{(2)}_k).
$$
C23 ⇒ C3 (redondant) ; candidat : C0, C1, C23, C4. Crash-tests :
- compteur et juxtaposition : échouent déjà à C2 ;
- juxtaposition interne : échoue ;
- noyau : passe si deux ordres de recâblage mènent à des graphes de répertoires distincts (plausible).

**2. Ligne structurelle de la taxonomie mal typée.** I2^F, I2^D et I2^{K*} utilisaient π_{¬s}, abandonné en V5. Retypage par la lecture :
$$
\mathrm{I2}^F:\ \exists\,x_1,x_2:\ \rho_{\mathrm{int}}(x_1)=\rho_{\mathrm{int}}(x_2),\ \pi_s(x_1)\neq\pi_s(x_2),\ \mathcal L_F\rho_{\mathrm{int}}(x_1)\neq\mathcal L_F\rho_{\mathrm{int}}(x_2)
$$
(idem pour D et K*). Réserve à écrire : x₁ et x₂ peuvent aussi différer en contenu caché, donc l'attribution à s n'est pas ponctuelle — acceptable pour une taxonomie explicative.

**3. C3^rep n'est pas monotone en régime.** Une structure qui permute les contenus cachés sur toute sa fibre est décorative dans le régime maximal, mais peut devenir efficace dans un régime restreint. Le choix du régime maximal est cohérent avec la ligne 234 (permutation = décoratif), mais il ne découle plus de la monotonie : à dire explicitement. Avec I = C, Supp = C, donc « ∩ Supp » et « atteignables » sont vides de contenu dans C3 — à assumer ou à re-régimer.

**4. Transport de l'appartenance.** La proposition du §9 transporte C2. C3^rep n'est pas transporté vers l'avant en général : la cible peut avoir plus d'états par fibre, et les répertoires peuvent s'y égaliser. L'appartenance est invariante par isomorphisme structurel observationnel (f, ψ_X et ψ_s bijectifs), mais pas transportée par une flèche structurelle quelconque.

**5. Retouches.**
- §3 : écrire Y = 𝒮 × Y_int, r_s = pr₁ (lien entre la ligne 109 et la tour de la ligne 123).
- End en G₁ = état post-cascade, sinon x_k ∈ D possible ; la remarque de la ligne 198 en dépend implicitement.
- Ligne 312 : poser γ⁻(0) := x₀ quand x₀ ∈ D.
- §9 : ajouter f(C_S) ⊆ C_T (régime maximal I = C) et intégrer la condition de préservation des exécutions, aujourd'hui seulement au §8.1.
- Ajouter la remarque C2 ⇒ H^max_ρ (ρ_X lit s).
- Ligne 503 : « les conditions de ses traversées ultérieures » est le contenu de C5 (ouvert) — marquer comme horizon ou retirer.

### 3.17 — Relecture de la V5.1

**Corrections intégrées depuis la V5 :**
- C23 (C2 et C3 fusionnés) et crash-test de la juxtaposition interne ;
- ligne structurelle de la taxonomie retypée par les lectures, avec sa réserve d'attribution ;
- régime maximal des répertoires assumé comme choix, sans argument de monotonie ;
- transport limité à la divergence structurelle, avec invariance par isomorphisme ;
- Y = 𝒮 × Y_int et r_s = pr₁ ; End post-cascade ; γ⁻(0) := x₀ ;
- flèches complètes (f(C_S) ⊆ C_T, η monoïdal, préservation des exécutions) ;
- C23 ⇒ H^{s,ord,max} ⇒ H^max ;
- fin de texte : la boucle (C5) est présentée comme horizon.

**1. Invariance par isomorphisme : ψ_X doit respecter la lecture séparée.** En général ψ_X(s, y) = (ψ_s(s), ψ_int(s, y)), dont la partie interne dépend de s. Un ré-étiquetage des lectures internes dépendant de la structure peut égaliser dans T des répertoires distincts dans S (Rep_S(s') = 2·Rep_S(s), ψ_int(s', y) = y/2). Il faut
$$
\psi_X=\psi_s\times\psi_{\mathrm{int}}.
$$
Sens de fond : Y = 𝒮 × Y_int est *l'identification minimale déclarée* — des lectures internes d'une fibre à l'autre, pas des états. Les flèches doivent la préserver pour que C23 reste comparable.

**2. L'admissibilité a disparu du texte.**
- « Supp = C » (ligne 216) exige Reach ⊆ C, c'est-à-dire l'invariance de C (priorité au premier contact, ∂_exit C ⊆ D, K(C∩D) ⊆ C, C et D fermés). Présente en V4, elle est absente de la V5.1 : à réintroduire dans le socle, comme hypothèse ou comme lemme.
- Rep^max(s) doit porter sur x ∈ X_s ∩ C, et non sur X_s.

**3. C23 relie des structures, pas les états atteints.** Rep^max compare des fibres entières. La différence entre b et c peut tenir à une région des fibres jamais visitée par la branche historique, alors que les états effectivement atteints ont les mêmes futurs lus (juxtaposition interne déplacée *dans* les fibres). Deux lectures :
- **efficacité potentielle** — l'histoire choisit entre deux organisations distinctes ; c'est la lecture actuelle, cohérente avec le régime maximal ;
- **efficacité actualisée** — il faut en plus que les futurs lus depuis les états atteints diffèrent.

La tension disparaît si 𝔐^adm donne accès, depuis les états atteints, aux régions discriminantes. Choix à nommer dans la V5.2.

**4. [PROP, candidate — plan de preuve] C23 pour le noyau au point γ₁ = λ = 0, ζ > 0.** Le cas qu'on craignait d'exclure est le plus simple.
- **Répertoires, pour tout A ≠ A'.** Ã détermine A (motif hors diagonale), donc Ã ≠ Ã'. Il existe H non homogène avec ÃH ≠ Ã'H, et tanh(ÃH) ≠ tanh(Ã'H). Soit x ∈ X_A ∩ C avec V = 0 et P petit. Comme V̇(0) = −H + ζ tanh(ÃH) + u ne dépend pas de τ, tout x' ∈ X_{A'} de même (H, V, P) a un V̇(0) différent sous la même entrée. Donc R_x ∉ Rep^max(A'), et Rep^max(A) ≠ Rep^max(A'). (Pour H homogène, ÃH = H : cohérent avec S_Δ.)
- **Bifurcation.** Deux histoires d'entrée, issues d'un même x₀, mènent au même (H, V, P, A) avec des τ différents. Comme τ n'entre pas dans le flot, les trajectoires de (H, V, P) coïncident jusqu'au Kairos suivant : même i*, même instant. Seules les similarités de traces diffèrent ; si leur classement change, A⁺ diffère et les mots divergent en position 1. Le point précédent rend les répertoires des deux nouveaux graphes distincts.
- **Restes à établir.** Atteignabilité : pilotage de (H, V) par u (actionné directement sur V̇), ajustement de P, pas de Kairos pendant les préfixes (P < Θ), changement de classement avec m > 0.
- **Cas γ₁, λ > 0.** Plus difficile : τ entre dans V̇ et peut compenser partiellement l'effet du graphe dans l'argument sur les répertoires.

### 3.18 — Après la relecture V5.1 : décisions et précisions

**Décisions.**
- **Isomorphisme de présentations** : ψ_X = ψ_s × ψ_int, avec ψ_int indépendant de s. Avec f, ψ_s, ψ_int bijectifs et un transport adéquat des histoires, C23 est invariant. *On ne compare pas les états à travers les structures ; on compare ce qu'on a déclaré comparable dans leurs lectures.*
- **Admissibilité** (régression accidentelle de la V5, à réparer). Propriété requise : x₀ ∈ C, ℋ ∈ 𝔐^adm_{x₀} ⇒ γ_{x₀,ℋ}(t,j) ∈ C sur tout le domaine. Elle est distincte des conditions suffisantes utilisées pour le noyau (C, D fermés ; priorité au premier contact ; ∂_exit ⊆ D ; K(C∩D) ⊆ C). Alors Supp^max = C et Rep^max(s) = {R_x : x ∈ X_s ∩ C}.
- **C23 = efficacité structurelle potentielle**, nommée comme telle. La version actualisée est définie à côté, sans être axiomatisée.

**Correction : C23^act ne doit pas être « les états atteints ont des futurs distinguables ».** Cette version est incomparable avec C23^pot : pour une structure qui permute les contenus cachés, les répertoires sont égaux (C23^pot faux) alors que les états atteints ont des futurs distincts par leur contenu caché (C23^act vrai). Elle mesure donc une différence de contenu, pas une efficacité structurelle. Version retenue :
$$
\mathbf{C23^{act}}:\quad R^{\rho_{\mathrm{int}}}_{x^{(1)}_k}\notin\mathrm{Rep}^{\max}\bigl(s^{(2)}_k\bigr)\ \ (\text{ou symétriquement}).
$$
Le comportement de l'état réellement produit est impossible sous l'autre organisation. On a C23^act ⇒ C23^pot strictement, et le cas de la permutation est exclu. Crash-test futur : IWS exige-t-il l'efficacité actualisée, ou la capacité comportementale de l'organisation suffit-elle ?

**Noyau, γ₁ = λ = 0 : précisions de preuve.**
- **R_x ∉ Rep^max(A') — étape à écrire explicitement.** L'égalité des réponses impose la même lecture initiale, donc x' a les mêmes (H, V, P). Comme V̇ = −γ₀V − H + ζ tanh(ÃH) + u ne contient pas τ (pour tout V, pas seulement V = 0), aucun τ' ne compense ζ(tanh(ÃH) − tanh(Ã'H)). Prendre une continuation de durée positive (attente, u = 0) pour convertir la différence de dérivée en différence de trajectoire.
- **Version actualisée probablement gratuite.** Il suffit que le H atteint au Kairos vérifie (Ã₁⁺ − Ã₂⁺)H ≠ 0. C'est générique, puisque le recâblage de i* échange des voisins de H différents ; sinon, l'entrée pilote H vers une configuration discriminante.
- **Fenêtre de pertinence.** Sous la continuation commune, le forçage de τ est identique, donc τ₁(t) − τ₂(t) = e^{−βt}(τ₁(0) − τ₂(0)). La différence historique s'efface exponentiellement devant la partie commune, et la similarité est un cosinus. Le Kairos commun doit survenir avant que Δτ devienne négligeable. Avec l'oubli β, l'historicité structurelle a une *durée de validité*.
- **Plan de preuve localisé.** Construire ℋ₁ et ℋ₂ depuis un même x₀ qui : (1) aboutissent à la même lecture (A, H, V, P) ; (2) produisent τ₁ ≠ τ₂ avec des classements différents ; (3) restent sous Θ pendant l'écriture ; (4) déclenchent ensuite un Kairos commun, dans la fenêtre de pertinence ; (5) avec m > 0. Alors atteignabilité + changement de classement ⇒ C23.

**Taxonomie : deux formes de mémoire silencieuse, à ne pas confondre.**
- Noyau γ₁ = λ = 0 : **défaut de factorisation, colonne K*** (I1^{K*} sans I1^F) — muette dans le flot, décisive au saut. C'est l'exemple pur de cette colonne.
- Minuterie dormante : **défaut de détermination** — factorisation exacte dans tous les canaux, quotient non unique.

*Une trace n'a pas besoin d'influencer continûment le présent pour être historiquement causale : elle peut rester silencieuse pendant le flot et devenir décisive au Kairos.*

### 3.19 — Relecture de la V5.2

Intégré : invariance d'admissibilité dans le socle (propriété distinguée de ses conditions suffisantes), Rep^max sur X_s ∩ C, ψ_X = ψ_s × ψ_int, invariance par isomorphisme avec ψ_int, C23^pot nommé, C23^act (appartenance au répertoire de l'autre branche), proposition sur le noyau (γ₁ = λ = 0) avec fenêtre de pertinence, distinction colonne K* / défaut de détermination.

Reste à reprendre :
- **Étiquettes « V5.1 » résiduelles** : lignes 15, 41, 554, 573, 575.
- **Deux notions de continuation admissible.** H et C23 utilisent des continuations définies par préfixe (ℋ₀⁻¹𝔐^adm) ; Rep utilise des histoires admissibles depuis un état (𝔐^adm_x). Pour que C23 soit cohérent, il faut une propriété markovienne de l'admissibilité, à mettre dans le socle : ℋ₀⁻¹𝔐^adm_{x₀} = 𝔐^adm_{End(x₀,ℋ₀)}. Vraie dans le noyau (entrées mesurables bornées). Par ailleurs, 𝔐^adm_{x₀} est utilisé ligne 77 avant sa définition ligne 212.
- **Définition des flèches structurelles redondante.** Avec ψ_X = ψ_s × ψ_int, l'égalité r_{s,T}∘ψ_X = ψ_s∘r_{s,S} est automatique. Définition plus simple : flèche observationnelle avec ψ_X produit et ψ_s injective.
- **Proposition sur le noyau.** Préciser que H est la lecture de l'état post-cascade à la bifurcation. La condition (Ã₁⁺ − Ã₂⁺)H ≠ 0 porte, sur la ligne i*, sur des *sommes* : Σ_{j∈N₁∖N₂} H_j ≠ Σ_{j∈N₂∖N₁} H_j (le degré de i* est le même dans les deux branches, puisque le recâblage est conservatif). Les lignes des voisins échangés offrent d'autres chances de discrimination. « Dès que les composantes pertinentes de H ne coïncident pas » est donc un peu trop fort.

### 3.20 — Relecture de la V5.2.1

Intégré : 𝔐^adm_x défini dès le socle, compatibilité préfixe–état, flèches structurelles simplifiées (ψ_X produit + ψ_s injective, commutation notée automatique), H post-cascade dans la proposition, condition H ∉ ker(Ã₁⁺ − Ã₂⁺) et forme en sommes, étiquettes de version.

**Point principal : l'union 𝔐^adm = ⋃_x 𝔐^adm_x est utilisée là où il faut la famille indexée par l'état.**
- **Définitions de H et H^{s,ord}** (lignes 157–171, 196) : ℋ_k ∈ 𝔅 ⊆ 𝔐^adm ne garantit pas que ℋ_k soit exécutable depuis x₀. De plus, ℋ₁⁻¹𝔐^adm = {ℋ : ℋ₁·ℋ ∈ 𝔐^adm_y pour un certain y} peut contenir des continuations inexécutables depuis x₁. Correction : 𝔅_{x₀} := 𝔅 ∩ 𝔐^adm_{x₀}, ℋ_k ∈ 𝔅_{x₀}, ℋ' ∈ ℋ₁⁻¹𝔅_{x₀} ∩ ℋ₂⁻¹𝔅_{x₀} ; dans le régime maximal, par compatibilité, cela donne 𝔐^adm_{x₁} ∩ 𝔐^adm_{x₂}.
- **Tour** (ligne 139) : End est défini sur {(x, ℋ) : ℋ ∈ 𝔐^adm_x}, pas sur I × 𝔐^adm.
- **Flèches** (ligne 456) : η(𝔐^adm_S) ⊆ 𝔐^adm_T doit devenir η(𝔐^adm_{S,x}) ⊆ 𝔐^adm_{T,f(x)}, sinon l'histoire transportée peut être inexécutable depuis f(x).
- **Présentation** (ligne 121) : elle doit porter la famille (𝔐^adm_x)_{x∈C} ; l'union perd l'information d'exécutabilité.

**Retouches.** Ligne 222 : 𝒳 ∩ C = C. Ligne 505 : préciser aussi l'absence de témoin I1^D (D = {∃i : P_i ≥ Θ} est lu par ρ, donc saturé), pour que le cas soit bien « pur K* ».

### 3.21 — Atteignabilité du témoin (noyau, γ₁ = λ = 0, ζ > 0) : construction par symétrie

**Levier : H est une sortie plate de (H, V).** Pour tout chemin H(·) de classe C², l'entrée u = Ḧ + γ₀Ḣ + H − ζ tanh(ÃH) le réalise, et elle est bornée pour une petite amplitude. τ et P ne sont alors que des fonctionnelles du chemin :
$$
\tau_i(T)=e^{-\beta T}\tau_i(0)+\alpha\!\int_0^T\! e^{-\beta(T-s)}\tanh((\widetilde AH)_i)\,ds,\qquad
\dot P_i=\kappa_1\|H_i\|+\kappa_2\|V_i\|-\kappa_3P_i.
$$

**[PROP, candidate] Écrire dans τ et revenir au même (H, V, P) : réflexion.** On part de x₀ = (H = 0, V = 0, τ₀, P₀, A), avec P₀ < Θ. Branche 1 : une boucle H¹ de 0 à 0, à vitesse nulle aux deux bouts. Branche 2 : H² = −H¹ (d'où u² = −u¹, par imparité de tanh). Alors :
- H(T) = 0 et V(T) = 0 dans les deux branches ;
- P¹(T) = P²(T) exactement, puisque Ṗ ne voit que des normes, paires ;
- A est inchangé (pas de Kairos si l'amplitude est petite) ;
- τ^{1,2}(T) = e^{−βT}τ₀ ± I avec I = α∫e^{−β(T−s)} tanh(ÃH¹) ds, donc τ¹ − τ² = 2I ≠ 0 dès que l'excursion garde un signe sur un (ÃH)_j.

*P est aveugle au signe, τ ne l'est pas : c'est exactement ce qui permet d'écrire sans laisser de trace lue.*

**Piège 1 — invariance du cosinus.** Si τ₀ = 0, alors τ² = −τ¹ globalement, et cos(−a, −b) = cos(a, b) : tous les classements coïncident. La symétrie qui égalise P égalise aussi les similarités. Correction : une partie commune non nulle, c = e^{−βT}τ₀ ≠ 0 (ou apportée par la continuation), puis comparer c + I et c − I.
- d = 1 : la similarité vaut sign(τ_{i*}τ_j). Il suffit que |I_j| > |c_j| (le signe de τ_j bascule entre les branches) et |I_{i*}| < |c_{i*}| (celui de i* ne bascule pas).
- d ≥ 2 : générique.

**Piège 2 — l'écriture doit être localisable.** Il faut (ÃH)_{i*} ≈ 0 tout en ayant (ÃH)_j ≠ 0. C'est possible dès que les lignes i* et j de Ã sont distinctes, c'est-à-dire que i* et j ne sont pas *jumeaux* (N[i*] ≠ N[j], voisinages fermés). Deux lignes stochastiques distinctes sont linéairement indépendantes.

**Piège 3 — le changement doit traverser la coupure de sélection.** Le saut retire les m voisins de plus faible similarité et ajoute les m non-voisins de plus forte similarité, avec m = min(2, |N|, |N^c|). Si |N(i*)| = m, tous les voisins sont retirés quel que soit le classement (idem pour N^c). Il faut donc plus de m candidats du côté concerné (par exemple deg(i*) ≥ 3 avec m = 2), et que l'*ensemble sélectionné* change, pas seulement l'ordre interne.

**Fenêtre de pertinence.** Préparer P_{i*}(T) juste sous Θ, en faisant monter ‖H_{i*}‖ pendant la boucle tandis que les voisins, en opposition, maintiennent (ÃH)_{i*} ≈ 0. On garantit aussi P_j(T) < P_{i*}(T) pour que i* saute le premier. Une continuation commune courte (durée Δ) déclenche alors le Kairos : e^{−βΔ} ≈ 1 et la partie commune ajoutée est en O(Δ), donc les inégalités de classement, stricte avec marge, persistent. Contrainte : u_max borne la vitesse de montée de P, d'où l'intérêt de partir près du seuil.

**Dernière marche (H discriminant).** Les inégalités de classement sont strictes, donc ouvertes. On perturbe légèrement le chemin de la continuation pour que H(t*) ∉ ker(Ã₁⁺ − Ã₂⁺), qui est un sous-espace propre. Généricité.

**Reste à vérifier en détail.** Compatibilité quantitative entre amplitude (u ≤ u_max, P < Θ pendant le préfixe), montée de P_{i*} près du seuil, et marge du classement. Choix d'un graphe concret (N ≥ 5 environ, deg(i*) = 3, sans jumeaux). Un cas numérique minimal permettrait de contrôler les marges avant la rédaction de la preuve.

### 3.22 — Témoin numérique N = 6 [NUM] (script `temoin_C23_noyau.py`)

Graphe : arêtes (0,1),(0,2),(0,3),(1,4),(2,5),(3,4),(3,5),(4,5). i* = 0, N(i*) = {1,2,3}, N^c = {4,5}, m = 2, pas de jumeaux, Ã inversible. Paramètres Annexe F, γ₁ = λ = 0. Boucle H^± = ±amp·sin²(πt/T)·v, T = 3, avec Ãv = w supporté sur {1,2}, donc (Ãh)_{i*} = 0 exactement. Continuation commune : u_{i*} = (U, 0), le reste nul.

Résultats (amp = 0,2, U = 2,5) : max P pendant la boucle 0,574 < Θ ; max|u| = 1,33 ; écart (H,V,P) entre branches à T ~1e−13 ; τ⁺ − τ⁻ = (0, −0,224) sur les nœuds 1 et 2 seulement. Kairos à t* = 1,446 dans les deux branches, seul le nœud 0 au seuil. Classement 1 ↔ 2 inversé (cos 0,9915 / 0,9462). Branche + : retire {3,2} ; branche − : retire {3,1} ; les deux ajoutent {4,5}. A₁⁺ ≠ A₂⁺, marge 0,045. ‖(Ã₁⁺ − Ã₂⁺)H‖ = 0,93 et ‖ΔV̇‖ = 0,64 au même (H,V).

Balayage amp ∈ {0,05 ; 0,1 ; 0,2 ; 0,3} × U ∈ {1,5 ; 2,5 ; 4} et ζ ∈ {0,4 ; 0,8 ; 1,2} : A₁⁺ ≠ A₂⁺ partout. La marge est ≈ linéaire en amp (0,012 à 0,05 ; 0,063 à 0,3), avec max P ≈ 2,87·amp. Il n'y a donc pas de verrou quantitatif : toute amp ∈ (0 ; 0,43) convient. Seule la marge est proportionnelle à l'amplitude.

Argument C23^act (indépendant du τ testé) : si x′ ∈ X_{A₂⁺} ∩ C a la même lecture initiale, alors (H,V,P)(x′) = (H,V,P)(x₁). Sous u = 0, V̇(0⁺) diffère de ζ[tanh(Ã₁⁺H) − tanh(Ã₂⁺H)] ≠ 0, quel que soit τ(x′), puisque τ n'entre pas dans (H,V,P) et qu'aucun saut n'est possible avant que P n'atteigne Θ. Donc R_{x₁} ∉ Rep^max(A₂⁺).

### 3.23 — Identifiabilité universelle de la structure ; borne sur u

**[PROP] Lemme d'identifiabilité (noyau, γ₁ = λ = 0, ζ > 0).** Pour A ≠ A′ et tout x ∈ X_A ∩ C hors de D : R_x ∉ Rep^max(A′). La preuve procède par l'absurde avec des entrées constantes de norme ≤ ε, pour un ε > 0 quelconque.

- Si les lectures coïncidaient, on aurait (H,V) égaux sur un intervalle, donc K := (Ã − Ã′) vérifierait K·H(t) ≡ 0.
- Les dérivées successives donnent alors K·H(0) = 0, puis K·V(0) = 0, puis K·(ζ tanh(ÃH(0)) + u₀) = 0, et ce pour tout u₀ de la boule.
- Cela impose K = 0, puis A = A′ (A ↦ Ã est injective), ce qui est contradictoire.

**Version verrouillée (Benoit).**

- L'égalité des lectures donne ζ tanh(BH) = ζ tanh(B′H). Par injectivité de tanh, KH ≡ 0, donc KV ≡ 0, puis K V̇ ≡ 0. On obtient ζK tanh(BH(0)) + Ku₀ = 0 pour tout u₀ de la boule, donc K(u₀ − u₁) = 0, donc K = 0. Aucune dérivée d'ordre supérieur n'est nécessaire.
- Hypothèses à expliciter :
  - (i) D est ρ_int-lisible (il ne dépend que de P), donc x′ ∉ D et les deux flots durent le même temps avant tout saut ;
  - (ii) 𝔐^adm_x contient les constantes d'une boule de ℝ^{N×d}, c'est-à-dire une actuation complète. Avec une actuation partielle, on n'obtient que K·(colonnes actionnées) = 0, et il faut un argument de propagation par tanh(BH) ;
  - (iii) le support hors diagonale de Ã est celui de A.
- **Vérification dans les textes.**
  - L'Annexe F ne fixe aucune convention sur u : pas de u_max dans le tableau de référence, et les notations u₁, u_⊥ y désignent des directions d'exposition.
  - Tome I, « Équations » : entrée u_i(t) ∈ ℝ^d par nœud, exogène, mesurable, bornée, ‖u_i(t)‖ ≤ u_max. L'actuation est donc complète, ce qui valide (ii).
  - Tome I, C/D : D = {∃i, P_i ≥ Θ}, ce qui valide (i).
  - Annexe A et Tome I (existence) : « toute entrée mesurable essentiellement bornée ». u_max y fonctionne comme la borne de l'entrée considérée (B = ζ√d + u_max), pas comme un paramètre fixé. L'ambiguïté est à lever dans le texte.
- Sans Kairos accessible (u_max < u_crit), τ est une mémoire morte : π_s est constante, donc H^{s,ord} échoue et même H_ρ échoue. Le noyau reste dans 𝔥 mais n'est pas IWS pour cette présentation et cette admissibilité.

Conséquences :

- La condition « H discriminant » disparaît du témoin : A₁⁺ ≠ A₂⁺ suffit pour obtenir C23^act.
- Toute la difficulté du témoin porte sur l'historicité (écriture dans τ, recâblage). L'efficacité est gratuite dès que ζ > 0, ce qui en fait le cas pur I1^{K*}.
- Le lemme n'exige que u_max > 0.

**Borne sur u [NUM].**

- Si 𝔐^adm est la classe des entrées mesurables bornées sans borne fixée, rien n'est à ajouter.
- Avec une borne fixée, la phase d'écriture (‖u_a‖ = O(a)) et le lemme d'identifiabilité passent pour tout u_max > 0.
- En revanche, atteindre le Kairos demande une borne u_max > u_crit. Depuis le repos, avec un forçage résonant du seul nœud 0 (|u| ≤ U), on atteint max P = 1,14 < Θ pour U = 0,3 ; pour U = 0,5, on atteint Θ à t = 6,5. Donc u_crit ≲ 0,33 pour cette stratégie : c'est une borne supérieure, pas l'optimum.
- [CONJ] u_crit > 0 : ζ < 1 et ‖Ã‖_∞ = 1 donnent une non-linéarité contractante, donc pour une borne sur u petite l'état reste près de l'origine et P reste sous Θ.

### 3.24 — Relecture de la V5.3

Les trois points de la relecture V5.2.1 sont intégrés : famille indexée (𝔐^adm_x)_{x∈C} dès le socle (l'union n'est plus utilisée pour typer quoi que ce soit), 𝒳 ∩ C = C trivialement résorbé par construction, I1_ρ^D explicitement écarté dans le crash-test noyau. La convention sur u (L^∞, u_max = ess sup d'une entrée donnée et non un paramètre du modèle) est maintenant énoncée dans le texte, conforme à la vérification faite sur le Tome I et l'Annexe A.

**Le lemme d'identifiabilité est correctement verrouillé.** La preuve suit exactement la version de Benoit : KH(t) = 0 par injectivité de tanh, puis KV(t) = 0 par dérivation, puis Ku₀ = −ζK tanh(BH(0)) par une deuxième dérivation, puis K = 0 en faisant varier u₀ dans une boule. Un point technique que je m'attendais à devoir soulever est déjà traité correctement dans le texte : rien ne suppose x′ ∈ C \ D a priori ; c'est ρ_int(x) = ρ_int(x′) (même réponse) qui force P(x′) = P(x) < Θ, donc x′ ∉ D. Bien vu.

**Un point à ajouter, mineur.** Le corollaire visé — Rep^max(A) ≠ Rep^max(A′) pour A ≠ A′ — suppose X_A ∩ (C\D) ≠ ∅. C'est trivial (H = V = P = 0 convient toujours), mais ce n'est pas dit. Une phrase suffit, par exemple après la Proposition : « Comme (0,0,τ,0) ∈ X_A ∩ (C\D) pour tout A et tout τ, on a immédiatement Rep^max(A) ≠ Rep^max(A′). »

**Un point d'organisation, à juger.** L'hypothèse de « voisinage de zéro d'entrées constantes admissibles » (fin de la section « Admissibilité et histoires ») est énoncée comme une précision générale du socle, mais elle n'est justifiée que pour le noyau (coordonnées u_i par nœud). Si un autre exemple d'IWS avait une actuation partielle, cette phrase serait fausse pour lui alors qu'elle est rédigée hors de tout exemple. Je proposerais de la déplacer dans le crash-test noyau, à côté de la Proposition d'identifiabilité, en la formulant comme une hypothèse vérifiée pour cet exemple plutôt que comme un fait du socle général — mais ce n'est qu'une question de placement, pas de contenu.

Rien d'autre à signaler : taxonomie, granularités G₀/G₁, flèches structurelles, crash-tests (compteur, juxtapositions, pendule, S_Δ) et les deux questions ouvertes (C5, G₂) sont cohérents avec les échanges précédents.

### 3.25 — Relecture de la V5.3.2

Les deux points mineurs de la 3.11 sont traités. Le corollaire Rep^max(A) ≠ Rep^max(A′) est maintenant justifié par la non-vacuité de X_A ∩ (C\D) (état H=V=P=0). L'hypothèse du voisinage de zéro d'entrées constantes est déplacée dans le crash-test noyau, avec la précision « propriété du noyau, non hypothèse du socle général ». La figure tikz du recâblage (graphe A, A₁⁺, A₂⁺ avec sommet double i* et arêtes ajoutées/retirées) rend le témoin N=6 lisible d'un coup d'œil ; rien à redire dessus.

## 4. Nouveau chantier — quotient de Nerode sur les fibres d'opacité

Proposition de Benoit : sur une fibre F_y = ρ_X⁻¹(y), poser x ∼_N x′ ssi mêmes continuations admissibles et mêmes réponses futures, et étudier F_y/∼_N, puis sa variation en y.

**Formalisation proposée.** x ∼_N x′ ssi 𝔐^adm_x = 𝔐^adm_{x′} et R_x^{ρ_int} = R_{x′}^{ρ_int} comme fonctions (même domaine, mêmes valeurs). C'est exactement dire que x et x′ ont la même réponse interne au sens déjà utilisé pour Rep^max, mais comparée *à l'intérieur d'une seule fibre d'opacité*, alors que Rep^max(s) compare déjà, en les regroupant en un ensemble, les R_x sur toute une fibre d'organisation X_s ∩ C (donc sur tous les y_int en même temps). Le quotient F_y/∼_N est donc un raffinement strictement plus fin, un niveau intermédiaire entre l'état brut et Rep^max :
\[
\text{état}\ \longrightarrow\ F_y/\sim_N\ \longrightarrow\ \Rep^{\max}(s).
\]

**Remarque sur l'exigence de domaine.** Benoit a raison de l'imposer : sans elle, x et x′ pourraient coïncider sur 𝔐^adm_x ∩ 𝔐^adm_{x′} tout en ayant des répertoires de continuations différents, ce qui n'est pas une vraie indiscernabilité comportementale. Une variante plus faible mériterait d'être gardée en réserve : un préordre de simulation x ⪯ x′ ssi 𝔐^adm_x ⊆ 𝔐^adm_{x′} et R_{x′}|_{𝔐^adm_x} = R_x (x′ a au moins tout le comportement de x, plus éventuellement plus de continuations disponibles). C'est la version classique en théorie des automates à fonction de transition partielle, et elle pourrait être ce dont C5 a besoin plutôt que l'équivalence stricte.

**Dans le noyau, la contrainte de domaine est automatique.** 𝔐^adm_x ne dépend que de x ∈ D ou non (donc de P), pas de τ : toute entrée bornée est exécutable depuis tout x ∈ C, par la borne de non-explosion. Deux états d'une même fibre F_y ont donc toujours le même 𝔐^adm_x, et ∼_N s'y réduit à l'égalité pure de R_x sur ce domaine commun. C'est une simplification appréciable pour le premier calcul, mais elle ne vaudra pas pour tout exemple futur d'IWS.

**Lien avec C23 et avec C5.** |F_y/∼_N| ≥ 2 est une condition nécessaire mais non suffisante à un témoin de H_ρ en y : il dit qu'une diversité comportementale existe derrière la lecture y, pas qu'une paire d'histoires partant d'un même x₀ atteint effectivement deux classes différentes. C'est exactement le rôle qu'a joué la construction par boucles symétriques : produire deux préhistoires qui atteignent deux classes distinctes de F_y. Pour C5, la question « comment ces classes varient-elles quand y varie » est probablement la bonne formalisation de la question laissée ouverte (« la structure change-t-elle la façon dont le système garde la trace de ce qui lui arrive ? ») sans contamination par les différences visibles entre structures : on compare la partition F_{(s,y_int)}/∼_N à la partition F_{(s′,y_int)}/∼_N pour un même y_int, à s et s′ fixés.

**Prédiction pour le noyau (à vérifier avant Hardt/Whitney).** Sur la fibre à (A,H,V,P) fixés, la coordonnée cachée est τ. Deux τ voisins ont, génériquement, le même classement de similarité à tous les Kairos futurs tant qu'aucune inégalité de classement ne devient une égalité : la partition de l'espace des τ par ∼_N devrait donc être *localement constante sur un ouvert dense*, avec pour bord un ensemble de mesure nulle correspondant aux égalités de similarité (les cas de type « juxtaposition interne », § crash-test). Un nombre fini de classes n'est donc probablement pas la bonne attente globale (le nombre de recâblages accessibles à long terme peut être dénombrable), mais la structure locale (ouvert dense localement constant + frontière fine) est déjà testable numériquement sur le témoin N=6 : discrétiser un segment de τ autour du témoin, calculer le graphe recâblé obtenu après un nombre fixé de Kairos, et repérer les sauts de classe. C'est un crash-test à moindre coût avant tout énoncé de tameness.

**Prochaine étape suggérée.** Écrire la définition de ∼_N dans le corps du texte (à côté de Rep^max, pas dans un crash-test), avec la remarque sur le domaine, puis lancer le calcul numérique ci-dessus sur le témoin N=6 pour avoir un premier fait avant de choisir entre équivalence stricte et préordre de simulation.

**Premier calcul [NUM].** Fibre à (A,H,V,P) = (A₀,0,0,0) fixée, coordonnée cachée τ. Point de base τ₀ construit avec une tie exacte sim(i*,1) = sim(i*,2) (nœuds 1 et 2, 4 et 5 pris identiques dans τ₀). Protocole de continuation identique (poussée U=2,5 sur le nœud 0), mot enregistré sur k = 2 Kairos.

- *Direction transversale* (brise la symétrie 1↔2 : τ₁ += q e_y, τ₂ −= q e_y). Mur net et unique en q = 0 : mot = (retire {3,2}, ...) pour q < 0, mot = (retire {3,1}, ...) pour q ≥ 0, stable dès |q| ≥ 0,001 des deux côtés. Le point q = 0 lui-même est assigné par le départage à l'indice (résultat déterministe, cohérent avec le mot du côté q ≥ 0). C'est exactement le tableau conjecturé : cellule ouverte | mur | cellule ouverte.
- *Direction symétrique* (préserve l'automorphisme 1↔2, 4↔5 : τ₁, τ₂ et τ₄, τ₅ déplacés ensemble). Le mot reste identique — retire {3,1} — sur tout le segment testé, q ∈ [−0,10 ; 0,10]. La tie sim(i*,1) = sim(i*,2) est exacte sur tout le segment, pas seulement en q = 0 : ce n'est pas un mur ponctuel manqué par un maillage trop grossier, c'est une droite entière logée dans le lieu de tie, parce que l'automorphisme du graphe (1↔2, 4↔5, 0 et 3 fixes) laisse toute la dynamique — donc τ(t) tout entier — invariante quand la condition initiale l'est.

Confirmation nette de la mise en garde : la généricité de l'égalité de classement dépend de la direction testée. Elle est vraie transversalement à un sous-espace de symétrie, fausse (tie partout, pas de mur) le long de ce sous-espace. Le lieu de tie complet contient donc au moins deux types de morceaux : une nappe générique de codimension 1 (murs transverses), et un sous-espace invariant de codimension supérieure entièrement dégénéré. Avant tout énoncé de type Hardt/Whitney, il faudra donc traiter séparément le lieu de tie « accidentel » et le lieu de tie « forcé par une symétrie du problème » — un feuilletage stratifié par le groupe d'automorphismes du graphe est probablement le bon langage, pas une simple généricité transverse.

### 4.1 — Reformulation par strates de symétrie (Benoit)

Programme révisé, adopté :
\[
\text{espace des }\tau
\ \longrightarrow\
\text{strates }\mathcal T_H=\{\tau:\operatorname{Stab}_\Gamma(\tau)=H\}
\ \longrightarrow\
\text{murs transverses (ties non forcées)}
\ \longrightarrow\
\sim_k
\ \longrightarrow\
\sim_N,
\]
avec Γ = Aut(A) *au graphe courant*, et non un groupe fixé une fois pour toutes : après un recâblage A_k → A_{k+1}, le groupe Aut(A_k) → Aut(A_{k+1}) peut changer (rétrécir ou grossir). La bonne donnée est donc une suite de types de symétrie le long du mot structurel, pas un seul groupe ambiant. Le raffinement à profondeur k se décompose en
\[
\mathcal P_k=\mathcal P_k^{\mathrm{sym}}\vee\mathcal P_k^{\mathrm{trans}},
\]
la partie symétrique venant des lieux fixes traversés, la partie transverse des murs de classement rencontrés. Point de méthode adopté : on ne quotiente pas F_y par Aut(A) directement (deux états reliés par automorphisme ne sont pas nécessairement ∼_N-équivalents, précisément à cause du départage) — le groupe sert à *stratifier et expliquer*, pas à identifier.

### 4.2 — Crash-test : le départage par indice, convention ou nécessité ? [NUM]

Question de Benoit : le départage par indice appartient-il à la définition mathématique de K*, ou n'est-il qu'une convention numérique évitable ?

**Vérification.** Avec σ = (1 2)(4 5) ∈ Aut(A₀), sur le témoin N=6, protocole identique à celui de la §4 :

- *Hors du lieu fixe* (q = ±0,05 ; +0,02, direction transversale) : σ(A₁(τ)) = A₁(σ·τ), σ(i*(τ)) = i*(σ·τ), et l'ensemble retiré/ajouté se transporte exactement par σ. Confirmé sur les trois valeurs testées, sans exception. Le noyau lui-même — flot F, garde D, règle de classement — est donc bien Γ-équivariant partout où le classement n'est pas à égalité.
- *Sur le lieu fixe* (τ₀ exactement σ-invariant, q = 0) : A₁(τ₀) n'est **pas** σ-invariant (arête (0,2) conservée, son image (0,1) supprimée). Un point de départ parfaitement symétrique produit une sortie asymétrique. Aut(A₁) ne contient donc plus σ, alors que Aut(A₀) le contenait : exemple concret et vérifié de Aut(A_k) ⊋ Aut(A_{k+1}) le long du mot.

**Verdict : nécessité, pas convention.** Avec m = 2 à choisir parmi 3 voisins dont les deux moins similaires sont exactement à égalité et échangés par σ, aucune règle de départage Γ-équivariante et à valeur unique n'existe : une règle équivariante doit envoyer la paire liée {1,2} sur elle-même comme *ensemble*, donc retirer les deux ou aucun des deux — jamais un seul — ce qui viole m = 2 exactement dans un cas comme dans l'autre (retirer les deux force à en garder un troisième non prévu, n'en retirer aucun contredit le compte). Le départage par indice n'est donc pas un artefact d'implémentation : **déterminisme (H1–H4) et Γ-équivariance sont structurellement incompatibles sur le lieu de tie**, dès que la règle de sélection est à cardinal fixé. C'est un fait, pas un choix — la seule alternative réelle serait d'abandonner le cardinal fixé m ou le déterminisme sur ce lieu (K* multivalué, ou un régime spécial sur les ties), ce qui serait un changement de socle, pas un ajustement cosmétique.

Ceci confirme et referme le crash-test proposé : la symétrie du noyau (F, D, classement) et la symétrie de la sémantique complète de K* sont bien deux choses différentes, et l'écart entre les deux est localisé exactement sur les lieux fixes non triviaux — nulle part ailleurs.

**Écarté : remplacer m par un m_max variable.** L'idée serait d'inclure toute une orbite liée plutôt qu'une partie (retirer les deux nœuds à égalité, ou aucun, jamais un seul), en plafonnant à un m_max. Cela répare bien le cas pair de notre témoin (l'orbite {1,2} est incluse ou exclue en bloc), mais ne répare pas l'obstruction en général : une équivariance véritable exige d'inclure ou d'exclure chaque orbite de Γ_τ-tie *entièrement*, quelle que soit sa taille. Dès qu'une orbite de taille 3 se présente pile à la coupure pour un budget de 2, on retrouve exactement le même mur (retirer les 3 ou aucun, jamais 2), sauf que c'est maintenant le *cardinal* du recâblage qui devient discontinu au lieu de son *contenu* — le problème est déplacé, pas résolu. Et m_max cesserait d'être un paramètre du modèle : sa valeur effective dépendrait de la taille des orbites de Stab_Γ(τ) rencontrées, donc de τ lui-même, ce qui revient à faire dépendre K* de tout le groupe local à chaque saut pour un gain nul dans le cas général. Le diagnostic de 4.2 (incompatibilité structurelle déterminisme/équivariance sur le lieu de tie, à cardinal fixé *ou* borné) reste donc entier ; il n'y a pas de rustine côté arité de la sélection.

### 4.3 — Lemme combinatoire, généralisation au socle, et suivi numérique de (Aut(A_k), G_k)

**Statut V5.5 : incorporé.** Le lemme, la proposition d'invariance des lieux fixes sous le flot, et les deux témoins numériques (N=6 profondeur/réinjection, N=9 deux régimes) sont désormais dans le .tex lui-même — respectivement les propositions « Obstruction orbitale à une sélection équivariante » et « Invariance d'un lieu fixe pendant le flot du noyau », et les remarques qui les suivent dans le crash-test « Noyau IWS et cas pur K* ». Vérifié ligne à ligne contre les scripts : toutes les valeurs numériques citées (0,557832 ; 0,997785 ; 0,447214 ; |Aut(A₀)|=72 ; |Aut(A₁)|=240 ; la fusion d'orbite {1,2}∪{6,7,8}) correspondent exactement aux sorties de `orbit_diversity.py`, et la description du témoin N=6 (période 2, oscillation 2,1,2,1,…, réinjection) correspond à `orbit_track_depth.py` / `check_period.py` / `reinjection.py`. Ce qui suit reste la version de travail (dérivation complète, options écartées) ; le .tex en donne la forme publiable.

**Lemme (sélection équivariante à cardinal fixé).** Soit X un ensemble fini muni d'une action d'un groupe fini G, et v : X → ℝ une fonction G-invariante. Notons, pour m ≤ |X| : c le m-ième plus petit valeur distincte de v, T = {x ∈ X : v(x) = c} le niveau au seuil, a = |{x : v(x) < c}|. Comme v est G-invariante, T est G-invariant, donc réunion de G-orbites. Il existe un sous-ensemble S ⊆ X, G-invariant, réalisant exactement « les m plus petites valeurs de v » (c'est-à-dire {v<c} ⊆ S ⊆ {v≤c} et |S| = m) **si et seulement si** (m − a) s'écrit comme somme des tailles d'une sous-famille des G-orbites de T.

*Preuve.* (⇐) Prendre l'union de {v<c} et de la sous-famille choisie. (⇒) Tout sous-ensemble G-invariant est une union d'orbites ; S ∩ T en est une, de cardinal m − a. ∎

Corollaire immédiat : si T est une seule orbite de taille t > 1, une sélection équivariante existe seulement si m − a ∈ {0, t} — jamais une valeur intermédiaire. C'est exactement notre cas (a = 1, T = {1,2}, t = 2, m − a = 1 ∉ {0,2}).

**Généralisation au socle, pas seulement au recâblage.** Le même obstacle est déjà présent ailleurs dans H1–H4, sous une forme légèrement différente : le départage « plus petit indice » entre Kairos simultanés (Tome I, événements simultanés) demande de choisir un représentant canonique dans un ensemble de nœuds à égalité — c'est-à-dire une orbite de taille t > 1 réduite à un singleton, le cas m = 1 du même lemme avec a = 0. Les deux règles de départage du socle (ordre de traitement des sauts simultanés, et classement de similarité à l'intérieur d'un saut) sont donc deux instances de la même impossibilité, pas deux conventions distinctes. Le socle ne pouvait pas être totalement Γ-équivariant nulle part où une multiplicité de nœuds coïncide : ce n'était pas un défaut de rédaction du Tome I.

**Suivi numérique de (Aut(A_k), G_k = Stab_{Aut(A_k)}(τ_k)) sur le témoin N=6.** Calcul par force brute (720 permutations, N=6) sur 3 Kairos successifs, branche exactement symétrique (τ₀) et branche générique (q=0,05) :

| k | branche | Aut(A_k) | G_k | orbite au seuil compatible avec m ? | Aut(A_{k+1}) | G_k ⊆ Aut(A_{k+1}) |
|---|---|---|---|---|---|---|
| 0 | symétrique | 2 | 2 | non (t=2, m−a=1) | 1 | **non** |
| 0 | générique | 2 | 1 | — (déjà hors du lieu fixe) | 1 | oui |
| 1 | les deux | 1 | 1 | — (G déjà trivial) | 2 | oui (trivial) |
| 2 | les deux | 2 | 1 | — (G déjà trivial) | 1 | oui (trivial) |

Résultat qui affine le tableau proposé : **Aut(A_k) n'est pas monotone** — il retombe à 1 puis remonte à 2 en k=1→2, y compris sur la branche générique. Mais cette remontée est une symétrie du graphe *seul*, sans rapport avec l'état caché courant : à chaque fois que Aut(A_k) regagne un élément non trivial, G_k reste égal à 1, c'est-à-dire que τ_k ne se trouve pas (plus) dans le lieu fixe correspondant. La bonne variable à suivre est donc bien G_k et non Aut(A_k) seul, comme le proposait Benoit — et il faut ajouter au dictionnaire un troisième statut, à côté de « transverse » et « obstruction orbitale » : une composante de symétrie peut être **réapparue mais inerte** (Aut(A_k) non trivial, G_k trivial), ni un mur ni une obstruction, simplement une coïncidence combinatoire du graphe qui ne rencontre plus l'état.

Sur cette trace précise, une seule obstruction orbitale réelle a été rencontrée (k=0, branche symétrique) ; les pas suivants n'en présentaient plus l'occasion puisque G était déjà retombé à 1. Voir une seconde obstruction indépendante demanderait soit un témoin plus riche (N plus grand, groupe Aut(A) non résolu en un coup), soit de réinjecter délibérément une composante symétrique dans τ après le premier Kairos — ce qui serait un choix de construction, pas une observation spontanée de cette trajectoire.

**Extension en profondeur (script `orbit_track_depth.py`, k = 0..14, forçage constant inchangé).** Confirmation numérique de la remarque ci-dessus, et de sa raison mécanique précise. La séquence des graphes A_k devient exactement périodique de période 2 dès k = 0 (A₀ = A₂ = A₄ = … et A₁ = A₃ = A₅ = …, vérifié par égalité matricielle exacte), avec Aut(A_k) qui oscille 2,1,2,1,… indéfiniment sur les deux branches. Mais τ_k ne suit pas cette périodicité : sous le forçage constant utilisé (poussée fixe sur le nœud i*), τ dérive de façon monotone et asymétrique une fois la dégénérescence initiale brisée (à k = 0, τ₁ = τ₂ exactement ; dès k = 1, l'écart est déjà de l'ordre de 0,1 et ne se referme plus). Résultat sur les 15 premiers Kairos, deux branches : **G_k > 1 seulement à k = 0** (branche symétrique), jamais ensuite ; toutes les remontées de Aut(A_k) à 2 (k = 2,4,6,…) sont du statut « réapparue mais inerte », confirmé systématiquement et non plus seulement sur 2 occurrences. Interprétation : sous forçage déterministe fixe, la rupture de symétrie à la première obstruction est **définitive** — il n'existe pas de mécanisme spontané de retour à la coïncidence exacte qui a produit k = 0, quelle que soit la profondeur explorée, précisément parce que la dynamique post-obstruction n'a plus aucune raison structurelle de repasser par un point fixe de σ. Ceci ferme la piste « profondeur seule » et confirme que la piste de réinjection délibérée d'une composante symétrique (seconde option envisagée ci-dessus) est la voie nécessaire, et non simplement l'une des deux, pour obtenir une seconde obstruction indépendante.

**Réinjection délibérée (script `reinjection.py`) — seconde obstruction obtenue par construction.** À l'issue du jump 1 (état post1, graphe A₂ = A₀ par périodicité), on prend σ = (0)(1 2)(3)(4 5), l'unique automorphisme non trivial de A₂, et on symétrise l'état complet (H, V, τ, P) par moyenne avec son image par σ — pas seulement τ, pour que l'équivariance du flot continu garantisse que la symétrie se conserve exactement pendant le vol libre. Vérifié : l'écart |τ − σ·τ| passe de 0,142 à 0,0 exactement après symétrisation, et reste à 0,0 (à la précision machine) jusqu'au Kairos suivant — confirmation numérique directe, sur l'état complet et pas seulement sur K*, que le flot continu du noyau est lui-même Γ-équivariant tant que le graphe l'est (ce que `equivariance_check.py` n'avait testé que pour le recâblage). Au jump 2 ainsi engendré : Aut(A₂) = 2, G(τ) = 2 — une seconde obstruction orbitale réelle, obtenue à volonté. Mais elle reproduit **exactement** la même instance combinatoire que celle de k = 0 (i* = 0, m = 2, retirés {1,3}, ajoutés {4,5}, similarités quasi identiques à 0,998 pour la paire liée), et l'équivariance se brise de la même façon après le saut (σ ∉ Aut(A₃)). C'est attendu et non un artefact : A₂ = A₀ *exactement*, donc le graphe n'offre qu'une seule symétrie possible (le même σ) — réinjecter la reproduit à l'identique plutôt que de révéler un obstacle d'un type combinatoire différent (autre m, autre taille d'orbite t, autre a). Pour observer un second obstacle *qualitativement* distinct du premier (et non une simple répétition), il faudrait soit un témoin dont le graphe change de classe d'automorphie au fil des recâblages (N plus grand, structure moins rigide que le témoin actuel dont la seule symétrie est cette involution), soit réinjecter délibérément une configuration symétrique différente (portant sur un autre sous-ensemble de nœuds) plutôt que de repartir de la trajectoire naturelle. Conclusion actuelle : la réinjection est un outil qui fonctionne — elle prouve que l'obstruction n'est pas un accident isolé du démarrage mais une conséquence structurelle reproductible de la symétrie du graphe — mais elle ne suffit pas à elle seule à cartographier plusieurs *classes* d'obstruction sur ce témoin ; il faudrait l'étendre à un graphe moins rigide pour ça, si ce chantier devient prioritaire.

**Un second témoin (N=9, script `orbit_diversity.py`) — orbite de taille 3 et deux types d'orbites simultanés.** Le témoin N=6 ne pouvait produire qu'une seule classe d'obstacle (t=2, a=1) parce que sa seule symétrie est une involution portant sur une paire. Pour tester le lemme sur une orbite plus grande et sur plusieurs types d'orbites à la fois, un second graphe a été construit : nb(0)={1,2,3} jumeaux stricts (orbite de taille 3), nn(0)={4,5}∪{6,7,8} avec deux orbites disjointes (tailles 2 et 3). |Aut(A₀)|=72=S₃(sur 1,2,3)×Z₂(sur 4,5)×S₃(sur 6,7,8), vérifié par force brute (720 candidats via partition par degré, comme pour le témoin N=6).

Départ d'un état bloc-symétrique (τ égal à l'intérieur de chaque orbite) et poussée constante sur le nœud 0, comme pour le témoin précédent — sans réinjection cette fois, la symétrie est spontanément au rendez-vous du premier Kairos puisqu'elle est déjà dans l'état initial et que le flot est équivariant. Résultat, un seul événement, deux instances distinctes du lemme simultanément :

- **côté retrait (nb)** : les trois candidats 1, 2, 3 sont exactement à égalité (similarité 0,557832 chacun) — T de taille 3, a=0, m=2. m−a=2 ∉ {0,3} : **selon le lemme, aucune sélection Γ-équivariante de cardinal 2 n'existe.** Le tie-break déterministe retire {1,2} et garde 3 — un choix arbitraire parmi 3 équivalents, conforme à la prédiction.
- **côté ajout (nn)** : les candidats 4,5 sont à égalité au sommet (0,997785), strictement devant 6,7,8 (0,447214). T de taille 2, a=0, m=2. m−a=2 = t : **le lemme autorise ici une sélection équivariante**, et c'est exactement ce qui se produit — {4,5} est ajouté en bloc, sans aucun arbitraire (le tie-break ne fait que les ordonner entre eux, les deux sont pris).

Les deux régimes du lemme (existence vs vacuité de la sélection équivariante) sont donc observés dans le **même** événement, sur les deux moitiés de la même règle de recâblage — confirmation directe que le critère m−a ∈ {0,t} est bien ce qui décide, pas une propriété générale de K*.

**Recâblage et restructuration réelle du groupe.** Après ce Kairos, |Aut(A_suivant)| passe de 72 à **240**, et les orbites changent de nature, pas seulement de taille : {1,2,3} (orbite-3 avant, nb(0)) éclate — 3 reste seul (toujours connecté à 0), tandis que 1 et 2, désormais totalement isolés (leur unique arête a été coupée), **fusionnent avec l'orbite {6,7,8}** en une orbite unique de taille 5, parce que des sommets isolés sont indiscernables du point de vue du graphe quelle que soit leur origine. {4,5} reste une orbite de taille 2, mais son rôle change (ils sont maintenant aussi connectés à 0). Le groupe ne passe donc pas simplement d'un ordre à un autre : sa décomposition change de forme, S₃×Z₂×S₃ (ordre 72) devient Z₂×S₅ (ordre 240, sur {4,5} et {1,2,6,7,8}) — un recâblage qui redistribue concrètement qui-est-symétrique-avec-qui, au-delà d'un simple gain ou perte d'ordre. C'est le phénomène demandé par le troisième point : la fusion 1,2 avec 6,7,8 est un fait purement structurel du graphe courant, sans rapport avec l'historique de chaque nœud — cohérent avec l'esprit de C4 (rien dans la structure ne « se souvient » que 1 et 2 étaient récemment des voisins privilégiés de 0).

**Sur la non-téléologie.** Le rapprochement est juste, et je le formulerais ainsi : K* ne brise la symétrie par aucune préférence pour l'asymétrie — le lemme ci-dessus montre que l'ensemble des règles déterministes et Γ-équivariantes à cardinal m est simplement *vide* dès que m − a n'est pas une somme d'orbites. Il n'y a donc rien à choisir *entre* une issue symétrique et une issue asymétrique : l'issue symétrique n'existe pas dans l'espace des règles admissibles. Le départage n'optimise rien, il comble un ensemble vide par une convention — c'est bien la posture C4 (pas de telos primitif), même appliquée à la mécanique de sélection elle-même et pas seulement à la dynamique globale.

### 4.4 — Programme F_y/∼_N en trois temps (Benoit) : étape 1, un seul Kairos

**Le programme proposé.** Plutôt que d'attaquer directement C5 ou la tameness, cartographier d'abord concrètement la partition comportementale d'une fibre d'opacité : (1) un seul Kairos — fixer y=(A,H,V,P), faire varier τ, caractériser la partition de F_y par le prochain comportement observable ; (2) profondeur finie k — raffinement 𝒫₁⪰𝒫₂⪰⋯⪰𝒫_k, en réutilisant le matériel sur les groupes qui changent et les orbites qui fusionnent (§4.3) ; (3) seulement ensuite, k→∞ et la question de tameness. C5 est mis en sommeil : l'étude de F_y/∼_N doit dire ce que C5 devrait être, pas l'inverse.

**Fait analytique (avant tout calcul).** Dans le noyau, pour y=(A,H,V,P) fixé (donc i* déterminé comme le nœud au seuil), le résultat du Kairos suivant — les arêtes retirées et ajoutées, donc A_suivant — ne dépend de τ qu'à travers l'ordre des valeurs {cos(τ_{i*},τ_j)}_{j∈nb(i*)} (retrait) et {j∈nn(i*)} (ajout) : ni H, ni V, ni P n'interviennent dans ce choix (ils ne déterminent que le déclenchement, déjà fixé puisque y l'est, et le rescaling de P_{i*},V_{i*} après coup). Comme nb(i*) et nn(i*) sont finis, il n'existe qu'un nombre fini d'ordres totaux possibles sur chacun : **𝒫₁ est donc automatiquement une partition en un nombre fini de classes**, chacune une chambre ouverte séparée par les hypersurfaces de coïncidence {cos(τ_{i*},τ_j)=cos(τ_{i*},τ_k)}. Ce n'est pas une propriété qui demande une preuve au cas par cas : elle vient de ce que la règle de sélection est un simple classement sur un ensemble fini de candidats. La vraie question numérique n'est donc pas « fini ou pas » (toujours fini) mais **la forme géométrique de ces chambres et la nature de leurs parois**.

**Calcul (script `partition_Fy.py`), témoin N=6.** i*=0, nb(0)={1,2,3}, nn(0)={4,5}. Comme |nn(0)|=2=m, le côté « ajout » est trivial (toujours {4,5}) ; toute la combinatoire de 𝒫₁ est dans le côté retrait, c'est-à-dire dans quel nœud de {1,2,3} est *gardé* (= argmax du cosinus). En fixant τ₀ (jauge de rotation) et φ₃ (angle de τ₃ relatif à τ₀) à une valeur générique, et en balayant φ₁,φ₂∈[0°,360°) : trois régions, d'aires 43,4 % / 43,2 % / 13,4 %, respectivement 2, 2 et 1 composantes connexes sur le tore — un nombre fini confirmé numériquement, comme attendu.

La figure fait apparaître deux murs de nature différente, exactement la distinction que le témoin N=9 avait mise en évidence :
- un **mur structurel** φ₁=φ₂ (diagonale), qui correspond à τ₁=τ₂ comme *vecteurs* — le lieu fixe exact de l'automorphisme σ=(1 2)(4 5) ∈ Aut(A). Tout point de ce mur est une vraie coïncidence de symétrie.
- un **mur transverse** φ₁=−φ₂ (anti-diagonale), qui donne cos φ₁=cos φ₂ (donc une égalité de *score*) sans que τ₁=τ₂ comme vecteurs — une coïncidence de valeur sans rapport avec Aut(A). Rien ne le distingue localement du mur structurel dans le classement (les deux sont des ties de score 1↔2), mais un seul des deux est une orbite de Γ.

Les deux murs se croisent exactement aux points où φ₁=φ₂=0° ou 180° (mod 360°) — c'est-à-dire là où le mur transverse rencontre le lieu fixe : cohérent avec l'observation du §4.3 (un tie de valeur peut coïncider ponctuellement avec un tie structurel sans que les deux notions se confondent en général).

**Bilan étape 1.** La partition existe, est finie, et se décompose en chambres à parois algébriques simples (cosinus égaux) — mais la carte montre déjà, sur le cas le plus simple possible, qu'« un mur = une égalité de score » ne suffit pas à en lire la nature : il faut, en plus de l'équation du mur, savoir s'il porte ou non une orbite de Aut(A). Prochaine étape naturelle (point 2 du programme) : itérer sur 𝒫₂ pour voir comment chaque chambre de 𝒫₁ se subdivise à un second Kairos, et si les murs qui apparaissent à l'étape 2 respectent encore Aut(A_suivant) ou vivent dans la structure de groupe fusionnée (comme au N=9).

### 4.5 — Nature des parois : Fix(σ) ⊊ {c_i=c_j}, et étape 2 (script `partition_Fy_depth2.py` / `partition_Fy_depth2b.py`)

**Raffinement de la lecture de la figure d'étape 1 (Benoit).** La paroi φ₁=φ₂ (τ₁=τ₂ comme vecteurs) est le lieu fixe réel de σ=(1 2)(4 5) ∈ Aut(A) : la coïncidence des scores y est *forcée* par une symétrie de l'état. La paroi φ₁=−φ₂ donne c₁=c₂ mais τ₁≠τ₂ en général : une collision de l'application score sans rapport avec Aut(A). D'où
\[
\operatorname{Fix}(\sigma) \subsetneq \{\tau : c_i(\tau)=c_j(\tau)\},
\]
et le fait, plus général que l'étape 1 à elle seule : **K\* ne peut pas reconnaître, à partir de la seule égalité de scores, la nature géométrique de sa propre frontière** — il faut remonter à τ dans son ensemble pour savoir si l'on est sur une strate de symétrie ou sur une coïncidence transverse. C'est ce qui justifie rétrospectivement de ne jamais réduire prématurément le système à ses seuls rankings (cf. §4.1). Sur le plan de la tameness, les parois d'étape 1 sont des égalités de produits scalaires et de normes — rien de monstrueux à ce niveau — mais la vraie question reste le comportement sous tirage en arrière à travers plusieurs épisodes.

**Étape 2, premier essai (fenêtre φ₁,φ₂).** À l'intérieur de la chambre « gardé=1 » (retirés {2,3}, ajoutés {4,5} au Kairos 1), on intègre réellement la dynamique sous A₁ jusqu'au Kairos 2, pour une fenêtre (φ₁,φ₂) proche du centre de la chambre (φ₃, τ₄, τ₅ fixés). Résultat : sur les 2025 points testés, le nœud 1 reste dominant *partout* — aucune paroi de niveau 2 dans cette fenêtre. La chambre ne se raffine pas le long de cette coupe : le nœud qui gagnait déjà nettement au Kairos 1 continue de gagner au Kairos 2, la dynamique entre les deux n'ayant pas eu le temps de renverser un écart déjà large.

**Étape 2, second essai (fenêtre φ₄,φ₅) — la vraie paroi.** Dans A₁, nb(0)={1,4,5} : les candidats qui n'étaient *pas* en compétition à l'étape 1 (4 et 5, alors non-voisins, ajoutés automatiquement) sont ceux qui portent la nouvelle paroi. En fixant φ₁=10°, φ₂=40° (loin de tout mur d'étape 1) et en balayant φ₄,φ₅∈[0°,360°) : gardé=1 sur 88,4 % de la grille, gardé=4 sur 5,9 %, gardé=5 sur 5,8 % — deux bandes étroites près de φ₄≈0° et φ₅≈0° respectivement, quasi indépendantes l'une de l'autre. Géométriquement, ces bandes restent simples (des franges de niveau, pas de courbe visiblement tourmentée) : rien d'alarmant pour la tameness sur cet exemple précis, mais un seul exemple ne dit rien du cas général.

**Le point important : Aut(A₁) est trivial.** Vérifié par force brute : |Aut(A₀)|=2 (engendré par σ), |Aut(A₁)|=1. Le recâblage du Kairos 1 a détruit toute symétrie du graphe (attendu : node1 reste privilégié auprès de 0, node2 ne l'est plus, la paire (1,2) qui portait σ n'existe plus comme paire). Conséquence directe du critère de 4.5 ci-dessus : **aucune des deux nouvelles parois (gardé=4, gardé=5) ne peut être une strate de symétrie, faute de groupe non trivial pour la porter** — elles sont *nécessairement* du type coïncidence transverse, sans qu'il soit besoin de le vérifier point par point. C'est un cas limite instructif de la distinction Fix(σ)/{c_i=c_j} : quand Γ_k=1, cette distinction s'effondre d'un seul côté, tout tie restant est automatiquement transverse.

**Bilan et prochaine coupe.** Deux leçons pour la suite du programme en trois temps : (i) une paroi de profondeur 2 peut être une paroi *authentiquement nouvelle* — elle ne provient pas d'une préimage déformée d'une paroi de profondeur 1 (les candidats 4,5 n'étaient pas en compétition avant), donc « suivre l'origine de chaque paroi » demande de distinguer explicitement « préimage d'une paroi existante » de « paroi née de candidats nouvellement mis en concurrence par le recâblage » ; (ii) tant que Γ_k reste trivial, la question Fix(σ)/transverse ne se pose plus — elle ne redevient pertinente que si une future chambre restaure une symétrie non triviale de A_k, ce qui n'est pas le cas ici mais l'était dans le suivi (Aut(A_k),G_k) du témoin N=9 (§4.3). Un prochain essai utile serait donc de chercher, parmi les chambres de 𝒫₁, une chambre dont le graphe A₁ conserve un automorphisme non trivial, pour voir si sa paroi de profondeur 2 se scinde alors en Fix(σ')/transverse comme à l'étape 1, ou reste elle aussi purement transverse.

### 4.6 — Généalogie des parois (Benoit) et un artefact de protocole découvert en le cherchant

**Correction de généalogie (Benoit).** « Préimage d'une paroi de profondeur 1 » était trop restrictif : à l'intérieur d'une chambre C de 𝒫₁, le graphe A₁ est fixé et définit son propre problème de ranking, de murs élémentaires W(A₁)=⋃{c_i^{A₁}=c_j^{A₁}}. Les nouvelles parois de 𝒫₂ dans C sont Φ_C⁻¹(W(A₁)) — des préimages, mais du *nouveau* problème combinatoire ouvert par K\*, pas de l'ancien. Généalogie à deux axes orthogonaux : (mur déjà pertinent avant K\* / mur activé par un nouvel ensemble de candidats) × (porté par une symétrie / transverse). Notre exemple {4,5} dans la chambre « gardé=1 » est bien : mur nouvellement activé + transverse.

**Test dans la chambre « gardé=3 » (script `partition_Fy_depth2_kept3.py`).** Prédiction de Benoit confirmée : après retrait de {1,2} et ajout de {4,5}, A₁ conserve σ=(1 2)(4 5) — et en réalité |Aut(A₁)|=4, pas seulement 2 : 0 et 3 sont devenus de vrais jumeaux (mêmes voisins {4,5} l'un de l'autre), ajoutant τ=(0 3) comme second générateur indépendant. En fixant τ₁=τ₂ (précondition de Fix(σ) sur cette coupe) et en balayant (φ₄,φ₅) : gardé=3 domine (90,25 %), gardé=4 (4,81 %) et gardé=5 (4,94 %) se partagent deux bandes étroites.

**Ce qui s'est passé en vérifiant les ties exacts.** Sur les 3600 points, 118 ont c₄=c₅ à 1e-10 près, pas seulement les 60 attendus sur la diagonale φ₄=φ₂. Plutôt que d'ignorer les 58 autres, je les ai regardés : ils sont *exactement* sur l'antidiagonale φ₄=−φ₅, et la coïncidence est exacte au bit près (`|c4−c5| = 0.000e+00`, vérifié en précision machine), pas un artefact de tolérance.

Cause identifiée et vérifiée : dans le régime γ₁=λ=0, avec un forçage qui ne pousse que la composante x d'un seul nœud, **H et V restent confinés exactement à y≡0 pour tout t** (vérifié : max|H_y|=max|V_y|=0,0 au bit près sur toute la trajectoire — le sous-système y part de 0 sans jamais recevoir de forçage puisque Ã ne mélange jamais x et y et que tanh(0)=0). Conséquence directe : chaque τ_{j,y}(t) obéit à une simple décroissance exponentielle *découplée de tout le reste*, ce qui rend chaque score c_j(τ) automatiquement **pair en φ_j** — c_j(φ_j)=c_j(−φ_j) — indépendamment de toute symétrie du graphe. Combiné au fait que 4 et 5 partagent la même fonction c(·) (à cause de σ, comme prévu), on obtient gratuitement c₄(φ₄)=c₅(φ₄) *et* c₅(−φ₄)=c₅(φ₄), donc c₄(φ₄)=c₅(−φ₄) : l'antidiagonale entière est un tie exact, sans lien avec Aut(A₁).

**Portée de la correction.** Ce n'est pas une paroi « transverse générique » au sens où on l'entendait : elle est *elle aussi* forcée, mais par une symétrie du **protocole de forçage** (réflexion y, propre au choix d'une poussée constante mono-directionnelle sur un seul nœud) et non par Aut(A). À l'étape 1, ça ne changeait rien : τ y était une variable libre sans dynamique, et cos(φ)=cos(−φ) y est une trivialité de la formule, correctement identifiée comme telle. Mais dès qu'une vraie évolution intervient (étape 2 et au-delà), cette parité cachée est présente dans **toutes** nos expériences numériques de la session, puisque toutes utilisent ce même type de forçage (poussée constante mono-axe sur i*). Elle ne remet en cause aucun résultat analytique (le lemme, la proposition d'invariance, l'identifiabilité — aucun ne dépend du choix du forçage), mais elle veut dire qu'on **sous-échantillonne systématiquement** la vraie diversité des parois transverses : tant qu'on force uniquement selon un axe fixe sur un seul nœud, une partie de ce qu'on prend pour « coïncidence générique » est en fait forcée par cette parité résiduelle. Pour voir une paroi authentiquement non forcée (ni Fix(σ), ni cette parité), il faudra un forçage moins dégénéré — au moins deux directions non colinéaires, ou plusieurs nœuds poussés simultanément de façon non symétrique.

### 4.7 — Contrôle expérimental (Benoit) : casser la symétrie du protocole sans casser celle du système

**Le tri proposé.** Trois origines possibles d'un tie, dont une seule est un artefact à éliminer plutôt qu'une catégorie du modèle : (1) symétrie structurelle/dynamique (Fix(σ)) ; (2) symétrie accidentelle du protocole de sonde (le forçage mono-axe, ici) ; (3) coïncidence générique de scores. La 2 n'entre pas dans la classe IWS, elle affecte seulement la manière dont on interroge numériquement le système.

**Test (script `partition_Fy_depth2_kept3_2Dforce.py`).** Même chambre « gardé=3 », même scan (φ₄,φ₅), mais u₀=(Ux,Uy) avec un angle générique (37°) au lieu de (U,0) — σ fixant le nœud 0, cette poussée reste σ-invariante quelle que soit sa direction, donc Fix(σ) n'a aucune raison d'être affecté. Vérifié : max|H_y|, max|V_y| ≈ 1,10 / 1,34 en fin de trajectoire (le confinement à y≡0 a bien disparu, contre 0,0 exact auparavant). Résultat sur les ties exacts (tolérance 1e-9) : **60/60 sur la diagonale** (Fix(σ) intact), **2/3600 seulement près de l'antidiagonale** (les deux points d'intersection triviale diagonale∩antidiagonale en (0,0) et (180,180), pas une ligne), **0 ailleurs**. L'antidiagonale a bien disparu comme prévu, la diagonale a bien survécu telle quelle, et aucune nouvelle coïncidence générique n'apparaît à cette résolution.

**Bilan.** Séparation numérique propre entre les deux mécanismes, exactement comme anticipé : casser la symétrie du protocole (forçage 2D générique sur un nœud fixé par σ) sans casser celle du système (σ reste un automorphisme, sa poussée reste σ-invariante puisque portée par un nœud fixe de σ) isole Fix(σ) comme seule source de tie exact dans cette chambre. Leçon méthodologique retenue pour la suite du chantier F_y/∼_N : avant de qualifier une paroi numérique de « transverse », vérifier que le protocole de sonde (forçage, conditions initiales) n'introduit pas lui-même une symétrie supplémentaire — sans quoi on interprète une propriété de la sonde comme une propriété de l'objet.

### 4.8 — Clôture de l'étape 2 : la chambre « gardé=1 » sous forçage générique (script `partition_Fy_depth2b_2Dforce.py`)

**Méthode retenue (Benoit), en quatre points, à traiter comme diagnostic expérimental et non comme nouvelles catégories du modèle :** (1) automorphismes du graphe courant ; (2) l'état pertinent est-il réellement fixé par l'un d'eux ; (3) casser les symétries du protocole en préservant celle qu'on teste ; (4) observer ce qui survit.

**Test.** Même chambre « gardé=1 » que dans la première exploration de l'étape 2 (Aut(A₁)=1, aucune symétrie de graphe disponible), même scan (φ₄,φ₅), même forçage générique 2D (37°, Uy≠0) que le contrôle de la chambre « gardé=3 ». Résultat : les deux bandes **survivent** — gardé=4 : 6,44 % (contre 5,88 % en 1D), gardé=5 : 6,44 % (contre 5,76 %), légèrement plus larges et avec un bord visiblement moins net dans le coin (0°,0°) qu'en 1D (figure comparative `partition_Fy_N6_etape2_kept1_compare.png`). C'est le cas « survivent mais se déplacent/se courbent » anticipé par Benoit : ces murs ne sont pas des artefacts du protocole mono-axe.

**Point de rigueur.** Les deux aires sortent exactement égales (232/232 points de grille). Vérifié que ce n'est *pas* une symétrie cachée : H₄(t\*) ≠ H₅(t\*) explicitement (H₄=[0,04081; 0,03087], H₅=[0,04014; 0,03036], écart réel ≈1,6 %, cohérent avec l'asymétrie de A₁ — le nœud 1 relié directement à 0 apporte plus à 4 par un chemin court que le nœud 2, non relié à 0, n'en apporte à 5). L'égalité des aires à ce grillage est donc une coïncidence de comptage à cette résolution, pas une propriété structurelle — la frontière réelle est légèrement asymétrique mais trop finement pour se voir sur une grille 60×60 à cet endroit.

**Bilan des trois expériences, comme tableau de diagnostic (pas trois nouvelles entités) :**

| paroi | origine | sous forçage générique |
|---|---|---|
| φ₁=φ₂ (chambre nb=3 candidats, étape 1) | coïncidence de score, τ libre (pas de dynamique) | sans objet — pas de protocole à casser |
| φ₄=φ₅ dans « gardé=3 » | Fix(σ), σ=(1 2)(4 5) ∈ Aut(A₁) | survit à l'identique (§4.7) |
| φ₄=−φ₅ dans « gardé=3 » | symétrie R_y du protocole mono-axe | disparaît (§4.7) |
| bandes {4,5} dans « gardé=1 » | coïncidence de score générique (Aut(A₁)=1, rien à fixer) | survit, déformée (§4.8) |

Les trois situations attendues sont maintenant toutes observées côte à côte sur le même témoin N=6 : mur structurel, mur induit par le protocole, mur transverse générique. Leçon retenue pour la suite du chantier F_y/∼_N : avant de qualifier une paroi numérique, s'assurer qu'elle appartient à F_y et pas seulement à la sonde qui le traverse.

**Statut V5.6 : incorporé.** L'ensemble des sections 4.9 à 4.13 (proposition de finitude, taxonomie structurel/protocolaire/transverse, croissance 3→3→5→5, zoom, raffinement adaptatif, réinjection combinatoire) est désormais rédigé dans le .tex, section « Exploration à profondeur finie des fibres d'opacité » (§11 de la V5.6). Relu ligne à ligne contre les scripts et les sorties numériques : chiffres et description concordent (9 puis 26 chemins au coin, 60/256 cellules raffinées, caveat sur Aut(A₁)=1 reformulé exactement comme convenu). Le .tex distingue en outre plus finement que ce document ne le faisait deux niveaux de certitude sur la réinjection (récurrence combinatoire vérifiée sur l'arbre calculé vs domination de τ₁ non démontrée uniformément) — reformulation à reprendre ici si ce document est retravaillé. Ce qui suit reste la version de travail détaillée ; le .tex en donne la forme publiable et plus prudente.

### 4.9 — Étape 3 : croissance de 𝒫_k avec k (scripts `depth_growth.py` / `plot_depth_growth.py`)

**Question posée (Benoit).** Non plus une carte isolée à profondeur fixée, mais la suite k=1,2,3,4,5 : nombre de chambres algébriques et de composantes connexes géométriques, nombre de parois nouvelles à chaque profondeur, quelles scissions proviennent d'une nouvelle concurrence ouverte par K* et lesquelles sont portées par une symétrie — bref, un premier indice quantitatif pour ou contre la tameness à profondeur finie.

**Méthode.** Même témoin N=6, même point de départ que le §4.8 (chambre « gardé=1 », Aut(A₁)={e}, forçage 2D générique 37°), même grille (φ₄,φ₅) — réduite à 32×32 pour pouvoir répéter le cycle RK4→Kairos jusqu'à cinq fois. La règle de Kairos a été entièrement vectorisée (retrait/ajout par similarité, remise à l'échelle de P et V) pour pouvoir suivre, à chaque point de grille, le chemin complet des voisinages successifs de i* ; deux points portent le même « chemin » s'ils ont traversé exactement la même suite de retraits/ajouts. Pour chaque scission d'un groupe en plusieurs sous-groupes à une profondeur donnée, l'origine est testée directement (pas seulement inférée) : on calcule Aut(A_avant), on restreint aux automorphismes qui fixent i*, et on cherche si l'un d'eux envoie l'issue d'un enfant sur l'issue de l'autre — structurel si oui, transverse sinon.

**Résultat.**

| k | chambres algébriques | composantes connexes | N_{∂,k}^{grid} nouvelles depuis k−1 |
|---|---|---|---|
| 2 | 3 | 3 | 126 |
| 3 | 3 | 3 | 0 |
| 4 | 5 | 5 | 4 |
| 5 | 5 | 5 | 0 |

(N_{∂,k}^{grid} : nombre de paires de cellules de grille voisines portant des chemins différents — un compte discret de transitions, pas le nombre géométrique de parois au sens continu ; un même mur long est compté autant de fois qu'il traverse de paires de cellules. Terminologie corrigée sur remarque de Benoit, pour ne pas confondre les deux dans le texte théorique.)

À k=2 on retrouve les trois chambres déjà connues (gardé=1 : 87,9 %, gardé=4 et gardé=5 : ~6,05 % chacune sur cette grille 32×32, cohérent avec le §4.8 à la résolution près). À k=3, aucune nouvelle scission : les trois chemins se prolongent chacun de façon univoque au Kairos suivant. À k=4, la même compétition {4,5} réapparaît, mais *à l'intérieur* des deux petites bandes elles-mêmes : chacune se scinde en une sous-bande dominante et un reliquat minuscule (61+1 points, puis 2+60 points, sur 1024 au total — donc <0,2 % de la grille). Les deux scissions détectées sont classées **transverses** (aucun automorphisme de A_avant fixant i* ne les échange). À k=5, plus rien de nouveau.

**Point de rigueur.** Les deux reliquats de k=4 (1 et 2 points de grille) sont trop petits pour être autre chose qu'une indication : à cette résolution on ne peut pas exclure qu'il s'agisse d'un effet de bord de la discrétisation près de la frontière déjà connue plutôt que d'une compétition réellement nouvelle. Une grille plus fine localement, centrée sur ce coin, serait nécessaire avant de les qualifier de troisième génération de mur authentique. La figure `partition_Fy_N6_croissance_k2a5.png` montre d'ailleurs ce reliquat comme un point à peine visible dans le coin (φ₄,φ₅)≈(0°,0°). **Suite au §4.10 : le zoom local tranche cette question.**

**Lecture.** Sur ce témoin et dans cette fenêtre (k≤5), la croissance de 𝒫_k n'explose pas : elle passe de 3 à 5 chambres puis se stabilise deux fois de suite (k=2→3 et k=4→5 sans rien de nouveau). C'est un premier point, minimal mais réel, en faveur de l'intuition de tameness à profondeur finie évoquée par Benoit — à tempérer par deux limites explicites : (i) la branche part d'un graphe sans automorphisme non trivial (Aut(A₁)={e}), mais cela n'exclut pas en soi une réapparition ultérieure de symétries (on l'avait vu sur le suivi profond antérieur, où |Aut(A_k)| pouvait remonter après être tombé à 1) — dans cette expérience précise, le test direct (auts de A_avant fixant i*, à chaque scission) montre qu'aucune des scissions observées jusqu'à k=5 n'est en fait portée par une telle symétrie, mais ce n'est pas une conséquence automatique du point de départ, c'est une observation ; **suite au §4.11 : la même expérience depuis « gardé=3 » (Aut(A₁)=4), où une symétrie structurelle est bien active dès k=2, sert de comparaison directe.** (ii) une seule fenêtre 2D du F_y complet (φ₄,φ₅ à τ₁,τ₂,τ₃ fixés) a été explorée — la conclusion porte sur cette coupe, pas sur F_y dans son ensemble.

### 4.10 — Zoom local sur les reliquats de k=4 (script `depth_growth_zoom.py`)

**Question.** Les deux reliquats de 1 et 2 points de grille trouvés en §4.9 à k=4 sont-ils un artefact de discrétisation, ou une vraie région ouverte trop fine pour la grille 32×32 ?

**Méthode.** Même protocole, mais fenêtre restreinte à (φ₄,φ₅)∈[−5°,25°]² (le coin où vivaient les deux reliquats), grille 60×60 non torique sur cette fenêtre — soit un facteur ~20 de résolution locale en plus, comme suggéré par Benoit plutôt qu'un raffinement global.

**Résultat.** Ce n'est pas un artefact. À k=4, la fenêtre zoomée révèle **9 chemins distincts avec des aires substantielles** (de 56 à 1062 points de grille sur 3600, aucune proche de 1) — un motif en croix, visuellement la signature de la même compétition {4,5} qui se répète *à l'intérieur d'elle-même* à l'échelle plus fine, de façon manifestement structurée et non bruitée (figure `partition_Fy_N6_zoom_coin.png`). Les deux reliquats de la grille grossière n'étaient donc que la trace, sous-échantillonnée, d'une vraie sous-structure récursive — pas un artefact numérique.

**Conséquence pour le §4.9.** Le compte « 5 chambres, stable à k=5 » de la grille 32×32 sous-estime la complexité réelle de 𝒫_4 sur cette coupe : au moins 9 chambres y sont présentes, visibles seulement après raffinement local. La lecture qualitative (pas d'explosion, motif embîté plutôt que nouvelle architecture globale — cf. citation de Benoit ci-dessous) reste correcte, mais le compte numérique de 𝒫_k n'est fiable qu'à résolution suffisante ; toute affirmation future sur « le nombre de chambres à profondeur k » devra préciser à quelle résolution.

### 4.11 — Comparaison avec/sans symétrie active : la chambre « gardé=3 » (script `depth_growth_kept3.py`)

**Question (Benoit).** Refaire le même suivi k=2,…,5 depuis la chambre « gardé=3 » (Aut(A₁)=4, σ=(1 2)(4 5) et τ=(0 3)), où des symétries structurelles peuvent réellement intervenir, pour comparer à la branche sans symétrie du §4.9.

**Méthode.** Identique au §4.9 (même grille 32×32, même forçage 2D générique, même test direct d'origine structurelle/transverse à chaque scission), mais depuis A₁ = graphe « gardé=3 » et avec τ₁=τ₂ imposé exactement dans l'état de départ (pour rester dans Fix(σ), comme au §4.7).

**Résultat.**

| k | chambres | composantes connexes | N_{∂,k}^{grid} nouvelles |
|---|---|---|---|
| 2 | 3 | 3 | 126 |
| 3 | 3 | 3 | 0 |
| 4 | 5 | 5 | 4 |
| 5 | 5 | 5 | 0 |

**Exactement la même courbe de croissance que la branche « gardé=1 » (3→3→5→5).** Mais cette fois, le test automatique d'origine détecte correctement, dès k=2, une scission **structurelle** : {1,2,5} vs {1,2,4} — c'est précisément le mur φ₄=φ₅ déjà identifié à la main au §4.7 comme Fix(σ), retrouvé ici automatiquement par le critère « un automorphisme de A_avant fixant i* échange les deux issues ». Les deux autres scissions de k=2 (contre la branche « gardé=3 » elle-même) sont transverses, comme les deux nouvelles de k=4 (réapparition localisée de la même compétition, cette fois entre gardé=3/gardé=4 et gardé=5/gardé=3, toujours sans symétrie qui les échange).

**Lecture.** C'est la comparaison directe que demandait Benoit. Malgré la présence d'un vrai mur structurel dès k=2, la courbe de croissance de 𝒫_k est identique, chiffre pour chiffre, à celle de la branche sans symétrie active : ni la présence ni l'absence de symétrie ne semble à elle seule piloter le rythme de croissance sur ce témoin — la stabilisation à k=3 et k=5 se produit dans les deux cas, et l'unique épisode de croissance (k=4) est transverse dans les deux branches. C'est un premier élément empirique, encore modeste (un seul témoin, une seule coupe 2D, k≤5), mais allant dans le sens d'une complexité qui reste organisée par raffinements locaux plutôt que par explosion globale, qu'une symétrie structurelle soit active ou non — la formulation prudente que proposait Benoit : *« à profondeur finie, la complexité observée croît par raffinements locaux, pas par explosion globale »*, sur cette coupe et pour ce protocole.

### 4.12 — Stratégie adaptative sur tout le tore (Benoit, point A) : le coin de §4.10 n'est pas isolé (scripts `iws_kairos_core.py`, `adaptive_refine.py`, `adaptive_refine_zoom2.py`)

**Méthode.** Mécanique commune extraite dans `iws_kairos_core.py` (partagée désormais par tous les scripts de ce chantier). Grille grossière 16×16 sur tout le tore (φ₄,φ₅), profondeur k=4, chambre « gardé=1 ». Une cellule grossière est raffinée seulement si ses 4 coins ne portent pas tous la même étiquette (elle est traversée par un mur) ; chaque cellule flaguée est alors résolue par une grille locale fine (12×12) sur son seul rectangle — raffinement local récursif, pas une grille fine partout.

**Résultat.** 60 des 256 cellules grossières sont flaguées — exactement les deux bandes frontière (bord vert/« gardé=1 » contre bleu/« gardé=4 » vers φ₄≈11° et vers φ₄≈349° ; bord vert contre orange/« gardé=5 » vers φ₅≈11° et vers φ₅≈349°) plus les quatre coins où bleu et orange se rencontrent (dont celui déjà étudié en §4.10). La richesse trouvée après raffinement n'est **pas uniforme le long de la frontière** : sur le bord « proche » du coin étudié (φ₄≈11° sur toute sa longueur, φ₅≈11° sur toute sa longueur) elle est constante à 4 étiquettes fines (et jusqu'à 6 à un endroit) contre 2 aux coins grossiers ; sur le bord « loin » (φ₄≈349°, φ₅≈349°) elle est plus faible mais non nulle, constante à 3 étiquettes — sauf en un point isolé, (φ₄,φ₅)≈(214°,349°), qui monte à 5 sans raison apparente dans les voisins immédiats (figure `partition_Fy_N6_adaptive_site2.png`) ; les quatre coins sont les plus riches (5 à 9 étiquettes, cf. §4.10 pour celui déjà détaillé).

**Lecture.** Le raffinement adaptatif confirme que la sous-structure trouvée en §4.10 n'est pas une curiosité isolée du seul coin étudié : la même recompétition {4,5} existe, à une intensité variable, tout le long de la frontière entre la chambre majoritaire et les deux bandes fines — plus forte près des coins (où deux frontières se recoupent), plus faible mais réelle loin d'eux, avec au moins une anomalie ponctuelle non expliquée qui mériterait un raffinement encore plus local si on la recroise un jour. Le point méthodologique de Benoit est validé : une grille uniforme fine sur tout le tore aurait coûté (360/(30/12))² ≈ 20 700 points pour atteindre la même résolution locale que les 60×144 = 8640 points effectivement utilisés ici, et sans même savoir où regarder au départ.

### 4.13 — Généalogie et récurrence du motif au coin (0°,0°), k=2 à 7 (Benoit, points B et C ; script `zoom_deep_genealogy.py`)

**Méthode.** Même fenêtre que §4.10 ([-5°,25°]², grille 60×60), poursuivie jusqu'à k=7, avec pour chaque scission : la chambre parente (chemin complet), les deux candidats qui s'échangent (différence symétrique des deux issues), et l'origine (structurel/transverse, testée comme aux §4.9-4.11).

**Résultat — un motif rigoureusement périodique.** Aucune nouvelle paire de candidats n'apparaît jamais : à **toutes** les profondeurs où une scission a lieu (k=2, 4, 6), la compétition est *exactement* la même — entre les candidats {1,4}, {1,5} et {4,5}, c'est-à-dire un partage à trois issues {1,2,3}/{2,3,4}/{2,3,5} — et toutes sont transverses. Entre deux scissions (k=3, 5, 7), aucune scission : le graphe revient *systématiquement* au même voisinage {1,4,5} pour le nœud 0, quelle que soit l'issue retenue au tour précédent (tableau des 26 chemins finaux à k=7 dans la sortie du script — tous alternent {2,3,4}/{2,3,5}/{1,2,3} puis {1,4,5}, sans exception).

**Explication structurelle.** Ce n'est pas un hasard numérique : dès que le voisinage de 0 vaut {1,2,3} (ou {2,3,4}, ou {2,3,5}), ses deux non-voisins restants sont toujours exactement {4,5} (ou {1,5}/{1,3} selon le cas — dans chaque cas |non-voisins|=2=m), donc la règle de Kairos les **rajoute tous les deux automatiquement**, sans compétition — exactement le mécanisme sans-compétition-sur-l'ajout déjà repéré en §4.9. Et parmi {1,4,5}, c'est toujours τ₁ qui reste le plus aligné avec τ₀ à cet instant (τ₁ démarre le plus proche de τ₀ et n'est jamais assez perturbé par le reste de la dynamique pour perdre ce rang), donc c'est toujours 1 qui est retenu au retour. Le système repasse donc *nécessairement* par {1,4,5} à chaque étape impaire : c'est une réinjection combinatoire exacte, au sens déjà rencontré ailleurs dans ce chantier (témoin N=6 profondeur/réinjection, §4.3), pas une coïncidence propre à ce coin.

**Réponse à la question de Benoit.** Ni répétition ponctuelle isolée, ni mécanisme qui invente sans cesse de nouveaux candidats : c'est une **hiérarchie auto-similaire exacte sur un alphabet fini** — un arbre ternaire {1,4,5} qui se referme sur lui-même à chaque paire d'étapes, quelle que soit la branche descendue. Nombre de chemins distincts : 3 (k=2), 9=3² (k=4), 26≈3³=27 (k=6, un chemin manquant probablement par effet de bord de la fenêtre [-5°,25°], à vérifier avec une fenêtre légèrement plus large si le point importe). Le motif « en croix » du §4.10 est donc la coupe à k=4 de cet arbre ; à k=6 il se répète à l'intérieur de chacune de ses 9 branches, toujours avec le même triplet {1,4,5} (figure `partition_Fy_N6_genealogie_k4_6_7.png`).

**Portée et limite.** Ce résultat est propre à ce témoin et à ce coin précis de F_y — il tient à un fait numérique local (τ₁ toujours dominant parmi {1,4,5}) qui n'a aucune raison de se reproduire ailleurs sur le tore ou sur un autre graphe de départ ; rien n'indique que *toute* la complexité de 𝒫_k se réduit à ce genre d'arbre fini. Mais c'est la première fois, dans ce chantier, qu'on observe un mécanisme complet et compris de bout en bout expliquant pourquoi une hiérarchie a la forme qu'elle a, plutôt que de simplement le constater sur un tableau de comptage.

**Correction de vocabulaire (relecture a posteriori).** « Le système reste fini » ci-dessus est trompeur : à k fixé le nombre de chemins est trivialement fini (grille finie), mais il **croît sans borne avec k** — 3, 9, 26≈27, et la mécanique de réinjection prédit 3^{k/2} indéfiniment tant que τ₁ reste dominant, donc une croissance exponentielle en k, pas un plafond. Ce que ce site du témoin N=6 montre n'est donc pas une preuve de croissance bornée, mais l'inverse : une croissance non bornée entièrement **structurée** (arbre ternaire exact, prévisible, auto-similaire) plutôt qu'anarchique. C'est une distinction importante pour la question de tameness : celle-ci ne demande pas que le nombre de chambres reste petit, mais que sa croissance soit *contrôlée* par un mécanisme — ce qui est exactement ce qu'on a ici, à ce site précis, et c'est plus fort qu'une simple stabilisation.

### 4.14 — Premier pas sur le témoin N=9 (Benoit, test de résistance) : structurel et transverse coexistent déjà à profondeur 1 (scripts `iws_kairos_core_gen.py`, `n9_etape1.py`, `plot_n9_etape1.py`)

**Témoin.** Graphe construit précédemment pour le crash-test du lemme orbital (§3, Obstruction orbitale) : N=9, arêtes {(0,1),(0,2),(0,3),(4,5)}, nb(0)={1,2,3} (orbite de taille 3 sous Aut(A₀)), nn(0)={4,5}(orbite 2) ∪ {6,7,8}(orbite 3), |Aut(A₀)|=72 (3!·2·3! : permutations de {1,2,3}, échange (4 5), permutations de {6,7,8}) — confirmé par calcul direct. m=min(2,|nb|,|nn|)=2 des deux côtés : côté retrait, m=2 ne peut pas s'accorder à l'orbite de taille 3 (obstruction structurelle possible) ; côté ajout, m=2 coïncide exactement avec l'orbite {4,5} (sélection équivariante possible).

**Différence avec le crash-test initial.** Le crash-test du lemme orbital utilisait un τ *construit* pour forcer un résultat précis. Ici, on reprend la mécanique générique du chantier F_y/∼_N (même code que pour N=6, généralisé à N quelconque dans `iws_kairos_core_gen.py`) : un scan 2D générique (φ₂,φ₆) sur 60×60, nœuds 1,3,4,5,7,8 fixés à des angles distincts (1:15°, 3:45°, 4:5°, 5:355°, 7:200°, 8:160°), forçage générique sur le nœud 0, même régime et mêmes paramètres physiques que N=6.

**Résultat — dès la profondeur 1.** Quatre chemins apparaissent : {1,4,5} (79,4 %, dominant), {2,4,5} (12,2 %), {1,4,6} (7,2 %), {2,4,6} (1,1 %) — cohérent avec la mécanique attendue : node 3 (fixé à 45°) ne l'emporte jamais sur node 1 (fixé à 15°, plus proche de 0°), donc seul {1,2} s'échangent pour le retrait ; côté ajout, node 4 l'emporte systématiquement (aucune sortie de type {5,6} observée — cohérence interne vérifiée : H,V,P et donc la trajectoire de τ₀ ne dépendent d'aucun angle scanné, donc la comparaison 4 vs 5, tous deux fixes, a un vainqueur unique et constant sur toute la grille). Le test automatique d'origine classe correctement les scissions : {2,4,6}↔{1,4,6} et {2,4,5}↔{1,4,5} sont **structurelles** (portées par la transposition (1 2), un vrai élément de Aut(A₀) puisque 1 et 2 sont jumeaux) ; les quatre autres scissions sont **transverses** (nœuds 5 et 6 dans des orbites différentes de Aut(A₀), aucune symétrie ne peut les échanger) — figure `partition_Fy_N9_etape1.png`.

**Ce que ça apporte déjà par rapport à N=6.** Sur le témoin N=6, la coexistence structurel/transverse n'apparaissait qu'à partir de la profondeur 2 (le premier Kairos y était toujours purement combinatoire-transverse, cf. §4.4). Ici, dès la **profondeur 1**, les deux mécanismes sont présents simultanément dans la même partition — signe que l'arité et la richesse de la fibre d'opacité dépendent fortement du graphe de départ, exactement comme Benoit l'anticipait. Pas encore de conclusion sur la croissance à profondeur supérieure ni sur une éventuelle réinjection : c'est l'étape suivante, non encore lancée.

### 4.15 — Les 4 chambres de N=9 poussées en parallèle à k=4/5 (Benoit, plan explicite anti-biais de sélection) : diagnostics Aut(A₁), et un piège méthodologique trouvé puis corrigé (scripts `n9_depth_growth_4branches.py`, `n9_depth_growth_4branches_zoom.py`, `plot_n9_4branches_zoom.py`)

**Protocole demandé.** Plutôt que de choisir une chambre de profondeur 1 à approfondir, Benoit a demandé de pousser les quatre en parallèle ({1,4,5}, {2,4,5}, {1,4,6}, {2,4,6}) jusqu'à k=4/5, avec les mêmes diagnostics pour chacune, afin de comparer isolément l'axe structurel (1↔2, transposition (1 2)∈Aut(A₀)) et l'axe transverse (5↔6, orbites distinctes).

**Diagnostics directs sur A₁ (indépendants de toute simulation).**

| chambre A₁ | \|Aut(A₁)\| | orbites |
|---|---|---|
| {1,4,5} | 240 | {0}, {1}, {2,3,6,7,8}, {4,5} |
| {2,4,5} | 240 | {0}, {1,3,6,7,8}, {2}, {4,5} |
| {1,4,6} | 48 | {0}, {1,6}, {2,3,7,8}, {4}, {5} |
| {2,4,6} | 48 | {0}, {1,3,7,8}, {2,6}, {4}, {5} |

Point notable : les A₁ pour {1,4,5} et {2,4,5} sont **isomorphes** (même forme d'orbites, juste 1↔2 renommés), tout comme {1,4,6} et {2,4,6}. Toute différence de comportement entre membres d'une même paire ne peut donc pas venir de la structure combinatoire de A₁ elle-même — elle vient forcément du contexte τ (angles fixés différemment pour les nœuds non scannés).

**Premier essai, piège trouvé : biais de résolution.** La continuation directe de la grille (φ₂,φ₆) de k=1 (celle de §4.14) vers k=2..5 répartit très inégalement les 3600 points entre les quatre chambres (2860 / 440 / 260 / 40, exactement les aires de k=1) — et ce déséquilibre reste **identique à chaque profondeur** (vérifié explicitement : aucun point ne change de groupe d'origine). Les 𝒫_k bruts obtenus (10/6/9/5 à k=5) ne sont donc **pas comparables tels quels** : la chambre {2,4,6} n'a que 40 points pour détecter des scissions, contre 2860 pour {1,4,5}. C'est exactement le biais que le protocole de Benoit visait à éviter à l'échelle du choix de chambre — il réapparaît, plus discrètement, à l'intérieur même de la comparaison si on ne corrige pas la résolution.

**Correction : zoom local à budget égal.** Pour chaque chambre, un point intérieur représentatif a été choisi (moyenne circulaire de la région, reprojetée sur un point du calcul original) puis une grille fraîche 60×60 (3600 points, rayon ±15° en φ₂ et φ₆) a été simulée **depuis k=0** autour de ce point, indépendamment pour les quatre chambres. Vérification : k=1 confirme 3600/3600, 3600/3600, 3480/3600, 3480/3600 points dans la chambre attendue (la légère contamination pour {1,4,6}/{2,4,6} vient du rayon qui déborde légèrement sur la frontière en φ₆≈0/24° — mineur, non corrigé pour ce premier passage).

**Résultat à résolution égale, après correction complète (voir ci-dessous) — |𝒫_k^loc|, k=1→5 :**

| chambre | k=1 | k=2 | k=3 | k=4 | k=5 | nature des scissions |
|---|---|---|---|---|---|---|
| {1,4,5} | 1 | 1 | 1 | 1 | 1 | **aucune** — plate sur toute la fenêtre (confirmé deux fois, voir contrôle d'équivariance) |
| {2,4,5} | 1 | 2 | 2 | 3 | 3 | transverse uniquement |
| {1,4,6} | 1 | 2 | 2 | 3 | 3 | transverse uniquement |
| {2,4,6} | 1 | 3 | 3 | 6 | 6 | mixte, **une scission structurelle confirmée**, même témoin à k=2 et k=4 (voir généalogie) |

Figure `partition_Fy_N9_4branches_zoom_k5.png` : quatre cartes côte à côte, même échelle, même palette — {1,4,5} est une bande unicolore, {2,4,6} affiche une structure 2D non triviale (pas de simples bandes, une géométrie en îlots). *(Figure générée avant la correction de rééchantillonnage ci-dessous pour {1,4,6}/{2,4,6} ; valides pour {1,4,5}/{2,4,5}, légèrement optimistes en nombre de chambres pour les deux autres — à régénérer si une version figée est nécessaire.)*

**Lecture.** La chambre la plus massive en aire (79,4 % de la fibre à k=1, {1,4,5}) est localement la plus pauvre en profondeur, tandis que la plus marginale (1,1 %, {2,4,6}) est de loin la plus riche, avec la seule occurrence structurelle du lot. C'est une instance concrète de ce que Benoit voulait vérifier en refusant de choisir une chambre a priori : se fier à l'aire (ou à l'intuition de la chambre « dominante ») aurait conduit droit vers la branche la moins intéressante. |Aut(A₁)| n'est pas non plus un bon prédicteur scalaire : 240 donne 1 ou 3 chambres selon la branche, 48 donne 3 ou 6 — ce qui compte est l'action concrète des symétries sur l'état caché, pas leur seul cardinal. Fait notable : {2,4,5} et {1,4,6} (deux chambres a priori sans rapport, l'une sur l'axe structurel, l'autre sur l'axe transverse) produisent exactement la même suite 1,2,2,3,3 — à creuser, mais cohérent avec l'idée que c'est la position dans la fibre plutôt que l'étiquette qui organise la richesse.

**Contrôle d'équivariance (demandé par Benoit, fait) : la différence 1,4,5 vs 2,4,5 n'était qu'un artefact de contexte τ.** Première version de cette section : {1,4,5} donnait une fenêtre plate (1,1,1,1,1) alors que {2,4,5}, zoomée sur un point choisi indépendamment, donnait 1,2,2,3,3 — ce qui invitait à tort à lire un effet de l'échange 1↔2. Contrôle propre effectué : σ=(1 2)∈Aut(A₀) (vérifié), et la construction du graphe est bien équivariante (σ·A₁^{1,4,5}=A₁^{2,4,5}, vérifié numériquement). Le point-centre du zoom {1,4,5} a été transporté par σ (angles de 1 et 2 échangés, reste inchangé) et le même protocole (même rayon, balayage des images par σ des directions scannées) relancé à ce point transporté : il tombe bien dans la chambre {2,4,5} au premier Kairos, **et reproduit exactement la même suite plate 1,1,1,1,1** — pas la suite 1,2,2,3,3 trouvée à l'autre centre. Ceci verrouille à la fois (a) la numérique est correctement équivariante, et (b) la richesse différente observée entre {1,4,5} et {2,4,5} au premier essai venait bien du contexte historique τ (deux points non reliés par σ), pas de l'étiquette 1 ou 2 en tant que telle — exactement l'hypothèse de Benoit, confirmée. Script `n9_equivariance_control.py`.

**Correction du rééchantillonnage pour {1,4,6}/{2,4,6} (demandée par Benoit, faite).** La contamination de bord (~120/3600 points hors chambre, visible dans la version précédente de ce tableau) a été éliminée par rejet : sur-échantillonnage (grille 90×90, rayon élargi au besoin), filtrage aux points dont l'étiquette réelle à k=1 est exactement celle attendue, puis conservation de 3600 points garantis dans la chambre (fenêtre résultante irrégulière, non rectangulaire). Résultat : {1,4,6} passe de l'ancienne suite contaminée (2,3,3,4,4) à la suite propre **1,2,2,3,3** ; {2,4,6} passe de (2,5,5,10,10) à **1,3,3,6,6**. {2,4,6} reste de loin la plus riche des quatre, avec la même scission structurelle confirmée deux fois (k=2 et une fois de plus, depuis deux parents différents, à k=4). Script `n9_resample_conditioned.py`.

**Généalogie de la scission structurelle de {2,4,6} (question de Benoit : même automorphisme à k=2 et k=4, ou un autre ?).** Réponse nette : **le même**, à chaque occurrence. Les trois occurrences de la scission {1,3,6}↔{1,2,3} (à k=2 depuis le parent {2,4,6}, et à k=4 depuis deux parents différents — l'un passé par {1,3,4}, l'autre par {1,2,3} à l'étape intermédiaire) admettent exactement la même famille de témoins dans Aut(A_parent), de cardinal 4 à chaque fois, dont le témoin minimal est systématiquement **la simple transposition (2 6)** (fixant tous les autres nœuds). (2 6) est précisément l'automorphisme qui engendre l'orbite {2,6} déjà repérée dans A₁^{2,4,6} (§ diagnostics ci-dessus) — il survit donc intact à travers le recâblage intermédiaire, à deux profondeurs différentes et deux chemins différents. C'est une **réinjection structurelle authentique** (même symétrie qui revient, pas une nouvelle obstruction accidentelle) — le premier cas de ce type observé sans construction artificielle, à comparer avec la réinjection combinatoire (différente en nature) du site N=6, §4.13. Script `n9_246_genealogy_structurel.py`.

**Limites restantes.** (1) Un seul point de zoom par chambre pour {1,4,5}/{2,4,5} (le contrôle d'équivariance porte sur deux points précis, pas sur l'ensemble des deux régions) — rien ne dit que la platitude de {1,4,5} est uniforme sur toute la région à 79,4 % d'aire. (2) La figure `partition_Fy_N9_4branches_zoom_k5.png` reflète encore l'ancienne version contaminée pour {1,4,6}/{2,4,6} (valeurs légèrement optimistes) ; les tableaux de ce paragraphe font foi, pas l'image telle quelle. **Prochaine étape naturelle, réservée par Benoit pour ensuite :** raffinement adaptatif profond sur la chambre {2,4,6}, seule candidate montrant une richesse structurelle avérée, avec cette fois un objectif précis : vérifier si (2 6) continue de réapparaître comme témoin à des profondeurs encore supérieures (k=6, k=7), ou si une obstruction d'un autre type finit par apparaître.

### 4.16 — {2,4,6} à k=6,7 : (2 6) comme témoin persistant, et récurrence à travers l'arbre, pas seulement le long d'une branche (Benoit, deux questions ciblées ; script `n9_246_deep_26.py`)

**Questions posées.** (1) (2 6) reste-t-il témoin à chaque nouvelle scission structurelle, avec la même famille orbitale, ou le stabilisateur change-t-il ? (2) Une branche qui n'a pas pris la scission structurelle tôt peut-elle revenir plus tard vers une configuration où (2 6) redevient actif — récurrence dans l'arbre, pas seulement le long d'une lignée ?

**Protocole.** Reprise de l'échantillon conditionné de {2,4,6} (§4.15, 3600 points garantis dans la chambre), poussé jusqu'à k=7. À chaque nœud de l'arbre : test direct de (2 6) ∈ Aut(A_parent) (indépendamment de toute scission), et pour chaque scission structurelle trouvée, test si (2 6) fait partie des témoins.

**Réponse à (1) : oui, systématiquement, jusqu'à k=7.** Toutes les scissions structurelles trouvées (k=2 : 1 occurrence ; k=4 : 2 occurrences, depuis deux parents distincts ; k=6 : 2 occurrences, depuis deux parents distincts) admettent (2 6) comme témoin, toujours avec exactement **4 témoins équivalents** (même cardinal à chaque fois — le stabilisateur ne s'enrichit ni ne s'appauvrit). Aucune scission structurelle portée par une autre symétrie n'a été trouvée à ce stade : (2 6) reste, jusqu'à k=7, le seul mécanisme structurel actif sur ce témoin.

**Réponse à (2) : oui, récurrence confirmée à travers l'arbre.** En retraçant les chemins parents des scissions de k=4 et k=6, on voit que (2 6) ne réapparaît pas seulement sur une lignée figée : il redevient actif **chaque fois qu'une branche revient au voisinage {2,4,6} de 0**, quel que soit le chemin emprunté pour y revenir. Exemple concret : la branche {2,4,6}→{1,3,4} (k=2, pas de scission structurelle, (2 6) présent dans Aut mais inactif) → {2,4,6} (k=3, réinjection) retrouve à k=4 exactement la même scission structurelle {1,3,6}↔{1,2,3} portée par (2 6) ; de même la branche {2,4,6}→{1,2,3}→{2,4,6} et, à k=6, les deux branches {2,4,6}→{1,3,4}→{2,4,6}→{1,2,3}→{2,4,6} et {2,4,6}→{1,2,3}→{2,4,6}→{1,2,3}→{2,4,6}. Autrement dit : ce n'est pas « une branche répète toujours la même chose », c'est « revenir à l'état de voisinage {2,4,6} réactive (2 6), d'où qu'on vienne ». 𝒫_k^loc pour cette chambre : 1,3,3,6,6,10,11 (k=1→7).

**Lecture et formulation retenue (Benoit) :**

> (2 6) ∈ Aut(A_k) réapparaît comme témoin minimal de la même scission à plusieurs profondeurs, et cette réapparition est associée au retour au même voisinage plutôt qu'à une seule trajectoire — une vraie récurrence structurale au sens combinatoire, par opposition à une simple répétition le long d'une branche.

**Contraste N=6 / N=9, à garder comme résumé de ce chantier :**

> N=6 : réinjection **combinatoire locale** d'une même compétition (même triplet de candidats {1,4,5} revient, §4.13). N=9 : réinjection **structurelle spontanée** d'une même symétrie ((2 6) revient comme témoin, ce §). Deux mécanismes de croissance organisée, de nature différente.

**Limite à garder en tête.** Pas encore d'occurrence d'une scission structurelle portée par une symétrie *autre* que (2 6) — impossible de dire si c'est parce qu'il n'y en aura jamais sur ce témoin, ou simplement parce qu'on n'a pas encore assez creusé (k≤7 seulement, un seul point de zoom). Prochaine étape naturelle si Benoit veut pousser encore : profondeurs 8-10, ou un deuxième point de zoom dans la même chambre {2,4,6} pour vérifier que ce mécanisme n'est pas spécifique au point précis choisi.

**Second point de zoom (Benoit, contrôle de robustesse plutôt que profondeur 8-10) : même mécanisme confirmé (scripts `n9_find_second_center.py`, `n9_246_deep_26_center2.py`).** Question posée : le mécanisme (2 6) est-il une propriété locale robuste de la chambre {2,4,6}, ou seulement du voisinage particulier du premier point ? Un scan complet de la région {2,4,6} au niveau k=1 montre qu'elle forme un seul arc continu (φ₂∈[328°,375°] mod 360, φ₆∈[0°,24°] environ ; le premier centre (348°,12°) était proche du milieu). Un second centre a été choisi près d'un bord de cet arc, sans optimisation de richesse : (φ₂,φ₆)=(334°,18°), à 14° du premier.

Résultat : **même témoin, même scission, même mécanisme de réactivation**. Les deux occurrences structurelles trouvées à ce second centre (k=4 et k=6, toutes deux via un retour au voisinage {2,4,6} après passage par {1,2,3}) portent exactement la même paire d'étiquettes {1,3,6}↔{1,2,3}, avec (2 6) comme témoin et le même cardinal de 4 témoins équivalents qu'au premier centre. La richesse brute est plus faible (𝒫_k^loc : 1,2,2,4,4,5 contre 1,3,3,6,6,10 au premier centre — ce coin de la fibre est moins riche, mais structurellement identique) : conforme au premier des trois scénarios envisagés par Benoit (« même (2 6), même réactivation → mécanisme local robuste de cette chambre »), pas aux deux autres (symétrie inactive, ou autre symétrie active).

**Conclusion provisoire sur N=9, point d'arrêt convenu avec Benoit.** (2 6) apparaît comme une propriété structurelle robuste de la chambre {2,4,6} elle-même — pas un artefact du point de départ choisi — qui se réactive chaque fois que le système revient au voisinage {2,4,6} de 0, quel que soit le chemin emprunté. Le contraste retenu avec N=6 (§4.13) : réinjection combinatoire locale d'un même problème de classement (N=6) contre réactivation d'une même symétrie structurelle au retour d'une configuration (N=9) — deux formes différentes de croissance organisée. Sur décision de Benoit, le chantier numérique N=9 s'arrête ici pour le moment ; prochaine étape : retour à la consolidation du .tex (V5.6/V5.7) plutôt que la poursuite de la collecte de Kairos.

### 4.17 — Chantier de minimalité (Benoit, « je lancerais ce chantier maintenant ») : instrumentation numérique de la chaîne 𝔐 ⊃ 𝒰₅ ⊃ 𝒰₄ ⊃ 𝒰₃, trois paires de référence, et un fait mécanique général nouveau sur τ (scripts `nerode_separating_families.py`, `nerode_matrix_full.py`, `nerode_u5_diagnose.py`, `nerode_mechanism_check.py`)

**Reprise de la question posée en §5, Item 12 (reformulation de la minimalité) :** combien de richesse protocolaire faut-il réellement pour séparer deux états non-Nerode-équivalents ? Mesuré par la statistique S_{𝒰,K}(x,x')=1[∃u∈𝒰,∃k≤K : x≢_k^{(u)}x'], sur une chaîne emboîtée de familles de protocoles de plus en plus pauvres :
- **𝒰₅** : mono-axe, un seul nœud (nœud 0), direction fixée (u_y=0), amplitude variable (7 valeurs, 1.0 à 4.0 — puis 40 valeurs, 0.1 à 8.0, pour écarter un sous-échantillonnage) ;
- **𝒰₄** : forçage 2D constant, un seul nœud (nœud 0), amplitude ∈{1.5,2.5,3.5} × direction ∈ 11 angles (33 protocoles) ;
- **𝒰₃** : forçage 2D constant, nœud variable parmi un ensemble fixé, amplitude 2.5, 3 directions (18 protocoles pour N=6, 12 pour N=9).

𝒰₂ (mono-nœud, forçage variable dans le temps) et 𝒰₁ (tous nœuds, variable dans le temps) ne sont pas encore implémentés — prochaine étape si ce premier palier est jugé concluant.

**Trois paires de référence, choisies dans des données déjà calculées (pas de nouvelle recherche à l'aveugle) :**
- **Paire A** (N=6, témoin §3.22/§4.8) : paire miroir exacte construite par construction, φ_A=(15°,205°,100°,130°,310°), φ_A'=−φ_A (mod 360°) sur les nœuds 1 à 5. Choisie justement pour avoir une explication mécanique disponible a priori (voir plus bas).
- **Paire B** (N=6, coin (0°,0°), §4.10/§4.13) : deux points adjacents de la grille de `zoom_deep_genealogy.pkl`, même chambre jusqu'à k=4 (étiquette 4), séparés seulement à k=6 (étiquettes 12 vs 13) — angles fixes φ₁=10°, φ₂=40°, φ₃=2 rad (≈114,59°, convention du script d'origine, à ne pas confondre avec des degrés), et φ₄=−5° pour les deux, φ₅=0,085° contre 0,593° (différence de 0,51° seulement). Répond du même coup à la paire optionnelle « qui reste longtemps dans la même chambre avant de se séparer ».
- **Paire C** (N=9, chambre {2,4,6}, §4.15/§4.16) : les deux points du premier centre de zoom dont la scission structurelle (2 6) sépare à k=2 (chemins terminant en {1,2,3} contre {1,3,6}), φ₂=341,644° pour les deux, φ₆=358,525° contre 359,034°.

**Anomalie méthodologique trouvée par Benoit, et corrigée : les échantillons finis n'étaient pas eux-mêmes emboîtés.** Première passe : k_min(𝒰₄)=1 et k_min(𝒰₃)=5 pour la paire B — impossible si 𝒰₃⊃𝒰₄ au sens des *familles mathématiques* et que k_min est bien un minimum sur chacune, puisqu'une famille plus grande ne peut jamais séparer plus tard. Diagnostic de Benoit, confirmé à l'inspection du code : la grille numérique 𝒰̂₃ utilisée (amplitude 2,5 fixe, 3 angles) était *disjointe* de la grille 𝒰̂₄ (amplitudes {1,5 ; 2,5 ; 3,5}, 11 angles) au lieu de la contenir — un trou d'échantillonnage, pas une impossibilité réelle. Il faut distinguer la famille mathématique 𝒰_j de l'échantillon fini 𝒰̂_j⊂𝒰_j effectivement testé ; l'emboîtement de la seconde n'est pas automatique du simple fait de l'emboîtement de la première.

**Correction appliquée.** Les échantillons sont maintenant construits pour être emboîtés *par construction*, pas seulement en espérance : 𝒰̂₄(nœud) est la grille de référence (3 amplitudes × 11 angles = 33 protocoles) ; 𝒰̂₅(nœud) en est exactement la tranche angle=0 (donc 𝒰̂₅⊂𝒰̂₄ au sens ensembliste strict) ; 𝒰̂₃(nœuds) est l'union des 𝒰̂₄(nœud) sur la liste de nœuds (donc 𝒰̂₄(0)⊂𝒰̂₃ dès que le nœud 0 y figure). Un contrôle automatique (`check_nesting_and_monotonicity` dans `nerode_matrix_full.py`) vérifie à chaque exécution l'emboîtement ensembliste ET la monotonie k_min(𝒰₃)≤k_min(𝒰₄)≤k_min(𝒰₅) — désormais vérifiée sans exception sur les trois paires (toute violation future serait alors un vrai bug, plus une question d'échantillonnage).

**Résultat de la matrice, corrigé (profondeur minimale séparatrice, K≤7 sauf mention contraire pour 𝒰₅) :**

| Paire | 𝒰₅ (mono-axe, nœud 0, 3 protocoles) | 𝒰₄ (2D cst, nœud 0, 33 protocoles) | 𝒰₃ (2D cst, nœud variable, 198/132 protocoles) |
|---|---|---|---|
| A — miroir, N=6 | **✗ — prouvé : jamais, à aucune profondeur** | ✓ k_min=3 (18/33 séparent) | ✓ k_min=1 (166/198 séparent) |
| B — coin (0,0), N=6 | ✗ — jusqu'à k=12 et 40 amplitudes testées | ✓ k_min=1 (2/33 séparent) | ✓ k_min=1 (3/198 séparent) |
| C — {2,4,6}, N=9 | ✗ — jusqu'à k=12 et 40 amplitudes testées | ✓ k_min=2 (2/33 séparent) | ✓ k_min=2 (2/132 séparent) |

La monotonie est maintenant honnête de part en part : k_min(𝒰₃)≤k_min(𝒰₄) pour les trois paires (B et C : égalité, l'union sur plus de nœuds ne trouve rien de plus rapide que le nœud 0 seul déjà testé dans 𝒰₄ — c'est un fait sur ces témoins précis, pas une propriété générale).

**Garde-fou explicitement honoré (Benoit) : un ✗ n'est jamais, en soi, une preuve de non-séparabilité.** Les trois ✗ ci-dessus n'ont pas le même statut.

1. **Paire A : ✗ prouvé, pas seulement observé — argument renforcé (Benoit) via la réflexion orthogonale R_y.** Quand u_y=0 sur le seul nœud forcé et H(0)=V(0)=0, les équations ne mélangent jamais les composantes x/y d'un nœud à l'autre et le forçage n'a pas de composante y, donc **H_y≡V_y≡0 exactement, sur tous les nœuds, à tout instant** (vérifié à la précision machine : max|H_y|=max|V_y|=0,0). Soit R_y:(x,y)↦(x,−y) la réflexion. Comme H_y≡V_y≡0, le sous-espace fixé par R_y (composantes y nulles) est invariant pour (H,V) ; et comme la paire A est construite comme le miroir exact l'une de l'autre (φ'=−φ), les trajectoires de τ pour x et x' restent reliées par R_y à tout instant. **R_y est une isométrie (orthogonale)**, donc elle préserve le cosinus : cos(R_y a, R_y b) = cos(a,b) pour tous vecteurs a,b. Le classement de similarité cos_sim(τ_i,τ_j) qui pilote chaque saut K* est donc *identique*, terme à terme, pour x et x' à chaque Kairos — pas approximativement, exactement. D'où :

   > **𝒰₅ ne sépare jamais la paire A.** (plus un résultat numérique : une conséquence directe de l'orthogonalité de R_y et de l'invariance du sous-espace H_y=V_y=0 sous forçage mono-axe.)

   Confirmé expérimentalement (balayage dense 40 amplitudes, profondeur poussée à k=12, toujours ✗) mais la preuve ne dépend plus de ce balayage.

2. **Paires B et C : ✗ mécaniquement compris, toujours pas une preuve d'impossibilité — et le vrai mécanisme est plus fort que « l'amplitude importe peu ».** Ni B ni C ne sont des paires miroir. Le fait exact qui explique l'échec de 𝒰₅ ici (et plus généralement, la raison pour laquelle le protocole peut échouer à séparer deux branches encore confondues) est le suivant, formalisé en lemme :

   > **Lemme (Transport de la différence cachée avant séparation).** Dans le régime γ₁=λ=0, sous un protocole commun, et tant que x et x' suivent le même chemin structurel (même A, donc même (H,V,P) à chaque instant puisque (H,V,P) ne lit jamais τ — §3.21/§4.3), la différence Δτ=τ_x−τ_{x'} obéit à Δτ̇=−βΔτ (le terme de forçage α tanh(ÃH), commun aux deux états, s'annule dans la différence), donc
   > **Δτ(t) = e^{−β(t−t₀)} · Δτ(t₀)**
   > exactement entre deux Kairos consécutifs — quel que soit le protocole (nœud forcé, amplitude, direction, tous indifférents à cette loi). Si le saut lui-même ne modifie pas τ, la relation se prolonge tant que les deux branches restent structurellement confondues. Vérifié numériquement (`nerode_mechanism_check.py`) : erreur entre Δτ(t) simulé et Δτ(t₀)e^{−β(t−t₀)} de l'ordre de 10⁻¹⁵, y compris sous des protocoles hors de 𝒰₅.

   **Lecture conceptuelle (Benoit), à retenir comme la bonne façon de penser ce chantier :** *le protocole n'agit pas directement sur l'écart caché avant séparation ; il agit sur la configuration commune (le « fond » (A,H,V,P) partagé par x et x') relativement à laquelle cet écart est lu par K* via les cosinus.* Le contrôle ne fabrique pas la différence entre les traces — il déplace leur position commune dans l'espace, donc la façon dont une même Δτ rencontre les murs de classement. C'est précisément pourquoi la *direction* du forçage peut être cruciale (elle change le fond commun transversalement aux murs/symétries qui rendaient Δτ invisible) alors que l'*amplitude* seule, dans la sous-famille u_y=0, ne change que l'instant où ce fond commun est évalué — pas sa direction relative aux murs.

   Cas particulier u_y=0 (𝒰₅) : la composante y de τ sur chaque nœud décroît en e^{−βt}, découplée du forçage (H_y≡V_y≡0, comme au point 1, mais ici propriété d'un seul état, pas d'une paire miroir). Le profil *relatif* de τ_y entre nœuds (ce qui pilote le classement cos_sim) est donc indépendant de l'amplitude — cela explique l'échec identique à 40 amplitudes et k≤12 pour B et C : l'information discriminante entre B et C, portée par des angles proches de 0° donc presque uniquement par la composante y, est structurellement hors de portée de 𝒰₅ tel que testé. Dès qu'une direction ≠0° est autorisée, la séparation réapparaît (k=7 pour B, k=2 pour C) : exactement la lecture conceptuelle ci-dessus — une nouvelle direction déplace le fond commun, pas l'écart lui-même.

   **Ce qui n'est pas acquis, à la différence de A :** cette explication rend très improbable, mais ne prouve pas, qu'aucune entrée de 𝒰₅ ne puisse séparer B ou C — sauf si 𝒰₅ est précisément la famille uniparamétrique entièrement caractérisée (un seul nœud, direction nulle : ici seul le nœud 0 a été testé systématiquement sous u_y=0). Non exclu : un autre nœud forcé, toujours à u_y=0, romprait le même découplage pour une raison propre à sa géométrie locale. Non testé systématiquement.

**Lecture d'ensemble, affinée.** Le saut mono-axe→2D (même nœud) suffit déjà à séparer tôt (k≤3) dans les trois cas — la richesse décisive semble bien être la *direction* du forçage plutôt que son amplitude ou le nombre de nœuds forcés, et le lemme ci-dessus en donne maintenant la raison mécanique plutôt qu'une simple observation empirique : l'amplitude seule ne peut pas déplacer le fond commun transversalement aux murs de classement, une direction nouvelle le peut.

**Recherche d'un contre-exemple à 𝒰₄ (Benoit) : « 𝒰₄ sépare-t-elle A,B,C par vrai pouvoir séparant, ou seulement par vitesse ? »** Question posée après la matrice corrigée : existe-t-il une paire x≁_N x', témoignée par un protocole de 𝒰₃ (nœud ≠ 0), mais jamais séparée par aucun protocole de 𝒰₄ (nœud 0 seul), à aucune profondeur ? Recherche structurée (pas un scan aveugle) sur le témoin N=6 : trois configurations génériques de τ, perturbation angulaire isolée (δ=0,3° à 3°) sur un seul nœud m∈{1,…,5} à la fois, comparant systématiquement 𝒰̂₄(nœud 0) et la famille symétrique forçant le nœud m, jusqu'à k=12 (script `nerode_u4_counterexample_search.py`).

**Piège trouvé en route, corrigé avant d'aller plus loin : mauvais graphe.** La première version du script retapait à la main les 8 arêtes « habituelles » du témoin N=6, mais sur une permutation de nœuds différente de celle réellement produite par la simulation (Aut mesuré = 2 au lieu de 1 attendu pour cette chambre) — mélange involontaire de deux chambres distinctes. Corrigé en rechargeant le graphe exact depuis `nerode_pairs.pkl` plutôt qu'en le retypant.

**Deux candidats trouvés sur la grille de référence (33 protocoles, k≤12), aucun ne survit au stress-test.** Deux paires ont d'abord semblé être exactement ce que Benoit cherchait (𝒰̂₄ non séparé jusqu'à k=12, le nœud alternatif séparant à k=1 ou k=2). Stress-test appliqué avant de les reporter comme résultat : grille 𝒰₄(nœud 0) densifiée (10 amplitudes × 36 angles = 360 protocoles au lieu de 33) et profondeur poussée à k=20. **Dans les deux cas, la séparation réapparaît via le nœud 0 seul** (k=5 et k=4 respectivement), par un protocole absent de la grille de référence à 33 points (angle ≈110°, hors des 11 angles testés) — et il ne s'agit pas d'un simple déficit de profondeur : la grille de référence à 33 points, repoussée elle-même à k=20, ne sépare toujours pas. C'est bien un trou d'échantillonnage de 𝒰̂₄, pas une limite de la famille mathématique 𝒰₄.

**Leçon méthodologique (symétrique de celle trouvée par Benoit sur l'emboîtement U3/U4), reformulée par Benoit en règle générale :**

> ✓ est un témoin ; ✗ n'est une preuve que s'il vient d'une obstruction analytique.

La paire A sous 𝒰₅ satisfait ce second cas (symétrie R_y, §4.17 plus haut) ; pour B, C et les candidats ci-dessous, même k=20 et plusieurs centaines de protocoles ne donnent qu'une absence de séparation *dans l'échantillon testé*, jamais une preuve. **À noter explicitement comme résultat de méthode récurrent, pas un simple bug de script : toute étude de séparabilité doit distinguer la famille mathématique 𝒰_j de son échantillon numérique 𝒰̂_j, dans les deux sens — un ✓ sur 𝒰̂_j⊂𝒰_j est un vrai témoin, mais un ✗ sur 𝒰̂_j ne dit rien sur 𝒰_j sans un argument analytique séparé (comme pour A) ou un stress-test explicite (densification, profondeur).**

**Sensibilité locale ciblée (Benoit), plutôt qu'un nouveau scan aveugle (script `nerode_sensitivity_jacobian.py`).** Proposition : pour une compétition i↔j au Kairos k (un « mur » de décision g_ij(τ)=cos(τ_{i*},τ_i)−cos(τ_{i*},τ_j)=0), calculer le Jacobien J^{(r)}_{ij,k}=∂g_ij,k/∂(u_{r,x},u_{r,y}) du score par rapport au contrôle à chaque nœud r, et chercher un mur où J^{(0)}≈0 (le nœud 0 n'a localement aucune prise) alors que J^{(r)}≠0 pour un autre nœud — la signature recherchée d'un vrai écart de pouvoir séparant entre 𝒰₄ et 𝒰₃, pas seulement de vitesse.

Implémenté sur le témoin N=6 : à chaque Kairos, extraction du mur pertinent (ici uniquement un mur de *retrait* — le témoin N=6 a toujours |nn(i*)|=m exactement, donc aucun mur d'*ajout*, tous les non-voisins sont systématiquement ajoutés sans ambiguïté), puis différence centrée du score par rapport au contrôle en chaque nœud, avec un contrôle de référence permanent au nœud 0. Sur 5 configurations génériques × k=1..5, le meilleur candidat trouvé : **baseline (5°,95°,185°,275°,350°), k=1, mur de retrait : |J^{(0)}|=0,0018, |J^{(1)}|=0,0179 (rapport ×10)** — le nœud 0 semblait localement presque aveugle à ce mur, le nœud 1 dix fois plus sensible.

**Candidat construit à partir de ce diagnostic, lui aussi stress-testé et lui aussi séparé.** Paire perturbant le nœud 1 de ce baseline (δ=0,3° à 3°), testée directement avec la grille dense (360 protocoles) et k=20 (leçon du tour précédent appliquée dès le départ, pas après coup) : **séparée par 𝒰₄(nœud 0) dès k=1 dans les trois cas**, mais via un protocole *loin* du point de référence (2,0 ; 1,0) où le Jacobien avait été évalué (amplitude 1 à 1,5, angle ≈180-290°, pas dans le voisinage local testé). **La sensibilité locale (linéaire, autour d'un seul point de référence) ne capture donc pas la portée globale et non linéaire de 𝒰₄** : un mur localement plat autour d'un contrôle de référence peut rester tout à fait accessible à grande amplitude ou sous un angle très différent.

**Bilan à ce stade (3 candidats construits — 2 par recherche structurée, 1 par sensibilité ciblée — 3 séparés par 𝒰₄ après stress-test complet) : aucun contre-exemple à « 𝒰₄ sépare A, B, C » n'a survécu.** C'est, dans les propres termes de Benoit, « un résultat intéressant en soi » : sur ce témoin N=6, la richesse directionnelle d'un seul nœud (même sans varier son identité) semble suffire à atteindre, de façon non locale, les murs testés — ce qui suggère que le pouvoir séparant de 𝒰₄ n'est peut-être pas qu'une question de vitesse par rapport à 𝒰₃, du moins sur ce témoin. Leçon tirée par Benoit, à retenir : **faible sensibilité locale ⇏ défaut global de pouvoir séparant** — le Jacobien reste un outil d'interprétation *a posteriori*, pas un filtre de recherche fiable (un mur localement plat autour d'un point de référence peut rester accessible ailleurs dans l'espace, à amplitude ou angle très différents).

**Passage à N=9, chambre {2,4,6} (Benoit) : plus sévère, parce qu'il offre cette fois un vrai mur d'AJOUT (absent de N=6), et deux candidats de perturbation ciblés — l'orbite isolée {6,7,8}, et le mur d'ajout lui-même plutôt que de retrait (script `nerode_n9_u4_vs_u3.py`).**

**Diagnostic direct du mur d'ajout réel (pas une supposition) :** au centre de zoom connu (φ₂,φ₆)=(348°,12°) de la chambre {2,4,6}, le classement réel de cos_sim au moment du premier Kairos (A₀ : nb(0)={1,2,3}, nn(0)={4,5,6,7,8}, m=2) est **6 (0,9997) > 4 (0,9953) > 5 (0,9634) > 8 (−0,861) > 7 (−0,986)**. Les nœuds 6 et 4 sont les deux ajoutés (conforme à l'étiquette {2,4,6} déjà connue) ; le mur actif est entre 4 (rang 2, gardé) et **5** (rang 3, le concurrent immédiat) — pas entre 6 et 7/8 comme l'orbite isolée l'aurait suggéré a priori : 7 et 8 sont bien trop loin (cos_sim ≈ −0,86 à −0,99) pour être compétitifs par une petite perturbation. Vérifié avant de construire quoi que ce soit, conformément à la discipline demandée par Benoit (« suivre les marges de classement pertinentes » plutôt que deviner).

**Fait structurel nouveau, trouvé en creusant pourquoi {6,7,8} était hors-jeu : A₀ est déconnecté en 3 composantes — {0,1,2,3} (étoile), {4,5} (arête), {6,7,8} (isolés).** Ã ne mélange jamais deux composantes différentes (pas d'arête entre elles), donc tant qu'aucun recâblage ne les relie, (H,V) restent **exactement nuls, pour toujours**, sur toute composante ne contenant pas le nœud forcé — et donc τ y décroît en e^{−βt} de façon totalement autonome, à DIRECTION FIXE (seul le module décroît, invisible pour tout cos_sim). Conséquence : pour un nœud dans une composante non forcée, le seul degré de liberté qu'un forçage extérieur (nœud 0) peut actionner est la direction de **τ₀ lui-même**, qui balaie un sous-ensemble atteignable de directions selon le protocole — la séparabilité d'un mur impliquant un nœud externe se réduit donc à la question : *l'ensemble des directions de τ₀ atteignables sous 𝒰₄ croise-t-il, ou non, le secteur angulaire qui discrimine x de x' ?* C'est le bon cadre analytique pour chercher une obstruction (parent direct du mécanisme R_y de la paire A), mais ce n'est pas encore, en soi, une preuve — il faut encore montrer que ce sous-ensemble atteignable est borné et exclut le secteur discriminant.

**Candidat construit sur ce mur réel (nœud 5, δ=0,3° sur φ₅), lui aussi séparé par 𝒰₄ une fois stress-testé.** Non séparé par le protocole de référence unique (nœud 0, amp=2,5, angle=37°) jusqu'à k=8 — mais la grille dense (360 protocoles, k=20) trouve une séparation **à k=2, via 25/360 protocoles** (le plus proche : amp≈1, angle≈−10°). Donc, empiriquement, l'ensemble des directions de τ₀ atteignables sous 𝒰₄ dense *traverse bien* le secteur qui discrimine cette paire — pas d'obstruction ici non plus.

**Bilan cumulé (N=6 + N=9) : 4 candidats construits de façon informée (pas aveugle), 4 séparés par 𝒰₄ après stress-test dense. Toujours aucun contre-exemple.** Couvre maintenant les deux types de mur (retrait et ajout) sur deux témoins distincts. Coût à noter : le stress-test dense sur N=9 est nettement plus cher (≈7 min par famille contre ≈3 min sur N=6, 9 nœuds à intégrer au lieu de 6) — la confirmation symétrique « 𝒰(nœud 5) sépare bien plus vite » n'a pas pu être terminée dans ce tour (interrompue par le budget de calcul), mais n'est plus nécessaire pour établir x≁_N x' : 𝒰₄ lui-même en est maintenant le témoin direct (k=2).

**Statut consolidé pour la suite.** La discipline ✓/✗ de Benoit continue de bien fonctionner : chaque ✗ rencontré ce tour a soit été expliqué analytiquement (paire A), soit s'est révélé n'être qu'une absence observée, corrigée par un stress-test plus dense. Le cadre des composantes connexes de A₀ (nouveau) donne une piste analytique précise pour la prochaine tentative d'obstruction réelle — chercher un cas où le secteur discriminant est si étroit, ou le temps de forçage avant le Kairos pertinent si court, que l'ensemble atteignable de directions de τ₀ ne peut structurellement pas le croiser — plutôt que de continuer à construire des candidats au hasard des marges.

**Reformulation de Benoit, et renversement de méthode : cartographier directement l'ensemble atteignable plutôt que chasser des contre-exemples un par un.** Avant le premier recâblage qui connecte les composantes de A₀, le score externe c_j(t)=cos(τ₀(t),τ_j(0)) perd toute dépendance au facteur de décroissance e^{−βt} (invisible au cosinus), donc toute la capacité de 𝒰₄ à distinguer une paire externe passe par
R₀ = { τ₀(t_K;u)/‖τ₀(t_K;u)‖ : u∈𝒰₄ } ⊂ S¹
(l'ensemble des directions que τ₀ peut effectivement prendre au premier Kairos, sous forçage 2D constant au nœud 0 seul). Le mur discriminant W_pq={v : cos(v,τ_p)=cos(v,τ_q)} partage le cercle en deux ; la question devient : R₀ traverse-t-il les deux côtés de W_pq ? Une obstruction géométrique locale (R₀ ne traverse pas) ne serait d'ailleurs qu'une moitié de preuve — il faudrait ensuite montrer qu'elle est préservée par tous les recâblages accessibles sous 𝒰₄, pas seulement avant le premier contact (point explicitement signalé par Benoit comme le piège à ne pas oublier si une vraie obstruction apparaissait un jour).

**Cartographie numérique de R₀ sur le témoin N=9 (script `nerode_R0_mapping.py`).** Angle de τ₀ au premier Kairos, en fonction de (amplitude, angle) du forçage au nœud 0 : un premier balayage (25 amplitudes × 90 angles = 2250 points, résolution angulaire 4°) laissait apparaître de larges arcs « vides » (jusqu'à 193° de bins à 1° jamais touchés, concentrés en gros entre 70° et 290°). **En densifiant à résolution angulaire 1° (20 amplitudes × 360 angles = 7200 points), tous ces arcs se remplissent** : il ne reste que 35 bins isolés d'1° de large chacun (jamais deux consécutifs), signature classique d'un artefact de grille plutôt que d'un vrai trou — leurs voisins immédiats sont systématiquement atteints.

**Conclusion (numérique, pas encore une preuve, mais nette) : R₀ = S¹.** Un seul nœud forcé en 2D (amplitude et direction libres) semble déjà suffire, sur ce témoin, à faire balayer à τ₀ *toutes* les orientations possibles au premier Kairos — exactement le scénario alternatif anticipé par Benoit, et qui explique d'un coup les 4 échecs précédents à construire un contre-exemple : il n'y a, à ce stade de la fenêtre pré-connexion, **aucun secteur structurellement hors de portée** pour 𝒰₄ sur ce graphe. Benoit reformule proprement le constat : *« 𝒰₄ est numériquement angulairement complète au premier Kairos »* sur ce témoin — un fait numérique solide, pas (encore) un théorème, faute d'argument analytique de contrôlabilité de l'angle de τ₀.

**Benoit déplace alors la question vers l'obstruction séquentielle plutôt que ponctuelle : une famille complète à chaque étape prise isolément peut-elle échouer sur certaines combinaisons successives ?** Formalisation proposée : R₀^{(1,2)} = {(θ₁(u), θ₂(u)) : u∈𝒰₄} ⊂ S¹×S¹ — l'ensemble conjoint des angles de τ₀ aux PREMIER et DEUXIÈME Kairos, sous un même protocole *constant*. Comme u n'a que 2 paramètres réels (amplitude, direction) pour toute la durée, θ₁ et θ₂ ne sont pas des degrés de liberté indépendants : rien ne garantit que leur image conjointe remplisse tout le tore, même si chaque marginale, prise seule, couvre S¹ en entier.

**Cartographie numérique de R₀^{(1,2)} sur le témoin N=9 (script `nerode_R0_sequential.py`) : résultat net, et différent de l'épisode précédent.** 2160 protocoles (24 amplitudes × 90 angles) : chaque marginale couvre quasiment tout S¹ (1/36 et 0/36 cases de 10° vides), **mais le conjoint laisse 1135 cases sur 1296 (10°×10°) jamais visitées — 87,6% du tore inatteint.** Contrairement à l'épisode du balayage ponctuel (où le trou apparent disparaissait en densifiant la grille), **ce trou-ci résiste à la densification** : en plus que doublant l'échantillon (4800 protocoles, 40 amplitudes × 120 angles), le nombre de cases vides reste quasiment identique (1119/1296, soit 86,3%) alors que les deux marginales restent, elles, intégralement couvertes. Ce n'est donc pas un artefact de grille comme au tour précédent : **l'ensemble atteignable conjoint (θ₁,θ₂) occupe une région fine, de forme non triviale, dans le tore — pas le tore entier** (figure `R0_joint_reachable_N9.png` envoyée à Benoit).

**Portée exacte du résultat, à ne pas surinterpréter (discipline ✓/✗ encore).** Ceci établit que 𝒰₄ n'est **pas** conjointement complète sur (θ₁,θ₂) — une vraie structure séquentielle, pas juste de la vitesse ou de l'amplitude. Mais ce n'est **pas encore** un contre-exemple à la séparabilité : il faudrait maintenant exhiber une paire x,x' dont le mur discriminant à k=1 ET le mur discriminant à k=2 (conditionnellement au premier) exigent précisément une combinaison (θ₁*,θ₂*) qui tombe dans la zone jamais atteinte — ce qui n'a pas été tenté. C'est exactement la prochaine étape indiquée par Benoit : construire le candidat à partir de la géométrie d'atteignabilité (ici, conjointe) plutôt que l'inverse, cette fois au niveau séquentiel plutôt que ponctuel.

**Où cela laisse le chantier.** La piste d'obstruction statique au premier Kairos est bien morte sur ce témoin (R₀=S¹) ; mais l'obstruction séquentielle, elle, a une assise numérique solide pour la première fois (un vrai trou, qui résiste à la densification) — sans qu'on ait encore construit le témoin Nerode qui l'exploite.

**Rang/Jacobien de F₂:(r,φ)↦(θ₁,θ₂) (Benoit), avant toute construction (script `nerode_R0_jacobian.py`).** Différence centrée numérique sur 500 points (r,φ), déterminant relatif |det DF₂|/‖DF₂‖²_F (normalisé pour ne pas confondre « petit déterminant » et « Jacobien globalement petit en norme »). Résultat : **médiane |det_rel|=0,027, 79% des points à |det_rel|<0,05 (quasi-rang-1), 12% à <0,01** — mais PAS uniformément nul (max=0,325 sur certaines poches). C'est le second scénario que Benoit envisageait, confirmé : malgré ses 2 paramètres, F₂ produit presque partout une image de dimension effective inférieure à 2 dans le tore séquentiel — ce qui explique directement l'aspect « branches/faisceaux » de la carte plutôt que des trous dispersés.

**Localisation d'un trou robuste, et structure diagonale trouvée en le cherchant.** En croisant les deux jeux de données déjà calculés (2160 + 4800 protocoles) : pour θ₁∈[230°,250°), les 5 points disponibles donnent θ₂∈[214°,226°] — jamais proche de [60°,100°]. Même constat pour θ₁∈[260°,300°) (26 points, θ₂∈[209°,279°]) et θ₁∈[300°,340°) (203 points, θ₂∈[186°,333°]) : **aucune de ces bandes n'atteint θ₂∈[60°,100°]**, malgré une densité croissante. Inversement, θ₂∈[60°,100°) EST atteint (116 points), mais uniquement pour θ₁∈[2°,76°]. Le point le plus proche du centre de Q=[230°,250°]×[60°,100°] dans tout le nuage de points reste à 116,6° de distance angulaire — aucun quasi-rattage. **Lecture structurelle qui émerge : sous forçage faible, θ₂≈θ₁ (τ₀ n'a pas le temps de beaucoup tourner entre les deux Kairos) ; sous forçage fort, θ₂ peut dévier largement, mais apparemment toujours en restant sur une famille de branches qui n'atteint jamais la combinaison « θ₁ dans la bande 220-340° ET θ₂ dans la bande 60-100° » simultanément.** C'est exactement la forme d'obstruction conjointe que Benoit demandait : A₁=[230°,250°] et A₂=[60°,100°] sont CHACUN individuellement atteints (ailleurs), mais Q=A₁×A₂ ne l'est jamais, confirmé par recoupement de plusieurs bandes et deux échantillons indépendants.

**Première tentative de construction du témoin (script `nerode_Q_witness_attempt.py`) : échec net, mais mécanisme identifié précisément — plus informatif qu'un simple ✗.** Construction littérale de la recette à deux étages : nœuds p=7 (φ=250°), q=8 (φ=230°) IDENTIQUES pour x,x' (mur-bissectrice à θ₁=240°, centre de A₁) ; nœud r=4, DIFFÉRENT entre x et x' (φ₄ˣ=5°, φ₄ˣ'=135°), dans la composante {4,5} déconnectée de A₀, censé porter le mur conditionnel à θ₂≈80° (centre de A₂) via le nœud s=5 (φ=355°, identique pour x,x').

Résultat : la paire se **sépare à k=1, pour 115 protocoles sur 144 testés** (grille 6 amplitudes × 24 angles, K=4) — y compris pour la quasi-totalité des angles à amplitude fixée 2,5 (36/36 angles séparent à k=1). Ce n'est donc pas une séparation confinée à une région de θ₁ liée à Q : **le mur se déclenche dès le premier Kairos, pour n'importe quelle direction de forçage dès que l'amplitude est modérée**, ce qui disqualifie entièrement la construction — la séparation n'a rien à voir avec Q, elle précède même l'existence d'un θ₂.

**Mécanisme identifié (pas juste « mauvais réglage »).** Au premier Kairos, i*=0 de façon déterministe (seul nœud à P non nul à t=0) ; or nb(0)∪nn(0) = *tous les autres nœuds* — chaque nœud, sans exception, est donc déjà candidat (à l'ajout s'il est non-voisin, au retrait s'il est voisin) dès ce premier événement, via cos_sim(τ₀,·). Un nœud auxiliaire dont l'angle diffère entre x et x' est donc **exposé dès k=1**, pas seulement dans une fenêtre « à partir du k-ième Kairos dans la bonne chambre ». De plus τ₀ démarre à l'angle 0 et ne s'en écarte que lentement (son équation ne dépend du contrôle qu'indirectement, via tanh(ÃH), lui-même retardé) : à amplitude modérée, θ₁ reste proche de 0 quel que soit l'angle du contrôle, ce qui fait gagner par défaut un nœud auxiliaire placé près de 0 (ici φ₄ˣ=5°) — sans même que le contrôleur ait besoin de « viser » la résonance.

**Portée générale de ce constat (à vérifier plus avant, mais cohérent avec tout le reste du chantier) : une différence brute d'angle sur un nœud auxiliaire « libre » ne peut pas être cachée derrière Q, parce que son canal d'exposition (cos_sim au premier Kairos, i*=0) est partagé avec le mur p/q censé fournir la porte θ₁, et ce canal est actif dès k=1 — avant même qu'un θ₂ existe.** Ceci éclaire a posteriori pourquoi la Paire A (seul cas prouvé non-séparable par 𝒰₅) protège sa différence par une symétrie EXACTE (R_y) valable pour *tout* protocole, et non par un simple évitement de zone : en dehors de ce genre de symétrie exacte, une différence d'angle portée par un nœud auxiliaire semble condamnée à fuiter dès le premier Kairos, pour peu que l'amplitude soit suffisante — exactement le mécanisme qui a fait s'effondrer les 4 tentatives de contre-exemple précédentes, retrouvé ici sous une forme encore plus directe (k=1, pas même besoin de viser un angle particulier).

**Conséquence pour la suite : abandonner la recette « p,q identiques + r,s qui diffèrent en angle », revenir à des différences structurelles de graphe (à la manière des Paires B/C), situées à distance du nœud forcé plutôt que portées par un nœud librement choisi.** Une piste directe et déjà disponible : reprendre le candidat N=9 (perturbation φ₅) de `nerode_n9_u4_vs_u3.py` — non séparé par le protocole de référence, mais séparé par 𝒰₄ dense à k=2 — et regarder, cette fois, la corrélation entre ses événements de séparation et (θ₁,θ₂), plutôt que d'inventer une paire ex nihilo à partir des portes p,q,r,s. Si cette paire-là (ou une variante) s'avère non séparée par 𝒰₄ en restant confinée hors de Q, on aura le témoin — construit à partir d'une architecture qui a déjà fait ses preuves plutôt que d'un mécanisme qui vient de montrer sa fragilité.


**Prochaines étapes (non commencées) :** extraire proprement le Lemme de transport (et le cas particulier R_y pour les paires miroir) vers le corps du .tex, comme pièce du programme des familles séparantes plutôt que comme simple note de chantier numérique ; implémenter 𝒰₂/𝒰₁ (forçage variable dans le temps) si ce palier est jugé concluant ; élargir l'échantillon de paires au-delà de ces trois cas pilotes ; tester systématiquement un nœud forcé différent sous 𝒰₅ pour B/C.

## 5. Questions ouvertes consolidées

Liste refondue : les renvois pointaient auparavant sur la numérotation interne du .tex v4, aujourd'hui sans objet (le texte en est à la V5.5 ; voir aussi la note en tête de document sur les sections 1 à 3, non remises à jour). Ce qui suit distingue ce qui reste vraiment ouvert de ce qui est réglé depuis, pour ne plus rouvrir ce qui ne l'est plus. Point non vérifié dans cette repasse : les entrées 3 et 4 ci-dessous (C5, G₂) datent de la relecture V5.3.2 et n'ont pas été recroisées avec le contenu ajouté depuis (notamment les deux nouvelles propositions incorporées en V5.5, §4.3) — à faire dans la repasse de consolidation de 1 à 3.

**Item 12 — Programme : des partitions finies 𝒫_k vers l'équivalence de Nerode ∼_N (Benoit, prolongement direct de V5.7 ; crash-testé)**

Objectif : formaliser comment 𝒫_k approxime la partition comportementale complète F_y/∼_N, où pour x,x'∈F_y=ρ_X⁻¹(y)∩C,
x∼_N x' ⟺ 𝔐_x^adm=𝔐_{x'}^adm et R_x^{ρ_int}=R_{x'}^{ρ_int}.

Définition de travail : pour un protocole u et une profondeur k, x≡_k^{(u)}x' lorsque x et x', partant d'une même fibre d'opacité, produisent le même chemin structurel au cours de leurs k premiers Kairos sous u.

1. *Raffinement avec la profondeur.* x≡_{k+1}^{(u)}x' ⟹ x≡_k^{(u)}x' (trivialité de préfixe) ; 𝒫_{k+1}^{(u)} raffine 𝒫_k^{(u)}. **Déjà vérifié**, et pas seulement en théorie : c'est exactement ce que les `idx` de groupes encodent dans tout le code de simulation depuis le début (chaque enfant ⊆ son parent).

2. *Inclusion de Nerode vers les partitions finies.* x∼_N x' ⟹ x≡_k^{(u)}x' pour tout protocole admissible u et toute profondeur finie k. Donc, pour toute famille 𝒰, ∼_N ⊆ ⋂_{u∈𝒰}⋂_{k<∞}≡_k^{(u)}. **Acquis.**

3. *Question centrale : l'inclusion inverse.* Une famille 𝒰 est dite *séparante* si x≁_N x' implique l'existence de u∈𝒰 et k<∞ tels que x≢_k^{(u)}x'.

4. *Simplification propre au régime γ₁=λ=0.* ρ_int=(H,V,P) : τ n'est pas lue directement, et n'agit pas sur le flot continu. Pour un protocole et un readout initial fixés : même chemin structurel ⟹ même trajectoire ρ_int (c'est exactement le Lemme « Constance du readout sur une chambre », V5.7 §11). Une différence cachée de τ qui ne modifie jamais aucune issue structurelle reste donc dans la même classe de Nerode relativement à ce readout — ce n'est pas un contre-exemple à l'inclusion inverse dans ce régime (un premier candidat de contre-exemple basé sur une dérive continue de τ a été proposé puis réfuté précisément pour cette raison : ρ_int ne voit pas τ).

5. *Limite de portée.* Argument spécifique à γ₁=λ=0. Dès que τ agit sur le flot, deux états de même chemin structurel peuvent avoir des trajectoires ρ_int différentes ; les partitions structurelles seules deviendraient alors trop grossières, même à profondeur arbitraire.

**Correction d'hypothèse sur la clause d'admissibilité (Benoit) : pas π_s seul, mais ρ_X tout entier.** Le garde D du Kairos dépend de P, pas seulement de A : la bonne hypothèse n'est donc pas « 𝔐_x^adm ne dépend que de π_s(x) » (trop forte, et pas nécessaire) mais
ρ_X(x)=ρ_X(x') ⟹ 𝔐_x^adm=𝔐_{x'}^adm,
c'est-à-dire l'admissibilité constante sur les fibres d'opacité F_y elles-mêmes — exactement ce dont a besoin l'argument ci-dessous, ni plus ni moins. Dans ce régime, c'est bien le contenu caché τ qui ne doit pas modifier le domaine admissible.

**Théorème (Complétude de la profondeur finie pour la famille complète) — crash-testé, aucun trou trouvé.** Fixons y et x,x'∈F_y, dans le régime γ₁=λ=0, sous l'hypothèse que l'admissibilité est constante sur F_y. Alors
x∼_N x' ⟺ ∀𝓗∈𝔐_x^adm, ∀k<∞, x≡_k^{(𝓗)}x'.

Sens direct : immédiat (mêmes réponses complètes ⟹ mêmes chemins structurels à toute profondeur). Sens réciproque : fixons 𝓗 et un horizon T. Par non-Zénon, seulement n(T)<∞ Kairos avant T ; l'accord à toute profondeur donne en particulier l'accord des deux chemins jusqu'à n(T) ; le lemme V5.7 donne alors, récursivement sur chaque chambre, (A,H,V,P) identique après chaque Kairos ; entre deux Kairos, même flot déterministe depuis le même readout sous la même entrée, donc ρ_int∘γ_{x,𝓗}=ρ_int∘γ_{x',𝓗} sur [0,T] ; T arbitraire ⟹ égalité de la trajectoire ρ_int entière sous 𝓗 ; ceci pour toute histoire admissible, plus l'égalité des domaines (hypothèse) ⟹ x∼_N x'. Donc **𝒰=𝔐 est séparante dans ce régime** — pas trivialement au sens général, mais précisément parce que l'indépendance de (H,V,P) vis-à-vis de τ, le déterminisme du flot et le non-Zénon le permettent. Dès que τ revient dans F, la preuve casse (point 5).

Crash-test de l'hypothèse elle-même : elle est pour l'instant *supposée*, pas encore vérifiée contre la définition formelle de 𝔐_x du socle (Tome I). Très probablement vraie si le garde D ne dépend que de (A,H,V,P)=y et jamais de τ, mais à confirmer explicitement sur la définition exacte de Madm avant de considérer le théorème comme inconditionnel — sinon elle devra être ajoutée comme axiome supplémentaire du socle. **Non tranché.**

**Dette technique (Benoit), réglée par construction.** Pour une branche qui n'atteint jamais son k-ième Kairos : la longueur finie du chemin fait partie de l'observation. Un chemin qui s'arrête après r<k Kairos n'est égal à un autre préfixe que si celui-ci s'arrête lui aussi au même endroit avec le même mot structurel — formalisable par un symbole terminal †, ou simplement par convention explicite dans la définition de ≡_k^{(u)}.

**Reformulation du programme (acquis) : la question n'est plus l'existence d'une famille séparante (𝔐 en est une), mais sa minimalité.** Chaîne à étudier :
𝔐 ⊃ 𝒰₁ ⊃ 𝒰₂ ⊃ ⋯
avec des familles de plus en plus simples — forçages constants, mono-nœud, 2D génériques, amplitudes bornées, familles paramétriques finies — en demandant à chaque niveau si la séparation est conservée. C'est exactement ce que testent déjà les simulations N=6/N=9 (un forçage 2D générique sur un seul nœud est une famille infime comparée à 𝔐 tout entier, et sépare déjà beaucoup) ; combien de protocoles faut-il réellement pour obtenir la même séparation est désormais la question précise à instrumenter.

**Résumé du résultat acquis :** profondeur finie complète + tous les protocoles = équivalence de Nerode, dans le noyau découplé (γ₁=λ=0, admissibilité constante sur F_y).

**Statut.** C5 reste volontairement non rouvert : ce chantier doit d'abord dire ce que C5 devrait mesurer (pas « il existe de la mémoire », mais comment la structure modifie la persistance des distinctions historiques cachées). Caractérisation numérique de familles 𝒰 petites et séparantes sur les témoins N=6/N=9 : **commencée, voir §4.17** (chaîne 𝒰₅⊃𝒰₄⊃𝒰₃, trois paires de référence, un fait mécanique général nouveau sur la décroissance de Δτ entre Kairos).

**Socle et sémantique du noyau (Tome I — hors périmètre strict du candidat de classe)**
1. Kairos au contact plutôt qu'à la sortie : ce choix doit-il être assumé explicitement dans le Tome I, avec la discontinuité aux contacts tangents qu'il entraîne ?
2. Les hypothèses de la proposition d'invariance suffisent-elles en général, ou le noyau est-il un cas favorable (C fermé, garde scalaire) ?

**Candidat de classe (état à la relecture V5.3.2, non recroisé depuis — voir remarque ci-dessus) — ce qui reste réellement ouvert**
3. **C5** (fermeture de la boucle historique) : la piste actuelle passe par le préordre de simulation ⪯ sur F_y plutôt que l'égalité stricte ∼_N (§4.1) ; les quantificateurs exacts ne sont pas encore stabilisés.
4. **G₂** (temps intrinsèque) : différé tant qu'aucun témoin ne l'exige — inchangé depuis la V5.3.2.
5. Structure du monoïde 𝔐 : libre sur les épisodes, ou quotienté par des relations temporelles (fusion des délais) ? Question indépendante du candidat C23, toujours ouverte.
6. Unification catégorique (inclusions, écritures/lectures, quotients comme une même structure) : la charpente existe (𝔥_G, 𝔥_G^obs, flèches structurelles/événementielles), mais aucun énoncé ne dit encore qu'il s'agit d'une seule structure catégorique au sens fort.
7. Distinguer une réduction suffisante sous protocole d'un quotient de Nerode complet : ce n'est plus une question isolée, c'est l'objet même du chantier §4 (∼_N, préordre ⪯, stratification par Aut(A), lemme combinatoire de sélection équivariante).
8. À quel moment la stratification, l'o-minimalité ou le temps propre deviennent-ils nécessaires : en cours de test au §4 (crash-tests d'équivariance sur le témoin N=6), pas encore tranché — mais la question a maintenant un terrain concret plutôt que rhétorique.
9. S_𝒜 et Ω_{𝒫,ρ} (Annexe H, construction écrire/lire) comme deux types de flèches composables catégoriquement : en réserve, non repris depuis que le candidat passe par ρ_X = (π_s, ρ_int) — à réexaminer seulement si un défaut précis le demande.
10. Repasse de consolidation des sections 1 à 3 (état gelé à la relecture v4) contre la V5.5 : identifier point par point ce qui est résolu/incorporé (comme 3.13, déjà signalé en §4.3), ce qui est devenu sans objet, et ce qui reste réellement ouvert — demandée par Benoit, pas encore faite.
11. **Renforcement théorique, formulé par Benoit, statut : prêt à rédiger dans le .tex (crash-testé ci-dessous).**

    **Proposition candidate (Finitude à profondeur finie).** Supposons que, pour chaque chambre obtenue jusqu'à profondeur k, le prochain Kairos soit déterminé par un indice i* unique sur cette chambre. Alors pour tout k<∞, 𝒫_k comporte un nombre fini de chambres.

    **Démonstration (Benoit).** 𝒫_1 finie par la Proposition 11.1. Supposons 𝒫_k finie. Dans chaque chambre C∈𝒫_k, le graphe courant et i* sont fixés ; le prochain K* compare un ensemble fini de scores sur des ensembles finis de voisins/non-voisins candidats, donc ne peut produire qu'un nombre fini d'issues dans C. Union finie de raffinements finis : |𝒫_{k+1}|<∞. ∎

    **Non-implication à énoncer juste après, dans l'encadré (Benoit) :** |𝒫_k|<∞ ∀k ⇏ sup_k|𝒫_k|<∞ — le site N=6 étudié (§4.13) en est précisément l'exemple : sous persistance de la dominance de τ₁, |𝒫_{2r}^{loc}|=3^r, croissance exponentielle en parfaite compatibilité avec la finitude à toute profondeur finie. La bonne paire d'énoncés est donc *finitude à chaque profondeur* + *croissance éventuellement exponentielle avec la profondeur*.

    **Crash-test de la démonstration (fait ici) : un point est correct mais mérite d'être rendu explicite avant rédaction finale.** L'étape « le graphe courant ... est fixé » ne suffit pas à elle seule à invoquer la Proposition 11.1 : celle-ci fixe *y=(A,H,V,P) tout entier*, pas seulement A, et suppose i* constant sur la région de F_y ainsi fixée. Pour que l'induction soit rigoureuse, il faut donc que (H,V,P) soient eux aussi identiques — pas seulement le graphe — en tout point d'une même chambre C. C'est vrai ici, mais ce n'est pas automatique : ça découle spécifiquement du fait, déjà établi (Tome I, régime γ₁=λ=0), que (H,V,P) n'est influencé par τ à aucun moment — ni dans le flot (τ absent des équations de Ḣ,V̇,Ṗ), ni au saut (le recâblage de K* ne modifie que des arêtes et remet à l'échelle P,V par des constantes rP,rV indépendantes de τ). Deux points d'une même chambre partagent donc, par récurrence immédiate sur cette invariance, exactement le même y=(A,H,V,P) à chaque profondeur — pas seulement le même graphe — et c'est cela, plus que la seule identité du graphe, qui permet de réappliquer 11.1 tel quel. **Correction à apporter avant rédaction :** remplacer « le graphe courant ... est fixé » par « y=(A,H,V,P) est fixé sur C (pas seulement le graphe), par récurrence sur l'indépendance de (H,V,P) vis-à-vis de τ déjà établie dans ce régime » — une ligne, mais qui rend explicite la seule raison pour laquelle l'argument se limite, tel quel, au régime γ₁=λ=0 : dans un régime où τ influence (H,V,P) (γ₁≠0 ou λ≠0), deux points d'une même chambre pourraient avoir des (H,V,P) différents et l'induction ne se refermerait pas aussi simplement.

    **Reformulation empirique (Benoit), à substituer au texte actuel du §4.13/du .tex :** *« La stabilisation apparente observée à résolution grossière est un artefact de sous-résolution. Dans la région localement raffinée, le nombre de chemins croît rapidement avec la profondeur, mais selon une organisation récursive explicite. La complexité observée n'est donc pas bornée ; elle est structurée. »* Et pour le motif N=6 spécifiquement : *« Dans la région étudiée, la réinjection combinatoire entraîne, conditionnellement à la persistance de la dominance de τ₁, une arborescence ternaire aux profondeurs paires. Les observations 3, 9, 26 sont compatibles avec les valeurs idéales 3, 9, 27, la dernière différence étant liée à la résolution numérique utilisée. »* — le conditionnel est délibéré et à garder tant que la dominance de τ₁ n'est pas démontrée uniformément sur toute la descendance, seulement vérifiée numériquement branche par branche.

    **Question de fond reformulée (Benoit) :** non pas « la complexité reste-t-elle petite ? » mais « sa croissance reste-t-elle descriptible par une structure contrôlée ? ».

    **Prochaine étape convenue :** rédiger ce corollaire (avec la correction ci-dessus) dans le .tex d'abord, car quasi gratuit ; puis seulement ensuite reprendre le chantier numérique sur le témoin N=9 (|Aut(A₀)|=72, |Aut(A₁)|=240) pour tester la résistance du triptyque structurel/protocolaire/transverse, de la croissance de 𝒫_k, et de l'existence de mécanismes de réinjection — sans préjuger que N=9 donnera la même arité ou la même récursion que N=6 ; un résultat différent serait tout aussi instructif.

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

**Corrections éditoriales encore à vérifier dans le Tome I (relevées à l'époque v4, à recroiser avec la V5.5)**
- 𝒢_N → 𝔊_N (notation du graphe dans l'espace des états).
- Harmonisation de la règle de saut (r_P Θ) entre le Tome I et l'Annexe A — à confirmer si déjà reportée.

## 6. Piste Lean (mise à jour, V5.3.2 — noyau de la formalisation inchangé depuis ; les deux propositions incorporées en V5.5, §4.3, ne sont pas encore portées ici et sont les cibles naturelles suivantes, comme `NerodeEquiv` déjà signalé plus bas)

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
