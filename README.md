# Chantier minimalité / familles séparantes — IWS Volume II

Organisation des scripts numériques et du compte-rendu courant, rangés par étape du chantier (du plus ancien au plus récent).

## notes/
- `IWS_classe_axiomes_reflexions.md` — le compte-rendu courant complet (toutes les étapes, §4.17 pour le chantier de minimalité en cours).

## scripts/

- **core/** — noyau IWS (dynamiques H,V,τ,P, règle de Kairos K*, générateur de graphes).
  `iws_kairos_core.py`, `iws_kairos_core_gen.py`

- **utils/** — utilitaires transverses (renumérotation, vérifications de périodicité/équivariance, injection).
  `renumber.py`, `rewrite_tail.py`, `check_period.py`, `ucrit.py`, `equivariance_check.py`, `reinjection.py`, `sweep.py`

- **axiomes_crash_tests/** — crash-tests d'axiomes du noyau (hors chantier minimalité), ex. C23^act.
  `temoin_C23_noyau.py`

- **partitions_Fy/** — cartographie de la partition F_y (N=6), profondeurs successives, avec/sans forçage 2D.
  `partition_Fy*.py`, `plot_depth2*.py`

- **genealogie_n9/** — généalogie des branches, zooms adaptatifs, recherche de centres, sur le témoin N=9 (chambre {2,4,6}).
  `depth_growth*.py`, `adaptive_refine*.py`, `n9_*.py`, `orbit_*.py`, `zoom_deep_genealogy.py`, `plot_*.py`, `make_fig_*.py`, `nerode_scan.py`, `nerode_find_late_pair.py`

- **minimalite_U5_U4_U3/** — le chantier de minimalité proprement dit : familles emboîtées 𝒰₅⊂𝒰₄⊂𝒰₃, matrice ✓/✗, preuve Paire A (symétrie R_y), Lemme de transport, recherches de contre-exemples (N=6, N=9), Jacobien de sensibilité.
  `nerode_separating_families.py` (harnais), `nerode_matrix_full.py`, `nerode_run_matrix.py`, `nerode_u5_diagnose.py`, `nerode_mechanism_check.py`, `nerode_u4_counterexample_search.py`, `nerode_sensitivity_jacobian.py`, `nerode_n9_u4_vs_u3.py`

- **R0_reachability/** — cartographie de l'ensemble atteignable R₀ (angle de τ₀ au premier Kairos) puis de l'obstruction séquentielle R₀^(1,2) (joint sur deux Kairos), et son Jacobien/rang.
  `nerode_R0_mapping.py`, `nerode_R0_sequential.py`, `nerode_R0_jacobian.py`

- **construction_temoin_Q/** — tentatives de construction d'un témoin Nerode exploitant le trou Q de R₀^(1,2) : première tentative (p,q,r,s ex nihilo, échec instructif — fuite à k=1), puis reprise sur la paire validée (perturbation φ₇, N=9) avec corrélation (θ₁,θ₂) / chambre A₁ et séparation.
  `nerode_Q_witness_attempt.py`, `nerode_phi7_grid_cache.py`, `nerode_phi7_test_delta.py`, `nerode_phi7_chamber_cond.py`, `nerode_phi7_R0_correlation.py`

Les scripts dans `R0_reachability/` et `construction_temoin_Q/` importent `nerode_separating_families.py` et `nerode_R0_sequential.py` via un chemin absolu codé en dur (chemin du bac à sable de la session) — à ajuster si relancés depuis cet emplacement.
