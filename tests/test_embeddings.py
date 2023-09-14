from paperless_hook_bart.embeddings import BartEmbedder


def test_embeddings_happy_path(bart_embedder: BartEmbedder):
    vecs = bart_embedder.get_embeddings("Hello BART!")
    assert len(vecs) == 1  # it's short enough for a single vector, no chunks
    assert len(vecs[0]) == bart_embedder.model.shared.embedding_dim