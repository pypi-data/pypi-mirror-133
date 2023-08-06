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

import re


HOST_SEPARATOR = ':'


class ZPoolPartyException(Exception): pass


def parse_dataset_name(identifier):
    '''Return (host, dataset) from host:pool/fs@snapshot format.'''
    m = re.match(
        r'(?P<host>[^/%s]+)%s(?P<rest>.*)' % (HOST_SEPARATOR, HOST_SEPARATOR),
        identifier)

    if m is None:  # no hostname specified
        return (None, identifier)

    return (m.group('host'), m.group('rest'))


def bucket_by_host(datasets):
    if type(datasets) is str:
        host, name = parse_dataset_name(datasets)
        return {host: name}

    hosts = {}
    for dataset in datasets:
        host, name = parse_dataset_name(dataset)
        hosts.setdefault(host, []).append(name)
    return hosts


def assert_same_host(*args):
    if len(bucket_by_host(args).keys()) != 1:
        raise ZPoolPartyException('hosts must be the same')
