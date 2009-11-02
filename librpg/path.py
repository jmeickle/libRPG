"""
The :mod:`path` module provides functions for portable access to
LibRPG's installed folders, especially the ones that contain data.
"""

import os


def lib_path(relative_path='.'):
    """
    Return the absolute file path of a file, specified by a *relative_path*
    to the librpg module root directory.
    """
    return os.path.join(os.path.split(__file__)[0], relative_path)


def data_path(relative_path='.'):
    """
    Return the absolute file path of a file, specified by a *relative_path*
    to the librpg data root directory.
    """
    path = os.path.join('data', relative_path)
    return lib_path(path)


def tileset_path(relative_path='.'):
    """
    Return the absolute file path of a file, specified by a *relative_path*
    to the librpg data/tileset directory.
    """
    path = os.path.join('tileset', relative_path)
    return data_path(path)


def charset_path(relative_path='.'):
    """
    Return the absolute file path of a file, specified by a *relative_path*
    to the librpg data/charset directory.
    """
    path = os.path.join('charset', relative_path)
    return data_path(path)


def cursor_theme_path(relative_path='.'):
    """
    Return the absolute file path of a file, specified by a *relative_path*
    to the librpg data/cursor_theme directory.
    """
    path = os.path.join('cursor_theme', relative_path)
    return data_path(path)
