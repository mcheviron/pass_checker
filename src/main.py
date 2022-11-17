#!usr/bin/env python

import contextlib
from typing import Optional

import typer
from rich.traceback import install

from commands import (
    process_csv,
    process_file,
    process_json,
    process_single_password,
)

install(show_locals=True)


def main(
    password: Optional[str] = typer.Option(
        None,
        "--password",
        "-p",
        help="The password to check if you just want to check one password",
        show_default=False,
    ),
    file: Optional[str] = typer.Option(
        None,
        "--file",
        "-f",
        help="A file with passwords listed one at a line",
        show_default=False,
    ),
    json_path: Optional[str] = typer.Option(
        None,
        "--json",
        "-j",
        help="The path for the json file that contains the passwords",
        show_default=False,
    ),
    csv_path: Optional[str] = typer.Option(
        None,
        "--csv",
        "-c",
        help="The path for the csv file that contains the passwords",
        show_default=False,
    ),
    firefox: Optional[bool] = typer.Option(
        None,
        help="""Use this option along with the "--csv" if you want to provide a Firefox export,
                otherwise a Bitwarden export will be expected by default""",
        show_default=False,
    ),
):
    """
    This app will check databases of leaked passwords to know whether your
    passowrds have been previously leaked.
    It supports batch checking with json files, csv and normal files.
    The csv and json formats were tested on exported files from Bitwarden only,
    so other exports won't work.
    """
    if password:
        process_single_password(password)
    if file:
        process_file(file)
    if json_path:
        process_json(json_path)
    if csv_path:
        process_csv(csv_path, firefox)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        typer.run(main)
