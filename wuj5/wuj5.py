#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
import sys


if __package__ in {None, ''}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from wuj5.api import decode_file, encode_file


def main(argv=None):
    parser = ArgumentParser()
    parser.add_argument('operation', choices=['decode', 'encode'])
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('-o', '--outputs', nargs='*')
    parser.add_argument('--retained', nargs='*')
    parser.add_argument('--renamed', action='append', nargs=2)
    args = parser.parse_args(argv)

    operations = {
        'decode': decode_file,
        'encode': encode_file,
    }
    if args.outputs is None:
        args.outputs = [None] * len(args.inputs)
    if len(args.outputs) != len(args.inputs):
        parser.error('Wrong number of output paths.')
    renamed = {}
    if args.renamed is not None:
        renamed = {src: dst for src, dst in args.renamed}
    for in_path, out_path in zip(args.inputs, args.outputs):
        try:
            operations[args.operation](in_path, out_path, args.retained, renamed)
        except Exception as e:
            sys.exit(str(e))


if __name__ == '__main__':
    main()
