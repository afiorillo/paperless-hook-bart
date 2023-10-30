# Paperless Hook BART

This is a proof of concept to show that [BART](https://huggingface.co/facebook/bart-large) can be used to enhance search in [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx).
It originates from the proposal discussion [here](https://github.com/paperless-ngx/paperless-ngx/discussions/4059).

## Usage

This project is experimental, so expect rough edges.
Currently you can run the script by preparing the development environment (`poetry install`, documented below) and running

```bash
# you must provide credentials to access the paperless server
# see https://docs.paperless-ngx.com/api/#authorization for details
# go to "$PAPERLESS_BASE_URL/admin/authtoken/tokenproxy/" to create a token
export PAPERLESS_BASE_URL="http://..."
export PAPERLESS_TOKEN="abcd1234..."
# the hook provides a DOCUMENT_ID to specify which document was just consumed
export DOCUMENT_ID="1"
# and finally, you can run the hook
poetry run post_consume_script
```

**Note:** this will almost certainly have to change to improve portability.

## Contributing

This is an open source project and contributions are welcome!
Some basic ground rules:

- Please make all contributions through a PR. This enables discussing the changes *before* accepting them.
- Please be polite and civil. This is a volunteer project and it ought to be fun.

### Developing

This project uses Python 3.11+ and [Poetry](https://python-poetry.org/). Assuming you have these installed, preparing the developing environment should just be:

```bash
poetry install
```

You can run the unit tests with

```bash
pytest tests/
```
