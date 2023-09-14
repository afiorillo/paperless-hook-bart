import pytest

from paperless_hook_bart.embeddings import BartEmbedder

@pytest.fixture(scope='session')
def bart_embedder():
    return BartEmbedder()
