"""Parse command-line arguments"""

import argparse


def init_arg_parser(parser: argparse.ArgumentParser):
    """Initialise argument parser"""
    parser.add_argument(
            "-f", "--file", nargs="?", metavar="<file>", required=True,
            help="C source file"
    )

    parser.add_argument(
            "-c", "--check", action="store_true", default=False,
            help="check source file compiles before parsing"
    )

    parser.add_argument(
            "-d", "--debug", action="store_true", default=False,
            help="enable debug logging"
    )
