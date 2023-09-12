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
        # jam this vector in as another row, incrementing the index
        self.df = pd.concat(
            [self.df, pd.DataFrame({"embedding": [vector], **metadata})],
            ignore_index=True,
        )

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

    @staticmethod
    def chunk(string: str) -> list[str]:
        """Breaks a long input string into one or more smaller ones."""
        # TODO this implementation is naive, loses context. Some nicer interleaving of contents is preferable.
        chunksize = 800
        return [string[i : i + chunksize] for i in range(0, len(string), chunksize)]
