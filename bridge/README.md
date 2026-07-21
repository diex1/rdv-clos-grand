# 🌉 Pont GitHub — Claude Code (machine) ↔ Session planifiée (cloud)

> Canal de communication **de secours** au pont Google Drive `ClaudeCode-Bridge`.
> Ici, tout passe par le dépôt Git au lieu d'un dossier Drive. Avantage : la tâche
> planifiée dans le cloud accède au dépôt **sans avoir besoin d'approuver un
> connecteur** — donc elle fonctionne en exécution non surveillée.

## 1. Principe

- **Claude Code (ta machine)** = dépose les tâches dans `bridge/taches/`, commit + push.
- **Session planifiée (cloud)** = toutes les heures : lit les nouvelles tâches, les
  exécute, écrit les résultats dans le dépôt, puis notifie.
- Communication = ce dépôt Git (`diex1/rdv-clos-grand`), dossier `bridge/`.

## 2. Comment déposer une tâche

Un fichier **par tâche**, dans `bridge/taches/`, nommé `tache-<ID>.md`
(ex. `tache-002.md`, `tache-003.md`…). Puis `git add`, `git commit`, `git push`.

Format :

```
# Tâche <ID>
## Objectif
<une phrase>
## Instructions détaillées
<étapes précises — la session cloud n'a pas ton contexte local>
## Résultat attendu
<fichier, résumé, envoi…>
## Livraison
<où atterrit le résultat>
```

⚠️ La session cloud n'a **pas** accès à ta machine. Aucun chemin local. Tout ce dont
la tâche a besoin doit être décrit dans le fichier ou déposé dans `bridge/`.

## 3. Ce que fait la session cloud (auto, chaque heure)

1. Liste les fichiers `bridge/taches/tache-*.md`.
2. Ignore ceux ayant déjà un `bridge/taches/tache-<ID>.resultat.md` (1 seule exécution).
3. Exécute chaque nouvelle tâche.
4. Écrit `bridge/taches/tache-<ID>.resultat.md` (statut FAIT/ERREUR + ce qui a été produit).
   Les livrables (xlsx, docx, pdf…) sont déposés dans `bridge/livrables/`.
5. Commit + push, puis notifie l'utilisateur.

## 4. Règles

- Un fichier = une tâche. ID unique, jamais réutilisé.
- Instructions autonomes et explicites (pas de contexte local supposé).
- Déclenchement **horaire** : une tâche est prise au prochain top horaire, pas
  immédiatement.
- Ne jamais retraiter une tâche déjà pourvue d'un fichier `.resultat.md`.

## 5. Activation

Ce pont est **prêt mais en veille**. Pour l'activer :

1. Fusionner cette branche dans `main` (les fichiers `bridge/` doivent être sur la
   branche que lit la tâche planifiée — `main` par défaut).
2. Activer la tâche planifiée « Exécuteur de tâches (pont GitHub) » (elle est créée
   mais désactivée pour ne pas consommer de ressources tant qu'on ne s'en sert pas).
3. Côté machine, déposer les tâches dans `bridge/taches/` au lieu du dossier Drive.

Tant que le pont Drive fonctionne, celui-ci reste un simple filet de sécurité.
