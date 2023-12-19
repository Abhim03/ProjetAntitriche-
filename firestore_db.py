"""Module pour interagir avec la base de données Firestore"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import firebase_admin
from firebase_admin import credentials, firestore

# 'type annotations' afin d'améliorer l'autocomplétion dans VS Code
if TYPE_CHECKING:
    from google.cloud.firestore import Client


FIREBASE_CERTIF = Path("antitriche-firebase-adminsdk.json")


class FirestoreDB:
    """Classe pour interagir avec la base de données Firestore"""

    def __init__(self):
        """Initialise la connexion à la base de données"""
        # Vérifie que le fichier existe
        assert FIREBASE_CERTIF.exists(), f"Le fichier {FIREBASE_CERTIF} n'existe pas !"

        cred = credentials.Certificate(FIREBASE_CERTIF)
        app = firebase_admin.initialize_app(cred)

        self._client: Client = firestore.client(app)

    def coll_ref(self, collection: str):
        """Renvoie une référence vers une collection"""
        return self._client.collection(collection)

    def doc_ref(self, collection: str, doc_id: str):
        """Renvoie une référence vers un document"""
        return self._client.collection(collection).document(doc_id)

    def set(self, collection: str, doc_id: str, data: dict):
        """Ajoute ou remplace des données dans une collection"""
        self._client.collection(collection).document(doc_id).set(data)

    def update(self, collection: str, doc_id: str, data: dict):
        """Met à jour des données existantes dans une collection"""
        self._client.collection(collection).document(doc_id).update(data)

    def print(self, collection: str):
        """Affiche le contenu d'une collection"""
        coll_ref = self._client.collection(collection)
        for doc in coll_ref.stream():
            print(f"{doc.id} : {doc.to_dict()}")
