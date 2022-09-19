import json_stream
from pprintpp import pformat
import sys
from typing import Any, IO, Iterable, List
from headj.h_error import h_error

DEF_COUNT: int = 100
DEF_INDENT: int = 5
DEF_SKIP: int = 0


class JSONProcessingError(Exception):
    """"""


def run_headj(
    infile: IO = sys.stdin,
    output: IO = sys.stdout,
    keys: Iterable[str] = tuple(),
    quiet: bool = False,
    count: int = DEF_COUNT,
    skip: int = DEF_SKIP,
    format_json: bool = False,
    debug: bool = False,
    show_stack_trace: bool = False,
    keep_output_open: bool = False,
):
    """.msg"""
    h_error.init_config(quiet=quiet, debug=debug, show_stack_trace=show_stack_trace)
    try:
        h_error.debug("Keys = %r", keys)
        the_json = json_stream.load(infile)
        json_out = process(the_json, count, skip, keys)
        text_out = post_process(json_out, keys, format_json)
        output.write(text_out)
    except JSONProcessingError as e:
        h_error.warning(str(e))
        if show_stack_trace:
            raise
    except Exception as e:
        # warning?
        h_error.print(e)
        if show_stack_trace:
            raise
    finally:
        if not keep_output_open:
            output.close()


def process(the_json, count: int, skip: int, keys: Iterable[str]) -> List[Any]:
    """"""
    obj = the_json
    json_out = []
    # It would be nice to be able to output all of the JSON except the elements that
    # we are filtering.
    for key in keys:
        try:
            obj = obj[key]
        except KeyError:
            msg = 'Could not find key "%s" in object "%s".' % (
                key,
                pformat(obj, indent=DEF_INDENT),
            )
            h_error.debug(
                msg,
            )
            raise JSONProcessingError(msg)
        except TypeError:
            msg = "Could not look up key \"%s\" in non-dictionary-object '%s'." % (
                key,
                pformat(obj, indent=DEF_INDENT),
            )
            h_error.debug(
                msg,
            )
            raise JSONProcessingError(msg)
    last_element = skip + count
    for index, element in enumerate(obj):
        if index < skip:
            continue
        elif index >= last_element:
            return json_out
        else:
            json_out.append(element)
    else:
        return json_out


def post_process(json_list: List[Any], keys: Iterable[str], format_json: bool) -> str:
    json_out = json_list
    # This would cause issues if json_out is large
    if format_json:
        text_out = pformat(json_out, indent=DEF_INDENT)
    else:
        text_out = str(json_out)
    return text_out
