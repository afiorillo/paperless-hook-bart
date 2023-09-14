from paperless_hook_bart.embeddings import BartEmbedder


def test_embeddings_happy_path(bart_embedder: BartEmbedder):
    vecs = bart_embedder.get_embeddings("Hello BART!")
    assert len(vecs) == 1  # it's short enough for a single vector, no chunks
    assert len(vecs[0]) == bart_embedder.model.shared.embedding_dim

def test_embeddings_lots_of_text(bart_embedder: BartEmbedder):
    lipsum = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam rhoncus, tortor in venenatis sodales, arcu leo pellentesque arcu, vel ultricies turpis nibh nec lacus. Donec tempus elit purus, vitae venenatis nulla iaculis in. Fusce a turpis eget ante interdum vulputate ac vitae mi. Curabitur quis felis sit amet odio hendrerit congue. Sed dapibus et arcu ac laoreet. Vivamus sed facilisis purus. Nulla vehicula efficitur augue id vehicula. Fusce vehicula, turpis ultrices aliquet consequat, odio nisi aliquam purus, sit amet cursus purus turpis at eros. Integer tincidunt felis eget dapibus congue. Integer quis justo condimentum, lobortis sapien vel, pulvinar erat. In sagittis nibh viverra dictum volutpat.
    Fusce rutrum odio nec lacus convallis tincidunt. Vestibulum laoreet at metus consequat scelerisque. Duis ac enim a mauris sollicitudin pharetra. Quisque id justo dui. Aliquam ex nulla, auctor vitae tristique feugiat, faucibus et tortor. Proin tristique placerat magna a gravida. Nullam eget finibus tortor, sit amet sollicitudin libero.
    Nullam vitae nulla metus. Vivamus pulvinar sed tellus eu rhoncus. Phasellus vitae metus lorem. Aenean semper vehicula viverra. Aliquam ac nunc dui. Curabitur mollis ex ut facilisis porta. Integer venenatis ipsum blandit, vestibulum mi in, tristique nisl. Pellentesque ultrices nunc nec vulputate molestie. Duis vehicula neque semper justo sodales, vitae egestas massa vestibulum. Praesent dapibus, odio at ornare ullamcorper, libero ex fermentum nulla, vel tincidunt augue quam et neque. Nulla ut justo dolor. Sed tempor vestibulum turpis at tristique. Sed commodo massa velit. Mauris tincidunt nibh et magna auctor placerat. Nullam imperdiet nisl id nibh maximus convallis nec sit amet tellus. Praesent vel pharetra libero, vel ultrices erat.
    Donec porta erat felis, in tristique mi tempus at. Ut malesuada mattis felis non tempus. Proin nec tempus turpis. In varius id ligula sed venenatis. Etiam nec vulputate nulla, commodo imperdiet ex. Maecenas scelerisque varius ante, non aliquet neque mollis sit amet. Sed id laoreet massa. Phasellus nec dui sed velit mollis laoreet. Pellentesque tellus odio, dignissim ac vehicula euismod, commodo id turpis. Fusce lacinia ornare massa, vel placerat massa convallis eu. Fusce a ipsum maximus magna egestas dignissim. In massa lacus, condimentum quis nunc laoreet, eleifend pharetra nisl. Ut volutpat elit tellus, quis tincidunt libero feugiat at.
    Vivamus eu lacinia ex. Mauris luctus tempor nibh, et sollicitudin purus convallis a. In egestas dictum ultricies. Donec fermentum scelerisque bibendum. Morbi tincidunt convallis nunc, sed semper magna suscipit eget. Praesent at arcu nec metus consequat placerat. Morbi dolor turpis, lacinia vitae orci non, auctor tempor ligula. Suspendisse fringilla varius nibh. Morbi efficitur purus diam, sed cursus tortor mattis non. Sed ullamcorper nisi consequat, condimentum velit in, scelerisque nisl.
    """
    vecs = bart_embedder.get_embeddings(lipsum)
    assert len(vecs) == 4  # since it was a long string, it was chunked and each chunk has its own embedding
