#!/usr/bin/env python
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import typer

from paperless_hook_bart.processor import Processor
from paperless_hook_bart.settings import (
    PaperlessServerSettings,
)


def main():
    # TODO this script is intended to backfill the vector store with the already-consumed documents
    # Basically:
    # 1. Get all documents
    # 2. For each, get the contents, and ingest like the post_consume_script.
    # It will probably be very slow, could probably be parallelized, but then some rewriting of the vector store
    # needs to be done to make it multiproc-safe.
    pass

def typer_main():
    typer.run(main)

if __name__ == "__main__":
    typer_main()
