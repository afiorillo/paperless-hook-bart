# Paperless Hook BART

This is a proof of concept to show that [BART](https://huggingface.co/facebook/bart-large) can be used to enhance search in [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx).
It originates from the proposal discussion [here](https://github.com/paperless-ngx/paperless-ngx/discussions/4059).

## Usage

This project is experimental, so expect rough edges.
Currently you can run the script by preparing the development environment (`poetry install`, documented below) and running

```bash
poetry run post_consume_script
```

**Note:** this will almost certainly have to change to improve portability.

### Developing

This project uses Python 3.11+ and [Poetry](https://python-poetry.org/). Assuming you have these installed, preparing the developing environment should just be:

```bash
poetry install
```
