"""
Compatibility patch for experta with Python 3.12+
This module patches the collections.Mapping deprecation issue in frozendict.
"""

import collections
import collections.abc

# Monkey patch for Python 3.12+ compatibility
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, 'Iterable'):
    collections.Iterable = collections.abc.Iterable
if not hasattr(collections, 'MutableSet'):
    collections.MutableSet = collections.abc.MutableSet
