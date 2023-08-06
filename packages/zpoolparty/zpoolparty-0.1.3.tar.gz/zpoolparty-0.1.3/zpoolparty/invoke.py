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

import subprocess

from . import argv
from .util import assert_same_host, bucket_by_host, parse_dataset_name


class CommandBuilder(object):
    def __init__(self, executable, command, args):
        self.executable = executable
        self.command = command
        self.args = args

    def execute(self):
        cmd = self.full_command()
        print('# %s' % ' '.join(cmd))
        return subprocess.check_call(cmd)

    @classmethod
    def parse(self, command, kwargs, dataset_field):
        if type(dataset_field) is str:
            # signle dataset field, specifying one or more datasets
            for host, datasets in bucket_by_host(kwargs[dataset_field]).items():
                # strip host from each argument
                new_kwargs = kwargs.copy()
                new_kwargs[dataset_field] = datasets
                yield CommandBuilder._make_runner(command, new_kwargs, host)

            # if dataset argument is optional (as in zfs list) and unspecified,
            # run command locally with unmodified arguments
            if len(kwargs[dataset_field]) == 0:
                yield CommandBuilder._make_runner(command, kwargs, host=None)

        else:
            # commands with two dataset fields (clone, diff, rename)
            # both datasets must have the same host
            assert_same_host(*(kwargs[field] for field in dataset_field))

            # strip host from each argument
            new_kwargs = kwargs.copy()
            for field in dataset_field:
                host, name = parse_dataset_name(kwargs[field])
                new_kwargs[field] = name
            yield CommandBuilder._make_runner(command, new_kwargs, host)

    @classmethod
    def _make_runner(self, command, kwargs, host):
        # re-generate array of command-line arguments from manipulated kwargs
        zfs_args = getattr(argv, command)(**kwargs)

        #TODO allow switching between zzzfs and real ZFS (how?)
        if host is not None:
            runner = RemoteRunenr('zfs', command, zfs_args)
            runner.set_host(host)
        else:
            runner = LocalRunner('zfs', command, zfs_args)

        return runner


class LocalRunner(CommandBuilder):
    def full_command(self):
        return [self.executable, self.command] + self.args


class RemoteRunenr(CommandBuilder):
    def set_host(self, host):
        self.host = host

    def full_command(self):
        return ['ssh', self.host, self.executable, self.command] + self.args
