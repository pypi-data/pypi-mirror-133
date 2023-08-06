# -*- coding: utf-8 -*-


import collections

VersionInfo = collections.namedtuple(
    'VersionInfo', ['major', 'minor', 'micro', 'release_level'])

version_info = VersionInfo(major=0, minor=2, micro=0, release_level="beta")
__version__ = '{0}.{1}.{2}'.format(
    version_info.major, version_info.minor, version_info.micro)
