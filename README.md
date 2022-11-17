# Password Checker

This an async password checker that checks whether your passwords have been pwned or not. It achieves that by querying the [Have I Been Pwned](https://haveibeenpwned.com/) databases. This is achieved via using the K-Anonomity model, thus your passwords aren't really travering the internet or being recorded on a remote server. The passwords is hashed and the prefix is sent and a list of suffix-matches are returned. The processing happens on your local machine, ensuring that your passowrds and identity remain private.

The tool can be fed a single password, a batch file or Bitwarden and Firefox password exports (CSV and JSON). Otherwise you can add the passwords in normal text file, one password per line.

```
 Usage: main.py [OPTIONS]

 This app will check databases of leaked passwords to know whether your passowrds
 have been previously leaked. It supports batch checking with json files, csv and
 normal files. The csv and json formats were tested on exported files from Bitwarden
 only, so other exports won't work.

╭─ Options ─────────────────────────────────────────────────────────────────────────╮
│ --password            -p                  TEXT  The password to check if you just │
│                                                 want to check one password        │
│ --file                -f                  TEXT  A file with passwords listed one  │
│                                                 at a line                         │
│ --json                -j                  TEXT  The path for the json file that   │
│                                                 contains the passwords            │
│ --csv                 -c                  TEXT  The path for the csv file that    │
│                                                 contains the passwords            │
│ --firefox                 --no-firefox          Use this option along with the    │
│                                                 "--csv" if you want to provide a  │
│                                                 Firefox export, otherwise a       │
│                                                 Bitwarden export will be expected │
│                                                 by default                        │
│ --install-completion                            Install completion for the        │
│                                                 current shell.                    │
│ --show-completion                               Show completion for the current   │
│                                                 shell, to copy it or customize    │
│                                                 the installation.                 │
│ --help                                          Show this message and exit.       │
╰───────────────────────────────────────────────────────────────────────────────────╯
```
