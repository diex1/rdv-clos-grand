"""Prompteur vidéo LocalBooster — à héberger sur le VPS.

Une seule page web mobile : téléprompteur superposé à la caméra du téléphone,
enregistrement vidéo, puis envoi direct sur le serveur. À la réception, le
serveur peut lancer automatiquement la commande de traitement.

Lancement :
    pip install fastapi uvicorn python-multipart
    PROMPTEUR_TOKEN=monsecret uvicorn app:app --host 127.0.0.1 --port 8777

Variables d'environnement :
    PROMPTEUR_TOKEN        jeton d'accès (fortement recommandé — sans lui, accès libre)
    PROMPTEUR_VIDEOS       dossier de dépôt des vidéos   (défaut : ./videos)
    PROMPTEUR_SCRIPT       fichier du texte du prompteur (défaut : ./script.txt)
    PROMPTEUR_PROCESS_CMD  commande lancée après chaque upload, le chemin de la
                           vidéo est ajouté en dernier argument
                           (ex. "python3 /opt/localbooster/traite_video.py")
"""
import datetime
import os
import pathlib
import shlex
import shutil
import subprocess

from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, PlainTextResponse

BASE_DIR = pathlib.Path(__file__).resolve().parent
VIDEO_DIR = pathlib.Path(os.environ.get("PROMPTEUR_VIDEOS", str(BASE_DIR / "videos")))
SCRIPT_FILE = pathlib.Path(os.environ.get("PROMPTEUR_SCRIPT", str(BASE_DIR / "script.txt")))
TOKEN = os.environ.get("PROMPTEUR_TOKEN", "")
PROCESS_CMD = os.environ.get("PROMPTEUR_PROCESS_CMD", "")

MAX_SCRIPT_BYTES = 200_000

app = FastAPI(title="Prompteur LocalBooster", docs_url=None, redoc_url=None)

EXT_BY_TYPE = {"video/mp4": ".mp4", "video/webm": ".webm", "video/quicktime": ".mov"}


def _check(k: str) -> None:
    if TOKEN and k != TOKEN:
        raise HTTPException(status_code=401, detail="jeton invalide")


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/script", response_class=PlainTextResponse)
def get_script(k: str = Query("")):
    _check(k)
    return SCRIPT_FILE.read_text(encoding="utf-8") if SCRIPT_FILE.exists() else ""


@app.put("/api/script")
async def put_script(request: Request, k: str = Query("")):
    _check(k)
    body = await request.body()
    if len(body) > MAX_SCRIPT_BYTES:
        raise HTTPException(status_code=413, detail="texte trop long")
    SCRIPT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SCRIPT_FILE.write_bytes(body)
    return {"ok": True, "octets": len(body)}


@app.post("/api/upload")
def upload(k: str = Query(""), video: UploadFile = File(...)):
    _check(k)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    base_type = (video.content_type or "").split(";")[0].strip()
    ext = EXT_BY_TYPE.get(base_type) or pathlib.Path(video.filename or "").suffix or ".webm"
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = VIDEO_DIR / f"prompteur_{stamp}{ext}"
    n = 1
    while dest.exists():
        dest = VIDEO_DIR / f"prompteur_{stamp}_{n}{ext}"
        n += 1
    with dest.open("wb") as out:
        shutil.copyfileobj(video.file, out)
    size = dest.stat().st_size
    if size == 0:
        dest.unlink()
        raise HTTPException(status_code=400, detail="fichier vide")
    traitement = False
    if PROCESS_CMD:
        subprocess.Popen(
            shlex.split(PROCESS_CMD) + [str(dest)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        traitement = True
    return {"ok": True, "fichier": dest.name, "octets": size, "traitement_lance": traitement}


@app.get("/api/videos")
def list_videos(k: str = Query("")):
    _check(k)
    if not VIDEO_DIR.exists():
        return {"videos": []}
    items = sorted(
        (p for p in VIDEO_DIR.iterdir() if p.is_file()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return {"videos": [{"nom": p.name, "octets": p.stat().st_size} for p in items]}
