from pathlib import Path

from firestore_db import FirestoreDB

db = FirestoreDB()

with Path("test.py").open() as file:  # dir houn esim 4e élli dor  code lteb9i
    text = file.read()

data = {"text": text}


db.set_data("chatgpt/minimumlist", data)

db.print_collection("chatgpt")
