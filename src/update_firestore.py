from pathlib import Path

from firestore_db import FirestoreDB

db = FirestoreDB()

if __name__ == "__main__":
    for subdir in Path("questions").iterdir():
        if not subdir.is_dir():
            continue
        data = {}
        for file in subdir.iterdir():
            with file.open() as f:
                text = f.read()
                data[file.stem] = text
        db.set_doc(f"Questions/{subdir.name}", data)
