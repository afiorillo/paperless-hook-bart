#!/usr/bin/env python
import typer

from paperless_hook_bart.paperless_client import PaperlessClient
from paperless_hook_bart.processor import ingest_document
from paperless_hook_bart.settings import (
    PostConsumeHookSettings,
    PaperlessServerSettings,
)


def main():
    # we expect we're being called by Paperless and the settings are in the environment
    hook_settings = PostConsumeHookSettings()
    # we also expect for now the token is just provided magically
    paperless_settings = PaperlessServerSettings()
    # create a client
    client = PaperlessClient(
        base_url=str(paperless_settings.paperless_base_url),
        token=paperless_settings.paperless_token,
    )
    # and actually process the document
    ingest_document(client, hook_settings.document_id)


def typer_main():
    typer.run(main)
