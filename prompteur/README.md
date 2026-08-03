# 🎬 Prompteur vidéo LocalBooster (VPS)

Une seule page web à ouvrir sur le téléphone : le **téléprompteur défile par-dessus
la caméra pendant que tu filmes**, et à la fin la vidéo est **envoyée directement
sur le VPS**, qui peut lancer le traitement automatiquement. Plus besoin d'une
application mobile à côté.

## Ce que fait l'appli

- **Prompteur** : texte défilant superposé à la caméra frontale, vitesse et taille
  réglables, pause/reprise d'un tap sur le texte.
- **Texte stocké sur le serveur** (`script.txt`) : tu l'édites depuis le téléphone
  (bouton « ✎ Texte »), il est toujours là à la prochaine session — plus de texte
  prisonnier d'une appli.
- **Enregistrement** : bouton rouge → filme avec la caméra + micro du téléphone
  (mp4 sur iPhone, webm sur Android).
- **Envoi direct** : la vidéo part en HTTPS dans `videos/` sur le VPS, avec barre
  de progression.
- **Traitement auto** : si `PROMPTEUR_PROCESS_CMD` est défini, le serveur lance la
  commande avec le chemin de la vidéo en argument dès la réception.

## Installation sur le VPS

```bash
# 1. Copier ce dossier sur le VPS
scp -r prompteur/ user@VPS:/opt/localbooster/prompteur/

# 2. Dépendances
pip install fastapi uvicorn python-multipart

# 3. Lancer (choisis un vrai jeton !)
cd /opt/localbooster/prompteur
PROMPTEUR_TOKEN='un-secret-a-toi' \
PROMPTEUR_PROCESS_CMD='python3 /opt/localbooster/traite_video.py' \
uvicorn app:app --host 127.0.0.1 --port 8777
```

### Nginx (obligatoire : HTTPS)

⚠️ **La caméra du téléphone ne s'active qu'en HTTPS.** Il faut donc passer par le
nginx existant de `localbooster.site` :

```nginx
location /prompteur/ {
    proxy_pass http://127.0.0.1:8777/;
    proxy_http_version 1.1;
    client_max_body_size 2G;      # vidéos volumineuses
    proxy_request_buffering off;  # upload fluide
    proxy_read_timeout 300s;
}
```

Puis `sudo nginx -t && sudo systemctl reload nginx`.

### Service systemd (pour que ça survive aux reboots)

```ini
# /etc/systemd/system/prompteur.service
[Unit]
Description=Prompteur video LocalBooster
After=network.target

[Service]
WorkingDirectory=/opt/localbooster/prompteur
Environment=PROMPTEUR_TOKEN=un-secret-a-toi
Environment=PROMPTEUR_PROCESS_CMD=python3 /opt/localbooster/traite_video.py
ExecStart=/usr/bin/python3 -m uvicorn app:app --host 127.0.0.1 --port 8777
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload && sudo systemctl enable --now prompteur
```

## Utilisation sur le téléphone

1. Ouvrir **`https://localbooster.site/prompteur/?k=un-secret-a-toi`**
   (le jeton se mémorise tout seul — ensuite l'URL courte suffit).
2. Autoriser caméra + micro.
3. « ✎ Texte » → coller le script → « Enregistrer sur le serveur ».
4. Bouton rouge : l'enregistrement démarre **et** le texte défile.
5. Re-taper le bouton rouge pour arrêter → « Envoyer au serveur ».
6. La vidéo atterrit dans `videos/prompteur_YYYYMMDD_HHMMSS.mp4` et le
   traitement se lance.

Astuce : envoie en Wi-Fi si la vidéo est longue (compter ~1 Mo/seconde en 720p).

## Variables d'environnement

| Variable | Rôle | Défaut |
|---|---|---|
| `PROMPTEUR_TOKEN` | Jeton d'accès (recommandé) | *(vide = accès libre)* |
| `PROMPTEUR_VIDEOS` | Dossier de dépôt des vidéos | `./videos` |
| `PROMPTEUR_SCRIPT` | Fichier du texte du prompteur | `./script.txt` |
| `PROMPTEUR_PROCESS_CMD` | Commande lancée après upload (chemin vidéo ajouté en argument) | *(vide = pas de traitement)* |

## API (si un agent veut s'en servir)

- `GET /api/script?k=…` — texte du prompteur (text/plain)
- `PUT /api/script?k=…` — remplace le texte (corps text/plain)
- `POST /api/upload?k=…` — multipart, champ `video`
- `GET /api/videos?k=…` — liste des vidéos déposées
