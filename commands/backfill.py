#!/usr/bin/env python
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
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
    paperless_settings = PaperlessServerSettings()  # must be available in the env vars
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        taskid = progress.add_task(description="Loading model...", total=None)
        proc = Processor(paperless_settings)
        progress.remove_task(taskid)

        taskid = progress.add_task(description="Backfilling...", total=None)
        docs_ingested, vecs_ingested = 0, 0
        for res in proc.iter_ingest_all_documents():
            progress.update(taskid, advance=1)
            docs_ingested += 1
            vecs_ingested += res.ingested_vectors
        progress.remove_task(taskid)

    rich.print(f'Ingested [green]{docs_ingested}[/green] documents with [green]{vecs_ingested}[/green] vectors.')    


def typer_main():
    typer.run(main)

if __name__ == "__main__":
    typer_main()
