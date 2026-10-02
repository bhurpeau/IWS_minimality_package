# -*- coding: utf-8 -*-
path = "/mnt/user-data/outputs/IWS_classe_axiomes_reflexions.md"
with open(path, encoding="utf-8") as f:
    text = f.read()

def do(old, new, expect, label):
    n = text.count(old)
    if n != expect:
        raise SystemExit(f"ECHEC [{label}] : attendu {expect} occurrence(s) de {old!r}, trouvé {n}")
    return text.replace(old, new)

# --- 1. Références §-inline, dans l'ordre qui évite les collisions en cascade ---
text = do("(§3.3)", "(§3.4)", 2, "ref-3.3->3.4")
text = do("(§3.2)", "(§3.3)", 2, "ref-3.2->3.3")
text = do("§3.1 bis", "§3.2", 3, "ref-3.1bis->3.2")
text = do("§3.1 ter", "§3.8", 2, "ref-3.1ter->3.8")
text = do("§3.1 quater", "§3.9", 1, "ref-3.1quater->3.9")
text = do("§3.1 quinquies", "§3.10", 1, "ref-3.1quinquies->3.10")
text = do("§3.6)", "§3.7)", 1, "ref-3.6->3.7")

# --- 2. Titres de sous-sections (### ...), full-line, dans l'ordre du fichier ---
headings = [
    ("### 3.1 I1 dépend de la présentation — l'indépendance I2 ⇏ I1 en dépend aussi",
     "### 3.1 — I1 dépend de la présentation — l'indépendance I2 ⇏ I1 en dépend aussi"),
    ("### 3.1 bis — I1_ρ n'est pas encore l'historicité",
     "### 3.2 — I1_ρ n'est pas encore l'historicité"),
    ("### 3.2 Condition de contenu du quotient — *adopté*",
     "### 3.3 — Condition de contenu du quotient — *adopté*"),
    ("### 3.3 Reach en G₀ et en G₁ — *adopté*",
     "### 3.4 — Reach en G₀ et en G₁ — *adopté*"),
    ("### 3.4 Entrées et histoires dans ∂_exit",
     "### 3.5 — Entrées et histoires dans ∂_exit"),
    ("### 3.5 Notation 𝒢_N",
     "### 3.6 — Notation 𝒢_N"),
    ("### 3.6 Définition du morphisme au §4 du .tex",
     "### 3.7 — Définition du morphisme au §4 du .tex"),
    ("### 3.1 ter — Terminologie figée, et trois crash-tests du noyau",
     "### 3.8 — Terminologie figée, et trois crash-tests du noyau"),
    ("### 3.1 quater — Grille des mécanismes, S_Δ, stabilité par isomorphisme",
     "### 3.9 — Grille des mécanismes, S_Δ, stabilité par isomorphisme"),
    ("### 3.1 quinquies — ψ justifié, convention sur s, transport des mécanismes",
     "### 3.10 — ψ justifié, convention sur s, transport des mécanismes"),
    ("### 3.2 bis — Avis sur les trois nœuds ouverts de la V5 (propositions à valider)",
     "### 3.11 — Avis sur les trois nœuds ouverts de la V5 (propositions à valider)"),
    ("### 3.2 ter — H constitutif : acquis, et cinq crash-tests avant de figer",
     "### 3.12 — H constitutif : acquis, et cinq crash-tests avant de figer"),
    ("### 3.2 quater — Candidat structurel et nouveaux crash-tests",
     "### 3.13 — Candidat structurel et nouveaux crash-tests"),
    ("### 3.2 quinquies — H^{s,ord}, typage de la structure, piste pour C5",
     "### 3.14 — H^{s,ord}, typage de la structure, piste pour C5"),
    ("### 3.2 sexies — Déclaration structurelle, tour de projections, C3 et C5 sans identification des fibres",
     "### 3.15 — Déclaration structurelle, tour de projections, C3 et C5 sans identification des fibres"),
    ("### 3.3 — Relecture de la V5 (.tex)",
     "### 3.16 — Relecture de la V5 (.tex)"),
    ("### 3.4 — Relecture de la V5.1",
     "### 3.17 — Relecture de la V5.1"),
    ("### 3.5 — Après la relecture V5.1 : décisions et précisions",
     "### 3.18 — Après la relecture V5.1 : décisions et précisions"),
    ("### 3.6 — Relecture de la V5.2",
     "### 3.19 — Relecture de la V5.2"),
    ("### 3.7 — Relecture de la V5.2.1",
     "### 3.20 — Relecture de la V5.2.1"),
    ("### 3.8 — Atteignabilité du témoin (noyau, γ₁ = λ = 0, ζ > 0) : construction par symétrie",
     "### 3.21 — Atteignabilité du témoin (noyau, γ₁ = λ = 0, ζ > 0) : construction par symétrie"),
    ("### 3.9 — Témoin numérique N = 6 [NUM] (script `temoin_C23_noyau.py`)",
     "### 3.22 — Témoin numérique N = 6 [NUM] (script `temoin_C23_noyau.py`)"),
    ("### 3.10 — Identifiabilité universelle de la structure ; borne sur u",
     "### 3.23 — Identifiabilité universelle de la structure ; borne sur u"),
    ("### 3.11 — Relecture de la V5.3",
     "### 3.24 — Relecture de la V5.3"),
    ("### 3.12 — Relecture de la V5.3.2",
     "### 3.25 — Relecture de la V5.3.2"),
]
for old, new in headings:
    text = do(old, new, 1, f"heading:{old[:40]}")

# --- 3. Titres de section (## ...) ---
top = [
    ("## 4 ter. Nouveau chantier — quotient de Nerode sur les fibres d'opacité",
     "## 4. Nouveau chantier — quotient de Nerode sur les fibres d'opacité"),
    ("## 4. Questions ouvertes consolidées",
     "## 5. Questions ouvertes consolidées"),
    ("## 4 bis. Plan de consolidation pour la V5",
     "## 6. Plan de consolidation pour la V5"),
    ("## 5. Piste Lean (mise à jour)",
     "## 7. Piste Lean (mise à jour)"),
]
for old, new in top:
    text = do(old, new, 1, f"top:{old}")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)
print("OK, renumérotation appliquée.")
