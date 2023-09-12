from requests.exceptions import RequestException
from pydantic import ValidationError

from paperless_hook_bart.paperless_client import PaperlessClient


class IngestionError(Exception):
    """A catch-all for errors while ingesting documents into the vector store."""


class UnreadableDocument(IngestionError):
    """The document did not contain any contents, so it can't be embedded."""


def ingest_document(client: PaperlessClient, document_id: int):
    """
    Fetches data for an already consumed document in Paperless and stores its embeddings
    in the vector store.
    """
    try:
        doc = client.get_document(hook_settings.document_id)
    except RequestException as err:
        raise IngestionError("unable to fetch from paperless server") from err
    except ValidationError as err:
        raise IngestionError("unable to parse response") from err

    contents = doc.content
    if not contents:
        raise UnreadableDocument(f"document is empty? {doc.id}")

    # TODO open the vector store, chunk the contents, embed them, store them.
