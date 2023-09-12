from paperless_hook_bart.vector_store import InMemoryVectorStore


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
