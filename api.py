import logging
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import asyncio  # toegevoegd

_LOGGER = logging.getLogger(__name__)


class VistapoolApi:
    def __init__(self, credential_path: str):
        self._firestore_client = None
        self._credential_path = credential_path

    def initialize(self):
        if not os.path.exists(self._credential_path):
            _LOGGER.error("Firebase credential file not found at %s", self._credential_path)
            raise FileNotFoundError(f"Firebase credential file not found at {self._credential_path}")

        cred = credentials.Certificate(self._credential_path)
        firebase_admin.initialize_app(cred)
        self._firestore_client = firestore.client()

    def get_document_data(self, document_path: str) -> dict[str, any]:
        """Synchronous call to Firestore."""
        doc_ref = self._firestore_client.document(document_path)
        doc = doc_ref.get()
        return doc.to_dict()

    async def async_get_document_data(self, document_path: str) -> dict[str, any]:
        """Async wrapper for get_document_data using asyncio.to_thread()."""
        return await asyncio.to_thread(self.get_document_data, document_path)

    def parse_firestore_data(self, data: dict[str, any]) -> dict[str, any]:
        parsed_data = {}
        if not data:
            return parsed_data

        for key, value in data.items():
            if isinstance(value, dict) and "value" in value:
                parsed_data[key] = value["value"]
            else:
                parsed_data[key] = value

        return parsed_data