from pathlib import Path

import numpy as np
import pandas as pd


class InMemoryVectorStore:
    """
    A bare-bones, very forgetful, vector store.
    """

    def __init__(self):
        # start empty for now
        self.df = pd.DataFrame()

    def store(self, vector: list[float], **metadata):
        if ('embedding' in self.df.columns) and (self.df['embedding'].apply(lambda testvec: (vector == testvec).all()).any()):
            # FIXME there is probably a way to do this without an .apply() which slows things down
            # This also essentially prevents updates, but doing update logic would be tricky.
            # E.g. find duplicates, find the document ID associated, update all of those rows.
            # What if mutiple document IDs etc?
            return None

        # jam this vector in as another row, incrementing the index
        self.df = pd.concat(
            [self.df, pd.DataFrame({"embedding": [vector], **metadata})],
            ignore_index=True,
        )
        return self.df.index[-1]

    def nearest_neighbors(self, vector: list[float], nearest_n: int = 5):
        """Use Cosine similarity to find the N nearest vectors."""
        # dump the whole search corpus into a big 2D matrix
        corpus = np.stack(self.df["embedding"].to_numpy())
        # make the vector into a 2D matrix with the same number of identical rows
        search = np.repeat(np.atleast_2d(vector), corpus.shape[0], axis=0)
        # we want the row-wise cosine similarity
        dot_product = np.sum(search * corpus, axis=1)
        vector_mag = np.linalg.norm(vector)
        corpus_mag = np.linalg.norm(corpus, axis=1)
        cosine_sim = dot_product / (vector_mag * corpus_mag)
        # and the indexes of the top-N give us the rows in the dataframe for the nearest neighbors
        smallest_to_largest = np.argsort(cosine_sim)
        largest_to_smallest = np.array(list(reversed(smallest_to_largest)))  # FIXME
        top_n = largest_to_smallest[:nearest_n]
        return self.df.loc[top_n]

class DiskVectorStore(InMemoryVectorStore):
    """
    A persistent vector store that writes to disk whenever a vector is added.
    Stores the dataframe as a Parquet format.
    """

    def read_file(self):
        self.df = pd.read_parquet(self.filepath)

    def write_file(self):
        self.df.to_parquet(self.filepath)

    def __init__(self, filepath: Path):
        self.filepath = Path(filepath)
        
        if self.filepath.exists():
            self.read_file()
        else:
            # let's start with an empty corpus and write it to disk
            self.df = pd.DataFrame()
            self.write_file()

    def store(self, vector: list[float], **metadata):
        res = super().store(vector, **metadata)
        if res is not None:
            # we only need to sync if there are changes 
            self.write_file()
        return res
    