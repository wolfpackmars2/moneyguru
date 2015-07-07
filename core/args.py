# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filepath',
        nargs='?',
        help="Path of the moneyGuru file to open at startup"
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help="Start moneyGuru in debug mode"
    )
    return parser

