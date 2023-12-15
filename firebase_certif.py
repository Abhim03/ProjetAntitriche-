from pathlib import Path
import shutil

# chemin vers le dossier "~/Downloads" ou "~/Téléchargements"
downloads_path = Path.home() / "Downloads"
if not downloads_path.exists():
    downloads_path = Path.home() / "Téléchargements"


firebase_key = downloads_path / "antitriche-firebase-adminsdk.json"

# déplace le fichier vers le répertoire courant (du projet) si le fichier existe
if firebase_key.exists():
    shutil.move(firebase_key, Path.cwd())
else:
    print(f"Le fichier n'a pas été trouvé dans {downloads_path}")
