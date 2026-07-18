# 📊 Présentation — Le Clos Grand × LocalBooster

Système de présentation préparé pour le rendez-vous commercial **Le Clos Grand — Pradine** (06/07/2026).

## ▶️ Ouvrir la présentation

- **[presentation.html](presentation.html)** — Deck interactif 6 slides, design **Aurora v2**.
  Navigation clavier (← →), plein écran (F), export PDF (P), barre de progression et pastilles.
- **[index.html](index.html)** — Point d'entrée (redirige vers le deck) — sert de racine GitHub Pages.
- **[viewer.html](viewer.html)** — Vue PDF de secours (embed du PDF dans le navigateur).
- **[presentation.pdf](presentation.pdf)** — Export PDF 16:9, régénéré depuis le deck HTML.

## 🔗 Liens directs

- Deck en ligne : https://diex1.github.io/rdv-clos-grand/
- PDF brut : https://raw.githubusercontent.com/diex1/rdv-clos-grand/main/presentation.pdf

> ℹ️ Les liens en ligne nécessitent l'activation de **GitHub Pages**
> (Settings → Pages → Branch `main` / `/root`).

## 📋 Contenu des slides

1. **Couverture** — Préparation RDV, Le Clos Grand — Pradine
2. **Contexte** — restauration traditionnelle France (marché, digitalisation, attentes clients)
3. **Métriques clés** — CA 340 200 €, EBITDA 34 020 €, 12 600 couverts/an, 60 % d'occupation
4. **Solution** — LocalBooster en 3 piliers (site rapide, réservation 24/7, visibilité Google)
5. **ROI 12 mois** — +13 817 %, CA additionnel 137 781 €/an, payback 4 mois
6. **Appel à l'action** — audit gratuit 30 min, site en 7 jours, automatisations sur mesure

## 🛠️ Régénérer le PDF

Le PDF est un export du deck HTML (styles `@media print`, une slide par page 1280×720) :

```bash
# via un navigateur headless (Chromium/Playwright)
# ouvrir presentation.html puis imprimer en PDF, format 1280x720px, sans marges
```

Ou directement depuis le deck : touche **P** (ou bouton **⎙ PDF**), format 1280×720, marges nulles.

---

*Généré par le pipeline `rdv_prep` de LocalBooster Swarm — système de présentation restauré.*
