from pathlib import Path
import shutil

# chemin vers le dossier "~/Downloads" ou "~/Téléchargements"
downloads_path = Path.home() / "Downloads"
if not downloads_path.exists():
    downloads_path = Path.home() / "Téléchargements"


firestore_certif = downloads_path / "antitriche-firebase-adminsdk.json"

# déplace le fichier vers le répertoire courant (du projet) si le fichier existe
if firestore_certif.exists():
    shutil.move(firestore_certif, Path.cwd())
else:
    print(f"Le fichier n'a pas été trouvé dans {downloads_path}")
