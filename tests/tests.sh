#!/usr/bin/env bash

poetry run headj --help
#usage: headj [-h] [-q] [-k KEYS] [-c COUNT] [-s SKIP] [-f] [-o OUTPUT] [-d] [-t] [infile]
#
#positional arguments:
#  infile                The JSON file to read from. If none is specified, reads from
#                        Standard Input
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -q, --quiet           Don't print any status, diagnostic or error messages
#  -k KEYS, --key KEYS   The JSON key of the array to copy from. If none specified, treat
#                        the input JSON as an array.
#  -c COUNT, --count COUNT
#                        Number of elements to copy to the output (default: 100)
#  -s SKIP, --skip SKIP  Number of elements to skip before copying (default: 0)
#  -f, --format
#  -o OUTPUT, --output OUTPUT
#                        File to write the JSON results to (default: Standard Output)
#  -d, --debug           Activate extra debugging output
#  -t, --trace           Show a stack trace for exceptions

#echo '>poetry run headj /dev/null'
poetry run headj /dev/null
# No Output

poetry run headj <<- JSON
[1,2,3,4,5]
JSON
# Output: [1, 2, 3, 4, 5]

poetry run headj -c 1 <<- JSON
[1,2,3,4,5]
JSON
# Output: [1]

poetry run headj -c 1 -s 2 <<- JSON
[1,2,3,4,5]
JSON
# Output: [3]

poetry run headj -c 2 -s 2 <<- JSON
[1,2,3,4,5]
JSON
# Output: [3, 4]

poetry run headj -k 'foo' <<- JSON
{"foo":[1,2,3,4,5]}
JSON
# Output: ['foo']

poetry run headj -c 2 -s 2 <<- JSON
[1,2,3,4,5]
JSON
# Output: [3, 4]

poetry run headj -c 2 -s 2 <<- JSON
[1,2,3,4,5]
JSON
# Output: [3, 4]

poetry run headj -c 2 -s 2 <<- JSON
[1,2,3,4,5]
JSON
# Output: [3, 4]

poetry run headj -c 2 -s 2 <<- JSON
[1,2,3,4,5]
JSON
# Output: [3, 4]

poetry run headj -k 'foo.bar' -c 2 -s 2 <<- JSON
{"foo":{"bar":[1,2,3,4,5]}}
JSON
# Output: [3, 4]

poetry run headj -k 'foo.bar' -c 2 -s 2 <<- JSON
{"foo":{
"bar":[1,2,3,4,5]}
}
JSON
# Output: [3, 4]

poetry run headj -k 'foo' -c 2 -s 2 <<- JSON
{"foo":[1,2,3,4,5]}
JSON
# Output: [3, 4]

poetry run headj -k 'foo' /dev/null
# Error: cannot unpack non-iterable NoneType object

poetry run headj -k 'fooo.bar' -c 2 -s 2 <<- JSON
{"foo":{
"bar":[1,2,3,4,5]}
}
JSON
# Error: Could not find key "fooo" in object "<TransientStreamingJSONObject: TRANSIENT, DONE>".

poetry run headj -k 'foo' -c 2 -s 2 <<- JSON
{"bar":[1,2,3,4,5]}
JSON
# Error: Could not find key "foo" in object "<TransientStreamingJSONObject: TRANSIENT, DONE>".

poetry run headj -k 'foo' <<- JSON
[1,2,3,4,5]
JSON
# Error: Could not look up key "foo" in non-dictionary-object '<TransientStreamingJSONList:  #TRANSIENT, STREAMING>'.

poetry run headj -k 'foo' -c 2 -s 2 <<- JSON
{"bar":[1,2,3,4,5]}
JSON
# Error: Could not find key "foo" in object "<TransientStreamingJSONObject: TRANSIENT, DONE>".

poetry run headj -k 'foo' -c 2 -s 2 <<- JSON
{"bar":[1,2,3,4,5]}
JSON
# Error: Could not find key "foo" in object "<TransientStreamingJSONObject: TRANSIENT, DONE>".

poetry run headj -k 'foo.bar' -c 2 -s 2 <<- JSON
{"foo":{"bar":[1,2,3,4,5]}}
JSON
# Error: foo not found in transient JSON stream or already passed in this stream

poetry run headj -k 'foo.bar' -c 2 -s 2 <<- JSON
{"foo":{"bar":[1,2,3,4,5]}}
JSON
# Error: foo not found in transient JSON stream or already passed in this stream

poetry run headj -k 'foo.barz' -c 2 -s 2 <<- JSON
{"foo":{"bar":[1,2,3,4,5]}}
JSON
# Error: Could not find key "barz" in object "<TransientStreamingJSONObject: TRANSIENT, DONE>".

poetry run headj -k 'fooo.bar' -c 2 -s 2 <<- JSON
{"foo":{"bar":[1,2,3,4,5]}}
JSON
# Error: Could not find key "fooo" in object "<TransientStreamingJSONObject: TRANSIENT, DONE>".

poetry run headj -k 'foo.bar' -c 2 -s 2 <<- JSON
{"foo":{"bar":[1,2,3,4,5]}}
JSON
# Error: foo not found in transient JSON stream or already passed in this stream
