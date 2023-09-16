#!/usr/bin/env python
import rich
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TaskProgressColumn, TimeRemainingColumn
import typer

from paperless_hook_bart.processor import Processor, UnreadableDocument
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

    with Progress(
        TextColumn("[progress.description]{task.description} {task.completed}/{task.total}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
    ) as progress:
        docs_ingested, vecs_ingested = 0, 0
        doc_iterator = proc.client.iter_all_documents()
        for document in progress.track(doc_iterator, description='Backfilling...'):
            try:
                res = proc.ingest_document(document)
            except UnreadableDocument:
                pass  # just skip those?
            docs_ingested += 1
            vecs_ingested += res.ingested_vectors

    rich.print(f'Ingested [green]{docs_ingested}[/green] documents with [green]{vecs_ingested}[/green] vectors.')    


def typer_main():
    typer.run(main)

if __name__ == "__main__":
    typer_main()
