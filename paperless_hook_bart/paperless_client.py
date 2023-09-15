from datetime import datetime
from typing import Iterator

import requests
from pydantic import BaseModel

from paperless_hook_bart.settings import PaperlessServerSettings

class PaperlessDocument(BaseModel):
    id: int
    content: str
    title: str
    added: datetime

    def url(self, paperless_settings: PaperlessServerSettings):
        return f'{paperless_settings.paperless_base_url}/documents/{self.id}/details'


class PaperlessClient:
    """
    An incomplete client around the Paperless-ngx REST API. Documented here:
    https://docs.paperless-ngx.com/api/
    """

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")  # if a trailing slash is given, chop it
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Token {token}"

    def get_document(self, document_id: int) -> PaperlessDocument:
        full_url = f"{self.base_url}/api/documents/{document_id}/?format=json"
        resp = self.session.get(full_url)
        resp.raise_for_status()
        return PaperlessDocument.parse_raw(resp.content)

    def iter_all_documents(self) -> Iterator[PaperlessDocument]:
        full_url = f'{self.base_url}/api/documents/?format=json'
        while full_url is not None:
            resp = self.session.get(full_url)
            payload = resp.json()
            docs = payload.get('results', [])
            for doc in docs:
                yield PaperlessDocument.parse_obj(doc)
            
            full_url = payload.get('next', None)
            if full_url is not None:
                # we want to add this query param to get JSON back
                full_url += '&format=json'