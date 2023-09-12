#!/usr/bin/env python
import typer

from paperless_hook_bart.paperless_client import PaperlessClient
from paperless_hook_bart.settings import (
    PostConsumeHookSettings,
    PaperlessServerSettings,
)


def main():
    # we expect we're being called by Paperless and the settings are in the environment
    hook_settings = PostConsumeHookSettings()
    # we also expect for now the token is just provided magically
    paperless_settings = PaperlessServerSettings()
    # get the document in question
    client = PaperlessClient(
        base_url=str(paperless_settings.paperless_base_url),
        token=paperless_settings.paperless_token,
    )
    doc = client.get_document(hook_settings.document_id)
    # TODO the rest
    print(doc.model_dump_json(indent=2))


def typer_main():
    typer.run(main)
