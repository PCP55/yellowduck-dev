import sys
from pkg_resources import get_distribution


def get_ver(package):
    return get_distribution(package).version


__version__ = get_ver("yellowduck")
