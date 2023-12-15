from __future__ import annotations

from typing import TYPE_CHECKING

import firebase_admin
from firebase_admin import credentials, firestore

# 'type annotations' afin d'améliorer l'autocomplétion dans VS Code
if TYPE_CHECKING:
    from google.cloud.firestore import Client


class FirestoreDB:
    """Classe pour interagir avec la base de données Firestore"""

    def __init__(self, certif: str):
        """Initialise la connexion à la base de données"""
        cred = credentials.Certificate(certif)
        app = firebase_admin.initialize_app(cred)

        self.client: Client = firestore.client(app)

    def set_data(self, collection: str, doc_id: str, data: dict):
        """Ajoute ou remplace des données dans une collection"""
        self.client.collection(collection).document(doc_id).set(data)

    def update_data(self, collection: str, doc_id: str, data: dict):
        """Met à jour des données existantes dans une collection"""
        self.client.collection(collection).document(doc_id).update(data)

    def print(self, collection: str):
        """Affiche le contenu d'une collection"""
        coll_ref = self.client.collection(collection)
        for doc in coll_ref.stream():
            print(f"{doc.id} : {doc.to_dict()}")
