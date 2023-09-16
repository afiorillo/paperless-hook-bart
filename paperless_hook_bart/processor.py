from typing import NamedTuple, Iterator

from requests.exceptions import RequestException
from pydantic import ValidationError, parse_obj_as

from paperless_hook_bart.embeddings import BartEmbedder
from paperless_hook_bart.paperless_client import PaperlessClient, PaperlessDocument
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

    def ingest_document_by_id(self, document_id: int) -> IngestionResult:
        """
        Fetches the document and metadata from Paperless, and then ingests it.
        """
        try:
            doc = self.client.get_document(document_id)
        except RequestException as err:
            raise IngestionError("unable to fetch from paperless server") from err
        except ValidationError as err:
            raise IngestionError("unable to parse response") from err
        return self.ingest_document(doc)


    def ingest_document(self, document: PaperlessDocument) -> IngestionResult:
        """
        Store the embeddings of a given Paperless document into the vector store, along with metadata.
        """
        contents = document.content
        if not contents:
            raise UnreadableDocument(f"document is empty? {document.id}")
        
        if document.id in self.store.df['id']:
            # if the document was already ingested, we can skip embedding it
            return IngestionResult(1, 0)

        vectors = self.embedder.get_embeddings(contents)
        vecs_stored = 0
        for vec in vectors:
            res = self.store.store(vec, **document.dict())
            if res is not None:
                vecs_stored += 1
        return IngestionResult(1, vecs_stored)

    def search(self, searchstring: str, max_results: int = 5) -> list[PaperlessDocument]:
        searchvecs = self.embedder.get_embeddings(searchstring)
        # TODO long search strings would require supporting searching with all the vectors
        # from each chunk and combining them in a clever way. For now we just support short
        # search strings.
        searchvec = searchvecs[0]

        # the NN search may return multiple vectors for the same document, so we want to deduplicate
        # with only one result per document ID
        results = self.store.nearest_neighbors(searchvec, nearest_n=10*max_results)
        results.drop_duplicates('id', keep='first', inplace=True)

        # return the results in order, excluding the embedding itself

        # TODO this should handle backwards compatibility better. As-is, if any of the results contain data
        # from an older structure version (missing required fields) then the whole thing will crash.
        return parse_obj_as(list[PaperlessDocument], results.drop('embedding', axis=1).to_dict('records'))