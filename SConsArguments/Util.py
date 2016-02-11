"""`SConsArguments.Util`

Common utilities
"""

#
# Copyright (c) 2015 by Pawel Tomulik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

__docformat__ = "restructuredText"

import SCons.Util
import string

#############################################################################
ENV = 0
"""Represents selection of construction variable (ENV *endpoint*) corresponding
to particular *argument*."""

VAR = 1
"""Represents selection of command-line variable (VAR *endpoint*) corresponding
to particular *argument* variable."""

OPT = 2
"""Represents selection of command-line option (OPT *endpoint*) related to
particular *argument*."""

ALL = 3
"""Number of all namespaces (currently there are three: ``ENV``, ``VAR``,
``OPT``)"""
#############################################################################

#############################################################################
class _missing_meta(type):
    "Meta-class for the `_missing` class"
    def __bool__(self):
        return False
    __nonzero__ = __bool__
    def __repr__(cls):
        return 'MISSING'

#############################################################################
class _missing(object):
    "Represents missing argument to function."
    __metaclass__ = _missing_meta

#############################################################################
MISSING = _missing
"""Represents missing argument to a function."""

#############################################################################
class _undef_meta(type):
    """Meta-class for the `_undef` class"""
    def __bool__(self):
        return False
    __nonzero__ = __bool__
    def __repr__(cls):
        return 'UNDEFINED'

#############################################################################
class _undef(object):
    "Represents undefined/inexistent variable. This is not the same as ``None``"
    __metaclass__ = _undef_meta

UNDEFINED = _undef
"""Represents undefined/inexistent variable. This is not the same as ``None``"""

#############################################################################
class _notfound_meta(type):
    """Meta-class for the `_notfound` class"""
    def __bool__(self):
        return False
    __nonzero__ = __bool__
    def __repr__(cls):
        return 'NOTFOUND'

#############################################################################
class _notfound(object):
    "Something that has not been found, a result of failed search."
    __metaclass__ = _notfound_meta

NOTFOUND = _notfound
"Something that has not been found, a result of failed search."

#############################################################################
def _resubst(value, resubst_dict = {}):
    """Rename placeholders (substrings like ``$name``) in a string. This
    function is for internal use and IS **NOT a part of public API**.

    :Parameters:
        value
            the value to be processed; if it is a string, it is passed through
            placeholder renaming procedure; otherwise it is returned unaltered,
        resubst_dict
            a dictionary of the form ``{ "xxx":"${yyy}", "vvv":"${www}", ...}``
            used to rename placeholders within `value` string; with the above
            dictionary, all occurrences of ``$xxx`` or ``${xxx}`` within
            `value` string will be replaced with ``${yyy}``, all occurrences of
            ``$vvv`` or ``${vvv}`` with ``${www}`` and so on; see also
            `_build_resubst_dict()`,
    :Returns:
        returns the `value` with placeholders renamed.
    """
    if SCons.Util.is_String(value):
        # make substitution in strings only
        return string.Template(value).safe_substitute(**resubst_dict)
    else:
        return value

#############################################################################
def _build_resubst_dict(rename_dict):
    """Build dictionary for later use with `_resubst()`. This function is for
    internal use and IS **NOT a part of public API**.

    **Example**

    .. python::

        >>> import SConsArguments
        >>> SConsArguments._build_resubst_dict( {"xxx":"yyy", "vvv":"www", "zzz":"zzz" })
        {'vvv': '${www}', 'xxx': '${yyy}'}

    :Parameters:
        rename_dict : dict
            dictionary of the form ``{"xxx":"yyy", "vvv":"www", ...}``
            mapping variable names from one namespace to another,

    :Returns:
        returns dictionary of the form ``{"xxx":"${yyy}", "vvv":"${www}"}``
        created from `rename_dict`; items ``(key, val)`` with ``key==val`` are
        ignored, so the entries of type ``"zzz":"zzz"`` do not enter the
        result.
    """
    return dict(map(lambda x: (x[0], '${' + x[1] + '}'),
                    filter(lambda x : x[0] != x[1], rename_dict.iteritems())))

#############################################################################
def _build_iresubst_dict(rename_dict):
    """Build inversed dictionary for later use with `_resubst()`. This function
    is for internal use and IS **NOT a part of public API**.

    **Example**

    .. python::

        >>> import SConsArguments
        >>> SConsArguments._build_iresubst_dict( {"xxx":"yyy", "vvv":"www", "zzz":"zzz" })
        {'www': '${vvv}', 'yyy': '${xxx}'}

    :Parameters:
        rename_dict : dict
            dictionary of the form ``{"xxx":"yyy", "vvv":"www", ...}``
            mapping variable names from one namespace to another

    :Returns:
        returns dictionary of the form ``{"yyy":"${xxx}", "www":"${vvv}",
        ...}`` created from inverted dictionary `rename_dict`; items ``(key,
        val)`` with ``key==val`` are ignored, so the entries of type
        ``"zzz":"zzz"`` do not enter the result;
    """
    return dict(map(lambda x: (x[1], '${' + x[0] + '}'),
                    filter(lambda x : x[0] != x[1], rename_dict.iteritems())))

#############################################################################
def _compose_mappings(dict1, dict2):
    """Compose two mappings expressed by dicts ``dict1`` and ``dict2``. This
    function is for internal use and IS **NOT a part of public API**.

    **Example**

    .. python::

        >>> import SConsArguments
        >>> SConsArguments._compose_mappings({'a' : 'A', 'b' : 'B'}, {'A' : '1', 'B' : '2' })
        {'a': '1', 'b': '2'}

    :Parameters:
        dict1, dict2
            dictionaries to compose

    :Returns:
        returns a dictionary such that for each item ``(k1,v1)`` from `dict1`
        and ``v2 = dict2[v1]`` the corresponding item in returned dictionary is
        ``(k1,v2)``
    """
    return dict(map(lambda x : (x[0], dict2[x[1]]), dict1.iteritems()))

#############################################################################
def _invert_dict(_dict):
    return dict(map(lambda x : (x[1],x[0]), _dict.iteritems()))

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
