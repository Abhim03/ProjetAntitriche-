import shutil
from pathlib import Path

# chemin vers le dossier "~/Downloads" ou "~/Téléchargements"
DOWNLOADS = Path.home() / "Downloads"
if not DOWNLOADS.exists():
    DOWNLOADS = Path.home() / "Téléchargements"


FIREBASE_CERTIF = DOWNLOADS / "antitriche-firebase-adminsdk.json"

if __name__ == "__main__":
    # déplace le fichier vers le répertoire courant (du projet) si le fichier existe
    if FIREBASE_CERTIF.exists():
        shutil.move(FIREBASE_CERTIF, Path.cwd())
    else:
        print(f"Le fichier n'a pas été trouvé dans {DOWNLOADS}")
