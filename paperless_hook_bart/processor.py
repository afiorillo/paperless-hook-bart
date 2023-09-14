from typing import NamedTuple

from requests.exceptions import RequestException
from pydantic import ValidationError

from paperless_hook_bart.embeddings import BartEmbedder
from paperless_hook_bart.paperless_client import PaperlessClient
from paperless_hook_bart.settings import PaperlessServerSettings
from paperless_hook_bart.vector_store import DiskVectorStore


class IngestionError(Exception):
    """A catch-all for errors while ingesting documents into the vector store."""


class UnreadableDocument(IngestionError):
    """The document did not contain any contents, so it can't be embedded."""

class IngestionResult(NamedTuple):
    ingested_documents: int
    ingested_vectors: int

class Processor:

    def __init__(self, paperless_settings: PaperlessServerSettings):
        self.client = PaperlessClient(
            base_url=str(paperless_settings.paperless_base_url),
            token=paperless_settings.paperless_token,
        )
        self.store = DiskVectorStore('vectorstore.parquet')
        # get this lazily, since it occupies a lot of memory
        self._embedder = None

    @property
    def embedder(self) -> BartEmbedder:
        if self._embedder is None:
            self._embedder = BartEmbedder()
        return self._embedder

    def ingest_document(self, document_id: int) -> IngestionResult:
        """
        Fetches data for an already consumed document in Paperless and stores its embeddings
        in the vector store.
        """
        try:
            doc = self.client.get_document(document_id)
        except RequestException as err:
            raise IngestionError("unable to fetch from paperless server") from err
        except ValidationError as err:
            raise IngestionError("unable to parse response") from err

        contents = doc.content
        if not contents:
            raise UnreadableDocument(f"document is empty? {doc.id}")

        vectors = self.embedder.get_embeddings(contents)
        for vec in vectors:
            self.store.store(vec, document_id=doc.id)
        return IngestionResult(1, len(vectors))
