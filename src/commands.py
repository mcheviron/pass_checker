import asyncio
import contextlib
import csv
import json

from rich import print as rprint
from rich.table import Table

from core import fetch_hashes, hash, pwned, run_coros


def process_single_password(password):
    prefix, suffix = hash(password)
    ls_hashes = asyncio.run(fetch_hashes(prefix))
    state, times = pwned(suffix, ls_hashes)
    if state:
        print(f"{password} has been pwned {times} times")
    else:
        print(f"{password} is safe to use")


def process_passwords(passwords, pass_data):
    for password in passwords:
        prefix, suffix = hash(password)
        pass_data.append(
            {"password": password, "prefix": prefix, "suffix": suffix}
        )

    prefixes = [entry["prefix"] for entry in pass_data]
    generators = asyncio.run(run_coros(*prefixes))
    for prefix, gen in generators:
        for entry in pass_data:
            if prefix == entry["prefix"]:
                entry["hashes"] = gen

    for entry in pass_data:
        entry["pwned"], entry["times"] = pwned(
            entry["suffix"], entry["hashes"]
        )

    table = Table(title="Password Data", expand=True, highlight=True)
    table.add_column("Password", justify="left", style="bold cyan")
    table.add_column("Pwned", justify="center", style="bold green")
    table.add_column("Times", justify="center")
    for entry in pass_data:
        table.add_row(
            entry["password"], str(entry["pwned"]), str(entry["times"])
        )
    rprint(table)


def process_file(file):
    with contextlib.suppress(FileNotFoundError):
        pass_data = []
        with open(file) as file:
            passwords = {password.strip() for password in file.readlines()}

        process_passwords(passwords, pass_data)


def process_json(json_path):
    with contextlib.suppress(FileNotFoundError):
        pass_data = []
        with open(json_path) as file:
            data = json.loads(file.read())
        passwords = {
            entry.get("login").get("password") for entry in data["items"]
        }
        process_passwords(passwords, pass_data)


def process_csv(csv_path, firefox=None):
    with contextlib.suppress(FileNotFoundError):
        pass_data = []
        row_num = 2 if firefox else 9
        with open(csv_path) as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            passwords = {row[row_num] for row in csvreader}
            # passwords.remove("login_password")

            process_passwords(passwords, pass_data)
