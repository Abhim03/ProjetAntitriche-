from firestore_db import FirestoreDB

db = FirestoreDB()

with open("test.py") as file:  # dir houn esim 4e élli dor  code lteb9i
    text = file.read()

data = {"text": text}


db.set("chatgpt/minimumlist", data)

db.print("chatgpt")
