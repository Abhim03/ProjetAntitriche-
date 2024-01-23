from firestore_db import FirestoreDB
import os

db = FirestoreDB()


for subdir, _, files in os.walk("src/questions"):
    if len(files) == 3:  # Assurez-vous qu'il y a exactement deux fichierssrc/add_test_firebase.py
        data = {}
        for file in files:
            file_path = os.path.join(subdir, file)
            with open(file_path) as f:
                text = f.read()
                data[
                    file.split(".")[0]
                ] = text  # Ajoute chaque fichier au dictionnaire avec le nom de fichier comme clé
            db.set(f"Questions/{os.path.basename(subdir)}", data)
