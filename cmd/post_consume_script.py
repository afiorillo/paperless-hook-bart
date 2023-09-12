#!/usr/bin/env python
import typer

from paperless_hook_bart.settings import PostConsumeHookSettings


def main():
    # we expect we're being called by Paperless and the settings are in the environment
    settings = PostConsumeHookSettings()
    # TODO the rest
    print(settings)


def typer_main():
    typer.run(main)
