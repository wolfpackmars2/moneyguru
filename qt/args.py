# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

import core.args

def get_parser():
    parser = core.args.get_parser()
    parser.add_argument(
        '--log-to-stdout',
        action='store_true',
        help="Log to stdout instead of the regular log file"
    )
    return parser

