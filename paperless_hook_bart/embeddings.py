from transformers import BartTokenizer, BartModel


class BartEmbedder:
    """
    A wrapper around the BART language model to embed strings.
    On construction, if not available locally, it will download the pre-trained model ~1GB.
    """

    def __init__(self):
        self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
        self.model = BartModel.from_pretrained("facebook/bart-large")

    @staticmethod
    def chunk(string: str) -> list[str]:
        """Breaks a long input string into one or more smaller ones."""
        # TODO this implementation is naive, loses context. Some nicer interleaving of contents is preferable.
        chunksize = 800
        return [string[i : i + chunksize] for i in range(0, len(string), chunksize)]

    def get_embeddings(self, string: str) -> list[list[float]]:
        """Given a string, returns one or more embedding vectors representing its semantic meaning."""
        strings = self.chunk(string)
        embeddings: list[list[float]] = []
        for s in strings:
            inputs = self.tokenizer(s, return_tensors="pt")
            outputs = self.model(**inputs)
            # rather than a tensor, we want it as a simple vector of floats
            embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
            embeddings.append(list(embedding.flatten()))
        return embeddings
