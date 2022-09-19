import argparse
import sys
from typing import List

from headj.process import run_headj, DEF_COUNT, DEF_SKIP


def key_path(s: str) -> List[str]:
    keys = []
    current_key = ""
    is_quote = False
    for c in s:
        if is_quote:
            current_key += c
            is_quote = False
        elif c == "\\":
            is_quote = True
        elif c == ".":
            keys.append(current_key)
            current_key = ""
        else:
            current_key += c
    if current_key:
        keys.append(current_key)
    return keys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Don't print any status, diagnostic or error messages",
    )
    parser.add_argument(
        "-k",
        "--key",
        default=list(),
        type=key_path,
        dest="keys",
        help="The JSON key of the array to copy from. If none specified,"
        + " treat the input JSON as an array.",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=DEF_COUNT,
        help="Number of elements to copy to the output (default: %(default)s)",
    )
    parser.add_argument(
        "-s",
        "--skip",
        type=int,
        default=DEF_SKIP,
        help="Number of elements to skip before copying (default: %(default)s)",
    )
    parser.add_argument(
        "-f",
        "--format",
        action="store_true",
        dest="format_json",
        help="Nicely format the output JSON with indentation & newlines.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="File to write the JSON results to (default: Standard Output)",
    )
    parser.add_argument(
        "infile",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="The JSON file to read from. If none is specified, reads from Standard Input",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Activate extra debugging output"
    )
    parser.add_argument(
        "-t",
        "--trace",
        action="store_true",
        dest="show_stack_trace",
        help="Show a stack trace for exceptions",
    )
    parser.add_argument(
        "-n",
        "--no-context",
        action="store_false",
        help="Just return the list, don't place it in its original JSON context",
        dest="in_context",
    )
    args = parser.parse_args()
    arg_dict = vars(args)
    run_headj(**arg_dict)
