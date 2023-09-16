from datetime import datetime
from typing import Iterator

import requests
from pydantic import BaseModel, parse_obj_as

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
        return DocumentsIterator(self)


class DocumentsIterator:
    def __init__(self, client: PaperlessClient, **filter_args):
        self.client = client
        # paperless supports searching a subset of documents
        # https://docs.paperless-ngx.com/api/#searching-for-documents
        self.filter_args = filter_args  # TODO
        self.filter_args['format'] = 'json'

        # the request gives a page of documents at a time, so we'll keep them and paginate only
        # once all of the previous page's docs have been iterated
        self._buf: list[PaperlessDocument] = []
        self._count: int = 0
        self._next_url = f'{self.client.base_url}/api/documents/'
        # and load up the first page
        self._do_request()

    def _do_request(self):
        if self._next_url is None:
            raise StopIteration

        resp = self.client.session.get(self._next_url, params=self.filter_args)
        payload = resp.json()
        self._count = payload.get("count", 0)
        docs = payload.get('results', [])
        self._buf = parse_obj_as(list[PaperlessDocument], docs)
        
        self._next_url = payload.get('next', None)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._buf) == 0:
            # if there is no next page, this should stop iteration
            self._do_request()
        return self._buf.pop(0)

    def __len__(self):
        return self._count