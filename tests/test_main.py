import pytest


class TestKeyPath:
    """"""


HELP_TEXT = """
usage: headj [-h] [-q] [-k KEYS] [-c COUNT] [-s SKIP] [-f] [-o OUTPUT] [-d] [-t] [infile]

positional arguments:
  infile                The JSON file to read from. If none is specified, reads from
                        Standard Input

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Don't print any status, diagnostic or error messages
  -k KEYS, --key KEYS   The JSON key of the array to copy from. If none specified, treat
                        the input JSON as an array.
  -c COUNT, --count COUNT
                        Number of elements to copy to the output (default: 100)
  -s SKIP, --skip SKIP  Number of elements to skip before copying (default: 0)
  -f, --format
  -o OUTPUT, --output OUTPUT
                        File to write the JSON results to (default: Standard Output)
  -d, --debug           Activate extra debugging output
  -t, --trace           Show a stack trace for exceptions
"""


class TestMain:
    """"""

    # poetry run headj --help
