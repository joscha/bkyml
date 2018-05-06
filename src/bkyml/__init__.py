# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    # pylint: disable=invalid-name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:  # pragma: no cover
    __version__ = 'unknown'   # pragma: no cover
