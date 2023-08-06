#!/usr/bin/env python2.7
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License, version 1.1 (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at ./LICENSE.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at ./LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

# Copyright (c) 2016 Daniel W. Steinbrook. All rights reserved.

import sys

from libzzzfs.interpreter import ZzzfsCommandInterpreter

from .invoke import CommandBuilder


# mapping from ZFS command to parameter(s) specifying datasets
DATASET_FIELDS = {
    'clone':   ['filesystem', 'snapshot'],
    'create':   'filesystem',
    'destroy':  'filesystem',
    'diff':    ['identifier', 'other_identifier'],
    'get':      'identifiers',
    'inherit':  'identifiers',
    'list':     'identifiers',
    'promote':  'clone_filesystem',
    'receive':  'snapshot',
    'rename':  ['identifier', 'other_identifier'],
    'rollback': 'snapshot',
    'send':     'snapshot',
    'set':      'identifiers',
    'snapshot': 'snapshots'
}


def zpoolparty_main(argv):
    cmd = ZzzfsCommandInterpreter(argv[1:])

    command = cmd.args.command
    if command is None:
        sys.exit(cmd.parser.print_usage())

    return list(
        CommandBuilder.parse(command, cmd.params, DATASET_FIELDS[command]))


def main():
    # execute each command returned by the command builder
    for runner in zpoolparty_main(sys.argv):
        runner.execute()


if __name__ == '__main__':
    main()
