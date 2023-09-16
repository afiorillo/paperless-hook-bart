#!/usr/bin/env python
import rich
import typer

from paperless_hook_bart.paperless_client import PaperlessClient
from paperless_hook_bart.processor import Processor
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
    proc = Processor(paperless_settings)
    result = proc.ingest_document_by_id(hook_settings.document_id)
    rich.print(f'Ingested [green]{result.ingested_documents}[/green] documents with [green]{result.ingested_vectors}[/green] vectors')

def typer_main():
    typer.run(main)

if __name__ == "__main__":
    typer_main()
