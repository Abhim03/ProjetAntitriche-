# Module pour interagir avec la base de données Firestore

from __future__ import annotations

import random
from pathlib import Path
from typing import TYPE_CHECKING

import firebase_admin
from firebase_admin import credentials, firestore

# 'type annotations' afin d'améliorer l'autocomplétion dans VS Code
if TYPE_CHECKING:
    from google.cloud.firestore import Client


_FIREBASE_CERTIF = Path("antitriche-firebase-adminsdk.json")


class FirestoreDB:
    # Classe pour interagir avec la base de données Firestore

    def __init__(self):
        """Initialise la connexion à la base de données"""
        # Vérifie que le fichier existe
        assert _FIREBASE_CERTIF.exists(), f"Le fichier {_FIREBASE_CERTIF.resolve()} n'existe pas !"

        cred = credentials.Certificate(_FIREBASE_CERTIF)
        if not firebase_admin._apps:  # noqa: SLF001
            firebase_admin.initialize_app(cred)

        self._client: Client = firestore.client()

    def _coll(self, collection: str):
        """Renvoie une référence vers une collection"""
        return self._client.collection(collection)

    def _doc(self, doc_path: str):
        """Renvoie une référence vers un document"""
        return self._client.document(doc_path)

    def get_doc(self, doc_path: str):
        """Renvoie un document"""
        result = self._doc(doc_path).get().to_dict()
        assert result is not None
        return result

    def set_doc(self, doc_path: str, data: dict):
        """Ajoute ou remplace des données dans une collection"""
        self._doc(doc_path).set(data)

    def update_doc(self, doc_path: str, data: dict):
        """Met à jour des données existantes dans une collection"""
        self._doc(doc_path).update(data)

    def add_doc(self, collection: str, data: dict):
        """Ajoute des données dans une collection. ID auto-généré"""
        self._coll(collection).add(data)

    def delete_doc(self, doc_path: str):
        """Supprime un document"""
        self._doc(doc_path).delete()

    def print_collection(self, collection: str):
        """Affiche le contenu d'une collection"""
        coll_ref = self._coll(collection)
        for doc in coll_ref.stream():
            print(f"{doc.id} : {doc.to_dict()}")

    def get_doc_list(self, collection: str):
        """Renvoie une liste de tous les documents d'une collection"""
        collection_ref = self._coll(collection)

        all_docs: list[dict] = []
        for doc in collection_ref.stream():
            doc_data = doc.to_dict()
            assert doc_data is not None
            doc_data["id"] = doc.id  # Optionally include the document ID
            all_docs.append(doc_data)

        return all_docs

    def get_question(self, question_id):
        """Récupère une question"""
        # Assurez-vous que le chemin est correct
        result = self._doc(f"questions/{question_id}").get().to_dict()
        assert result is not None
        return result

    def get_random_question(self, language):
        """Récupère une question aléatoire pour un langage donné"""
        questions = self.get_doc_list("Questions")
        return random.choice(questions)
