#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import importlib_metadata
import sys
import traceback

__all__ = (
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
)

__copyright__ = "Copyright 2021 ibrahim CÖRÜT"
metadata = importlib_metadata.metadata("corut")
__title__ = metadata["name"]
__summary__ = metadata["summary"]
__uri__ = metadata["home-page"]
__version__ = metadata["version"]
__author__ = metadata["author"]
__email__ = metadata["author-email"]
__license__ = metadata["license"]


def print_error(error, *args, **kwargs):
    print("@" * 99)
    print(f"Error   >----> {error.__class__}")
    print(f"Message >----> {error}")
    print('-' * 99)
    print(f"args    >----> {args}")
    print('-' * 99)
    print(f"kwargs  >----> {kwargs}")
    print('-' * 99)
    exc_type, exc_value, exc_tb = sys.exc_info()
    for line in traceback.format_exception(exc_type, exc_value, exc_tb):
        print(line)
    print("@" * 99)
