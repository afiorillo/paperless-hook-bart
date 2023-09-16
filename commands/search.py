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
    paperless_settings = PaperlessServerSettings()  # must be available in the env vars
    query = typer.prompt("Search query:")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        taskid = progress.add_task(description="Loading model...", total=None)
        proc = Processor(paperless_settings)
        progress.remove_task(taskid)

        taskid = progress.add_task(description="Searching...", total=None)
        results = proc.search(query)
        progress.remove_task(taskid)

    table = Table(title='Results')
    table.add_column("Document ID")
    table.add_column("Document Name")
    table.add_column("Link")

    for result in results:
        table.add_row(str(result.id), result.title, result.url(paperless_settings))

    console = Console()
    console.print(table)

def typer_main():
    typer.run(main)

if __name__ == "__main__":
    typer_main()
