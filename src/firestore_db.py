# Module pour interagir avec la base de données Firestore

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import firebase_admin
from firebase_admin import credentials, firestore

# 'type annotations' afin d'améliorer l'autocomplétion dans VS Code
if TYPE_CHECKING:
    from google.cloud.firestore import Client


FIREBASE_CERTIF = Path("src/antitriche-firebase-adminsdk.json")


class FirestoreDB:
    # Classe pour interagir avec la base de données Firestore

    def __init__(self):
        """Initialise la connexion à la base de données"""
        # Vérifie que le fichier existe
        assert FIREBASE_CERTIF.exists(), f"Le fichier {FIREBASE_CERTIF} n'existe pas !"
        if not firebase_admin._apps:  # noqa: SLF001
            cred = credentials.Certificate(FIREBASE_CERTIF)
            firebase_admin.initialize_app(cred)

        self._client: Client = firestore.client()

    def collection(self, collection: str):
        """Renvoie une référence vers une collection"""
        return self._client.collection(collection)

    def doc(self, doc_path: str):
        """Renvoie une référence vers un document"""
        return self._client.document(doc_path)

    def set(self, doc_path: str, data: dict):
        """Ajoute ou remplace des données dans une collection"""
        self.doc(doc_path).set(data)

    def update(self, doc_path: str, data: dict):
        """Met à jour des données existantes dans une collection"""
        self.doc(doc_path).update(data)

    def add(self, collection: str, data: dict):
        """Ajoute des données dans une collection. ID auto-généré"""
        self.collection(collection).add(data)

    def delete(self, doc_path: str):
        """Supprime un document"""
        self.doc(doc_path).delete()

    def print(self, collection: str):
        """Affiche le contenu d'une collection"""
        coll_ref = self.collection(collection)
        for doc in coll_ref.stream():
            print(f"{doc.id} : {doc.to_dict()}")

    def get_all_documents(self, collection_name: str):
        """Retrieve all documents from a specified collection"""
        collection_ref = self.collection(collection_name)
        documents = collection_ref.stream()

        all_docs = []
        for doc in documents:
            doc_data = doc.to_dict()
            assert doc_data is not None
            doc_data["id"] = doc.id  # Optionally include the document ID
            all_docs.append(doc_data)

        return all_docs

    def get_question(self, question_id):
        # Assurez-vous que le chemin est correct
        question_ref = self.doc(f"questions/{question_id}")

        return question_ref.get().to_dict()
