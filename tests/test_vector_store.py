from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from paperless_hook_bart.vector_store import InMemoryVectorStore, DiskVectorStore


def test_vector_store_happy_path_3d():
    vs = InMemoryVectorStore()
    # vector stores can have sparse metadata
    vs.store([1, 2, 3], color="blue")
    vs.store([4, 5, 6], color="red", is_red=True)
    vs.store([7, 8, 9], color="brown")

    result = vs.nearest_neighbors([4, 5, 7], nearest_n=2)
    similar_indices = result.index
    assert result.loc[similar_indices[0]].color == "red"
    assert result.loc[similar_indices[0]].is_red
    assert result.loc[similar_indices[1]].color == "brown"

def test_vector_store_happy_path_1024d():
    vs = InMemoryVectorStore()
    # seed some search corpus
    for idx in range(1000):
        vec = np.random.random(1024)
        vs.store(vec, idx=idx)
    
    result = vs.nearest_neighbors(np.ones(1024), nearest_n=5)
    assert result.shape[0] == 5  # because we wanted 5 results

def test_persistent_vector_store():
    with TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir, 'vectorstore.parquet')

        # we may create an instance of this and store vectors, those end up on disk
        vs = DiskVectorStore(filepath)
        vs.store([1, 2, 3], food='pizza')
        # later we may create a new instance and retrieve those vectors
        vs2 = DiskVectorStore(filepath)
        result = vs.nearest_neighbors([1, 2, 3])
        assert result.loc[0].food == 'pizza'
