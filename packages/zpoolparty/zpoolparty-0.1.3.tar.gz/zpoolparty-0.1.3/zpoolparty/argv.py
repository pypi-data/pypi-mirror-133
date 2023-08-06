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


# The inverse of ZzzfsCommandInterpreter: from a set of parameters, construct
# an argv array for the given ZFS command.

def clone(snapshot, filesystem):
    return [snapshot, filesystem]


def create(filesystem, create_parents, properties):
    ret = [filesystem]
    if create_parents:
        ret.append('-p')
    for p in properties:
        ret += ['-o', str(p)]
    return ret


def destroy(filesystem, recursive):
    ret = [filesystem]
    if recursive:
        ret.append('-r')
    return ret


def diff(identifier, other_identifier):
    return [identifier, other_identifier]


def get(properties, identifiers, headers, sources, scriptable_mode, recursive,
        max_depth, types):
    ret = [str(properties)] + identifiers
    if scriptable_mode:
        ret.append('-H')
    if max_depth:
        ret += ['-d', max_depth]
    if recursive:
        rett.append('-r')
    if headers:
        ret += ['-o', str(headers)]
    if types:
        ret += ['-t', str(types)]
    return ret


def inherit(property, identifiers):
    return [property] + identifiers


def list(identifiers, types, scriptable_mode, headers, recursive, max_depth,
         sort_asc, sort_desc):
    ret = identifiers
    if scriptable_mode:
        ret.append('-H')
    if max_depth:
        ret += ['-d', max_depth]
    if recursive:
        ret.append('-r')
    if headers:
        ret += ['-o', str(headers)]
    if types:
        ret += ['-t', str(types)]
    for s in sort_asc:
        ret += ['-s', s]
    for s in sort_desc:
        ret += ['-S', s]
    return ret


def promote(clone_filesystem):
    return [clone_filesystem]


def receive(filesystem):
    return [filesystem]


def rename(identifier, other_identifier):
    return [identifier, other_identifier]


def rollback(snapshot):
    return [snapshot]


def send(snapshot):
    return [snapshot]


def set(keyval, identifiers):
    return [str(keyval)] + identifiers


def snapshot(snapshots, properties):
    ret = snapshots
    for p in properties:
        ret += ['-o', str(p)]
    return ret
